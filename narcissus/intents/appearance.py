import time


class Appearance:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("appearance", self.process)

    def process(self, data):
        self.app.mm_show_face()
        time.sleep(10)


def setup(intent_manager):
    Appearance(intent_manager)
