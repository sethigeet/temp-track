from uagents import Model
from pydantic import Field


class TrackerStatus(Model):
    loc: str = Field(description="The location whose status is given.")
    min_temp: float = Field(description="The minimun temperature of the range set.")
    max_temp: float = Field(description="The maximum temperature of the range set.")
    curr_temp: float = Field(
        description="The current temperature of the given location."
    )
    within_range: bool = Field(
        description="Whether the current temperature is within the range specified by the user."
    )
