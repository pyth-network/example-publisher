import time
from example_publisher.config import Config
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from example_publisher.publisher import Publisher


class API(FastAPI):
    publisher: Publisher
    config: Config


app = API()


def is_healthy():
    last_successful_update = API.publisher.last_successful_update
    return (
        last_successful_update is not None
        and time.time() - last_successful_update
        < API.config.health_check_threshold_secs
    )


@app.get("/health")
def health_check():
    healthy = is_healthy()
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
