import logging
from uagents import Agent, Context

from temp_track.messages import TrackerStatus, TrackerError
from temp_track.notification_providers import NotificationProvider

notifier = Agent(name="notifier", seed="notifier-agent-seed")
notifier._logger = logging.Logger("notifier-logger", logging.ERROR)

notification_provider: NotificationProvider | None = None


def set_notification_proivder(provider: NotificationProvider) -> None:
    global notification_provider
    notification_provider = provider


@notifier.on_message(TrackerStatus)
async def on_tracker_status_msg(
    _ctx: Context, _sender: str, msg: TrackerStatus
) -> None:
    if notification_provider is None:
        raise Exception(
            "`notification_proivder` must be set using `set_notification_provider` before starting notifier!"
        )

    # Do anything that needs to be done before sending the msg!

    notification_provider.notify(msg)


@notifier.on_message(TrackerError)
async def on_tracker_error_msg(_ctx: Context, _sender: str, msg: TrackerError) -> None:
    if notification_provider is None:
        raise Exception(
            "`notification_proivder` must be set using `set_notification_provider` before starting notifier!"
        )

    # Do anything that needs to be done before sending the msg!

    notification_provider.notify_error(msg)
