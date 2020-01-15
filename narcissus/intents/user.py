class User:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("user name", self.user_name)

    def user_name(self, data):
        self.app.mm_show_text_and_play(self.app.user_name)


def setup(intent_manager):
    User(intent_manager)
