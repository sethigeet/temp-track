from rich.text import Text
from rich.live import Live

from temp_track.messages import TrackerStatus, TrackerError
from . import NotificationProvider


class ConsoleNotificationProvider(NotificationProvider):
    _live = Live("", refresh_per_second=1)

    def __init__(self, min_temp: float, max_temp: float, loc: str) -> None:
        super().__init__(min_temp, max_temp, loc)

        self._live.start()

    def notify(self, msg: TrackerStatus) -> None:
        if msg.within_range:
            self._live.update(
                f":white_heavy_check_mark: The current temperature ([bold]{msg.curr_temp}[/]) is [green bold]within[/] the specified range ({self.min_temp}-{self.max_temp})"
            )
        else:
            self._live.update(
                f":cross_mark: The current temperature ([bold]{msg.curr_temp}[/]) is [red bold]outside[/] the specified range ({self.min_temp}-{self.max_temp})"
            )

    def notify_error(self, msg: TrackerError) -> None:
        self._live.update(
            f"[red bold]An unexpected error occurred![/]\n[red]{msg.title}: [italic]{msg.description}[/]"
        )
