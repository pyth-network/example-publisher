from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pyth_publisher.publisher import Publisher


class API(FastAPI):
    publisher: Publisher


app = API()


@app.get("/health")
def health_check():
    healthy = API.publisher.is_healthy()
    last_successful_update = API.publisher.last_successful_update
    if not healthy:
        return JSONResponse(
            content={
                "status": "error",
                "last_successful_update": last_successful_update,
            },
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    return JSONResponse(
        content={
            "status": "ok",
            "last_successful_update": last_successful_update,
        },
        status_code=status.HTTP_200_OK,
    )
