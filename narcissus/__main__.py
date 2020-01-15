from . import Narcissus
from .stt import GoogleRecognition


if __name__ == "__main__":
    google_stt = GoogleRecognition(debug=True)
    bot = Narcissus(stt_engine=google_stt)
    bot.start()
