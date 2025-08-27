from fastapi import FastAPI

from .api.ping import router as ping_router
from .api.users import router as users_router
from .api.transfer import router as transfer_router

app = FastAPI()
app.include_router(ping_router)
app.include_router(users_router)
app.include_router(transfer_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
