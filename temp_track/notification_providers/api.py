from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from temp_track.agents import tracker
from temp_track.messages import TrackerStatus, TrackerError
from . import NotificationProvider

msgs = {}
errors = {}


class APINotificationProvider(NotificationProvider):
    global msgs, errors

    def __init__(self) -> None:
        super().__init__()

    def notify(self, msg: TrackerStatus) -> None:
        msgs[msg.loc] = msg
        errors[msg.loc] = None

    def notify_error(self, msg: TrackerError) -> None:
        msgs[msg.loc] = None
        errors[msg.loc] = msg


api = FastAPI()
origins = ["http://localhost:3000", "localhost:3000"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/status/{loc}")
async def get_loc_status(loc: str):
    if loc not in msgs:
        stat = None
    else:
        stat = msgs[loc]
    if loc not in errors:
        error = None
    else:
        error = errors[loc]

    if stat is None and error is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "There is no location registered with this name!"},
        )
    return {"status": stat, "error": error}


@api.get("/register}")
async def register_loc(loc: str, min_temp: float, max_temp: float):
    try:
        tracker.add_tracker_location(loc)
        tracker.set_loc_temp_range(loc, min_temp, max_temp)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"msg": "Registered successfully!"},
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "An unknown error occurred!"},
        )
