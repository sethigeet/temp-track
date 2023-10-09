import logging
from uagents import Agent, Context

from temp_track.utils import weatherapi
from temp_track.messages import TrackerStatus, TrackerError
from .notifier import notifier

tracker = Agent(name="tracker", seed="tracker-agent-seed")
tracker._logger = logging.Logger("tracker-logger", logging.ERROR)


def set_loc_temp_range(loc: str, min_temp: float, max_temp: float) -> None:
    """Set the temperature range to be used by the tracker."""

    tracker.storage.set(f"{loc}.min_temp", min_temp)
    tracker.storage.set(f"{loc}.max_temp", max_temp)

    # Refresh status
    check_temp(tracker._ctx)


def add_tracker_location(loc: str) -> None:
    """Adds the location to the list of locations whose temperature has to be tracked."""

    locs = tracker.storage.get("locs")
    if locs is None:
        locs = []
    locs.append(loc)
    tracker.storage.set("locs", list(set(locs)))


@tracker.on_interval(period=10.0 * 60)  # refresh every 10 mins
async def check_temp(ctx: Context) -> None:
    """Checks whether the temperature of the given location lies between the
    given min and max temperature values and sends a message to the notifier if
    it is not."""

    locs = ctx.storage.get("locs")  # type: list[str] | None
    if locs is None:
        await ctx.send(
            notifier.address,
            TrackerError(
                loc="n/a",
                title="Unable to fetch current temperature",
                description="``loc` should be set first using `set_loc_temp_range` and `add_tracker_location`",
            ),
        )
        return

    for loc in locs:
        min_temp = ctx.storage.get(f"{loc}.min_temp")  # type: float | None
        max_temp = ctx.storage.get(f"{loc}.max_temp")  # type: float | None
        if min_temp is None or max_temp is None:
            await ctx.send(
                notifier.address,
                TrackerError(
                    loc=loc,
                    title="Unable to fetch current temperature",
                    description="`min_temp` and `max_temp` should be set first using `set_loc_temp_range`",
                ),
            )
            return

        try:
            curr_temp = weatherapi.get_curr_temp(loc)
            if curr_temp is None:
                await ctx.send(
                    notifier.address,
                    TrackerError(
                        loc=loc,
                        title="Unable to fetch current temperature",
                        description="Please check your internet connection!",
                    ),
                )
                return
        except Exception as e:
            await ctx.send(
                notifier.address,
                TrackerError(
                    loc=loc,
                    title="Unable to fetch current temperature",
                    description=str(e),
                ),
            )
            return

        await ctx.send(
            notifier.address,
            TrackerStatus(
                loc=loc,
                min_temp=min_temp,
                max_temp=max_temp,
                curr_temp=curr_temp,
                within_range=(min_temp <= curr_temp <= max_temp),
            ),
        )
