from models.card import Card
from datetime import datetime


class Session:

    TIME_OUT_SECONDS = 60

    def __init__(self, card: Card):
        self.card = card
        self.authenticated = False
        self.wrong_pin_attempts = 0
        self.session_start_time = datetime.now()
        self.session_last_active_time = datetime.now()

    def ping(self):
        self.session_last_active_time = datetime.now()

    def is_timed_out(self):
        current_time = datetime.now()
        elapsed_time = (current_time - self.session_last_active_time).total_seconds()
        return elapsed_time > self.TIME_OUT_SECONDS
