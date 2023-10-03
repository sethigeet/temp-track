import logging
from uagents import Agent, Context

from temp_track.utils import weatherapi
from temp_track.messages import TrackerStatus, TrackerError
from .notifier import notifier

tracker = Agent(name="tracker", seed="tracker-agent-seed")
tracker._logger = logging.Logger("tracker-logger", logging.ERROR)


def set_tracker_temp_range(min_temp: float, max_temp: float) -> None:
    """Set the temperature range to be used by the tracker."""
    tracker.storage.set("min_temp", min_temp)
    tracker.storage.set("max_temp", max_temp)


def set_tracker_location(loc: str) -> None:
    """Set the location of the place whose temperature has to be tracked."""
    tracker.storage.set("loc", loc)


@tracker.on_interval(period=10.0 * 60)  # refresh every 10 mins
async def check_temp(ctx: Context) -> None:
    """Checks whether the temperature of the given location lies between the
    given min and max temperature values and sends a message to the notifier if
    it is not."""

    min_temp = ctx.storage.get("min_temp")  # type: float | None
    max_temp = ctx.storage.get("max_temp")  # type: float | None
    loc = ctx.storage.get("loc")  # type: str | None

    if min_temp is None or max_temp is None or loc is None:
        await ctx.send(
            notifier.address,
            TrackerError(
                title="Unable to fetch current temperature",
                description="`min_temp`, `max_temp` and `loc` should be set first using `set_tracker_temp_range` and `set_tracker_location`",
            ),
        )
        return

    try:
        curr_temp = weatherapi.get_curr_temp(loc)
        if curr_temp is None:
            await ctx.send(
                notifier.address,
                TrackerError(
                    title="Unable to fetch current temperature",
                    description="Please check your internet connection!",
                ),
            )
            return
    except Exception as e:
        await ctx.send(
            notifier.address,
            TrackerError(
                title="Unable to fetch current temperature",
                description=str(e),
            ),
        )
        return

    await ctx.send(
        notifier.address,
        TrackerStatus(
            curr_temp=curr_temp,
            within_range=(min_temp <= curr_temp <= max_temp),
        ),
    )
