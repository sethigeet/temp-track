from abc import ABC, abstractmethod

from temp_track.messages import TrackerStatus, TrackerError


class NotificationProvider(ABC):
    min_temp: float
    max_temp: float
    loc: str

    def __init__(self, min_temp: float, max_temp: float, loc: str) -> None:
        super().__init__()

        self.min_temp = min_temp
        self.max_temp = max_temp
        self.loc = loc

    @abstractmethod
    def notify(self, msg: TrackerStatus) -> None:
        pass

    @abstractmethod
    def notify_error(self, msg: TrackerError) -> None:
        pass
