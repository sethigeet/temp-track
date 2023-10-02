from uagents import Model
from pydantic import Field


class TrackerStatus(Model):
    curr_temp: float = Field(
        description="The current temperature of the given location."
    )
    within_range: bool = Field(
        description="Whether the current temperature is within the range specified by the user."
    )
