from __future__ import annotations
import argparse
import logging
import os
import sys
import contextlib
from mcp_server import mcp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tiktoksearch.api import create_app
_CONFIG = os.environ.get('TTAPI_SIGNED_CONFIG', 'mobile/config_signed.yaml')
app = create_app(_CONFIG)

from mcp.server.transport_security import TransportSecuritySettings

mcp_security = TransportSecuritySettings(
    enable_dns_rebinding_protection=True,
    allowed_hosts=[
        "tiktok-search-api-bsez.onrender.com",
        "tiktok-search-api-bsez.onrender.com:*",
    ],
    allowed_origins=[
        "https://tiktok-search-api-bsez.onrender.com",
        "https://tiktok-search-api-bsez.onrender.com:*",
    ],
)

mcp_app = mcp.streamable_http_app()

original_lifespan = app.router.lifespan_context

@contextlib.asynccontextmanager
async def lifespan(app_instance):
    async with original_lifespan(app_instance):
        async with mcp.session_manager.run():
            yield

app.router.lifespan_context = lifespan
app.mount("/", mcp_app)
def main() -> None:
    parser = argparse.ArgumentParser(description='TikTok signed search API')
    parser.add_argument('--config', default=_CONFIG)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-7s %(name)s | %(message)s', datefmt='%H:%M:%S')
    import uvicorn
    application = app if args.config == _CONFIG else create_app(args.config)
    uvicorn.run(application, host=args.host, port=args.port, log_level='info')
if __name__ == '__main__':
    main()
