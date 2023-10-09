from abc import ABC, abstractmethod

from temp_track.messages import TrackerStatus, TrackerError


class NotificationProvider(ABC):
    @abstractmethod
    def notify(self, msg: TrackerStatus) -> None:
        pass

    @abstractmethod
    def notify_error(self, msg: TrackerError) -> None:
        pass
