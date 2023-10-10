from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@api.get("/api/status/{loc}")
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


class RegisterInput(BaseModel):
    loc: str
    min_temp: float
    max_temp: float

@api.post("/api/register")
async def register_loc(input: RegisterInput):
    try:
        tracker.add_tracker_location(input.loc)
        tracker.set_loc_temp_range(input.loc, input.min_temp, input.max_temp)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"msg": "Registered successfully!"},
        )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "An unknown error occurred!"},
        )

# Host react app!
api.mount("/assets", StaticFiles(directory="temp_track_web/dist/assets"), name="assets")
with open("temp_track_web/dist/index.html") as f:
    index_page = f.read()
@api.get("/")
@api.get("/home")
@api.get("/index.html")
async def get_index_page():
    return HTMLResponse(index_page)