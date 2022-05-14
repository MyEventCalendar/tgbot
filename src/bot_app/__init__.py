import logging
from . app import dp
from . import commands, all_events, delete_event, add_event, change_event

logging.basicConfig(level=logging.INFO)
