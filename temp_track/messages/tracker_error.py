from uagents import Model
from pydantic import Field


class TrackerError(Model):
    title: str = Field(description="The title of the error that occurred.")
    description: str = Field(
        description="The detailed description of the error that occurred."
    )
