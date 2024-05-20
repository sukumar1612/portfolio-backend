from litestar import Litestar
from backend.container import AppContainer

# initialize container
container = AppContainer()
container.init_resources()
container.wire(modules=[__name__])
container.firebase_app()

# initialize app
web_app = Litestar()
web_app.register(container.home_router().router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(web_app, host="0.0.0.0", port=8000, reload=False)

    # do not run uvicorn server with reload = True, the firebase app gets initialized twice giving error
