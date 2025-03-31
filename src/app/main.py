from app.api import init_app
from app.api.common.server.uvicorn import run_uvicorn
from app.config import get_config


def main() -> None:
    config = get_config()
    app = init_app(config=config)

    run_uvicorn(app=app, config=config.server)


if __name__ == "__main__":
    main()
