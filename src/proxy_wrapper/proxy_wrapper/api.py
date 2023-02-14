import os
from urllib.parse import urlsplit

import uvicorn
from uvicorn.config import LOGGING_CONFIG
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask
from starlette.datastructures import MutableHeaders
import httpx

from proxy_wrapper.exception import log_exception
from proxy_wrapper.logs import get_logger

logger = get_logger(__name__)

JOB_NAME = os.environ.get('JOB_NAME', 'job_name')
JOB_VERSION = os.environ.get('JOB_VERSION', 'job_version')
BASE_URL = f'/pub/job/{JOB_NAME}/{JOB_VERSION}'


def serve_proxy():
    fastapi_app = create_fastapi_app()

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "\033[2m[%(asctime)s]\033[0m %(levelname)s %(message)s"
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["default"]["()"] = "proxy_wrapper.logs.ColoredDefaultFormatter"

    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "\033[2m[%(asctime)s]\033[0m %(levelname)s %(request_line)s %(status_code)s"
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["access"]["()"] = "proxy_wrapper.logs.ColoredAccessFormatter"

    LOGGING_CONFIG["handlers"]["default"]["stream"] = 'ext://sys.stdout'
    LOGGING_CONFIG["handlers"]["access"]["stream"] = 'ext://sys.stdout'

    LOGGING_CONFIG["loggers"]["uvicorn"]["propagate"] = False

    http_port = int(os.environ.get('HTTP_PORT', 7000))
    uvicorn.run(app=fastapi_app, host="0.0.0.0", port=http_port, log_level="debug")


def create_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    subapi = FastAPI()

    setup_endpoints(subapi)
    app.mount(BASE_URL, subapi)

    @app.get("/")
    @app.get(BASE_URL)
    async def home():
        return RedirectResponse(f"{BASE_URL}/")

    @app.get("/job/status")
    async def _status():
        return {'status': 'ok'}

    @app.get("/live")
    async def _live():
        deployment_timestamp = int(os.environ.get('JOB_DEPLOYMENT_TIMESTAMP', '0'))
        return {
            'live': True,
            'deployment_timestamp': deployment_timestamp,
        }

    @app.get("/ready")
    async def _ready():
        return {'ready': True}

    @app.exception_handler(Exception)
    async def _error_handler(request: Request, exc: Exception):
        log_exception(exc)
        return JSONResponse(
            status_code=500,
            content={'error': str(exc)},
        )

    @subapi.exception_handler(Exception)
    async def _subapi_error_handler(request: Request, exc: Exception):
        log_exception(exc)
        return JSONResponse(
            status_code=500,
            content={'error': str(exc)},
        )

    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            log_exception(exc)
            return JSONResponse(
                status_code=500,
                content={'error': str(exc)},
            )

    app.middleware('http')(catch_exceptions_middleware)
    subapi.middleware('http')(catch_exceptions_middleware)

    return app


def setup_endpoints(app: FastAPI):
    user_module_hostname = os.environ['JOB_USER_MODULE_HOSTNAME']
    user_module_port = int(os.environ.get('JOB_USER_MODULE_PORT', 7001))
    logger.info(f'Proxying requests to "{user_module_hostname}:{user_module_port}" at base path "{BASE_URL}"')

    async def _proxy_endpoint(request: Request):

        subpath = f'/{request.path_params["path"]}'
        logger.info(f'Forwarding {request.url.path}{request.url.query} to: {subpath}')

        client = httpx.AsyncClient(base_url=f"http://{user_module_hostname}:{user_module_port}/")

        url = httpx.URL(path=subpath, query=request.url.query.encode("utf-8"))

        request_headers = MutableHeaders(request.headers)
        request_headers['referer'] = request.url.path

        rp_req = client.build_request(request.method, url,
                                      headers=request_headers.raw,
                                      content=await request.body())
        response = await client.send(rp_req, stream=True)
        content: bytes = await response.aread()
        headers = response.headers

        location_header = headers.get('location')
        if location_header:
            logger.debug(f'Transforming Location header into relative one: {location_header}')

            if location_header.startswith('://'):
                location_header = location_header[3:]

            split = urlsplit(location_header)
            if split.scheme or split.netloc:
                location_header = split._replace(scheme='', netloc='').geturl()
            else:
                location_header = '/' + location_header.split('/', 1)[-1]

            if location_header.startswith('/') and not location_header.startswith(BASE_URL):
                headers['location'] = BASE_URL + location_header
            else:
                headers['location'] = location_header

        if 'content-encoding' in headers:
            del headers['content-encoding']
            headers['content-length'] = str(len(content))

        if 'content-length' not in headers and 'transfer-encoding' not in headers and len(content) > 0:
            headers['content-length'] = str(len(content))
        
        if 'content-length' in headers and 'transfer-encoding' in headers:
            del headers['transfer-encoding']
            headers['content-length'] = str(len(content))

        return Response(
            content=content,
            status_code=response.status_code,
            headers=headers,
            background=BackgroundTask(response.aclose),
        )

    app.router.add_api_route("/{path:path}", _proxy_endpoint,
                             methods=["GET", "POST", "PUT", "DELETE"], tags=['API'])
