from rich.text import Text
from rich.live import Live

from temp_track.messages import TrackerStatus, TrackerError
from . import NotificationProvider


class ConsoleNotificationProvider(NotificationProvider):
    _live = Live("", refresh_per_second=1)

    def __init__(self) -> None:
        super().__init__()

        self._live.start()

    def notify(self, msg: TrackerStatus) -> None:
        if msg.within_range:
            self._live.update(
                f":white_heavy_check_mark: The current temperature ([bold]{msg.curr_temp}[/]) is [green bold]within[/] the specified range ({msg.min_temp}-{msg.max_temp})"
            )
        else:
            self._live.update(
                f":cross_mark: The current temperature ([bold]{msg.curr_temp}[/]) is [red bold]outside[/] the specified range ({msg.min_temp}-{msg.max_temp})"
            )

    def notify_error(self, msg: TrackerError) -> None:
        self._live.update(
            f"[red bold]An unexpected error occurred![/]\n[red]{msg.title}: [italic]{msg.description}[/]"
        )
