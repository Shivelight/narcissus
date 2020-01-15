class Weather:
    def __init__(self, intent_mgr):
        self.app = intent_mgr.app
        intent_mgr.register_intent("weather", self.process)

    def process(self, data):
        greet = self.app.nlg.greet()
        self.app.mm_show_text_and_play(greet)
