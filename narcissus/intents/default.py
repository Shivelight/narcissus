class Default:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("_default_", self.process)

    def process(self, data):
        self.app.mm_show_text_and_play(
            "I'm sorry, I couldn't understand what you meant by that"
        )
        return False


def setup(intent_manager):
    Default(intent_manager)
