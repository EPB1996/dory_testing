from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

app = FastAPI()


global message
message = "Hello, World!"


@app.get("/message/")
def read_root():
    return {"message": message}


@app.post("/message/")
def post_root(payload: dict):
    global message
    message = payload["message"]
    return {"message": "Message set!"}


@app.get("/openapi.json")
def get_openapi_endpoint():
    """
    Retrieve the generated OpenAPI schema.
    """
    return JSONResponse(content=generate_openapi_schema())


def generate_openapi_schema():
    """
    Generate the OpenAPI schema for the FastAPI application.
    """
    return get_openapi(
        title="My API",
        version="1.0.0",
        description="This is my API description",
        routes=app.routes,
    )
