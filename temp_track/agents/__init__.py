import logging
from uagents import Bureau

from .notifier import notifier as notifier_agent
from .tracker import tracker as tracker_agent

bureau = Bureau()
bureau.add(notifier_agent)
bureau.add(tracker_agent)
bureau._logger = logging.Logger("bureau-logger", logging.ERROR)
