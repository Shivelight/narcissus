import random
import datetime

from simplenlg import (
    NPPhraseSpec,
    PPPhraseSpec,
    SPhraseSpec,
    InterrogativeType,
    Realiser,
    Tense,
)


class NaturalLanguageGenerator:

    def __init__(self, user_name=None):
        self.user_name = user_name

        # make random more random by seeding with time
        random.seed(datetime.datetime.now())

    def acknowledge(self):

        user_name = self.user_name
        if user_name is None:
            user_name = ""

        simple_acknoledgement = ["Yes?", "What can I do for you?", "How can I help?"]

        personal_acknowledgement = [
            "How can I help you today, %s" % user_name,
            "How can I help you, %s" % user_name,
            "What can I do for you, %s" % user_name,
            "Hi %s, what can I do for you?" % user_name,
            "Hey %s, what can I do for you?" % user_name,
        ]

        choice = 0
        if self.user_name is not None:
            choice = random.randint(0, 2)
        else:
            choice = random.randint(0, 1)

        ret_phrase = ""

        if choice == 0:
            ret_phrase = random.choice(simple_acknoledgement)
        elif choice == 1:
            date = datetime.datetime.now()
            ret_phrase = "Good %s. What can I do for you?" % self.time_of_day(date)
        else:
            ret_phrase = random.choice(personal_acknowledgement)

        return ret_phrase

    def searching(self):
        searching_phrases = ["I'll see what I can find"]

        return random.choice(searching_phrases)

    def user_status(self, type="positive", attribute=None):

        ret_phrase = ""

        positive_complements = ["good", "nice", "great", "perfect", "Beautiful"]

        negative_complements = ["bad", "terrible"]

        moderate_complements = ["alright", "okay"]

        complement_choice = positive_complements
        if type == "negative":
            complement_choice = negative_complements
        elif type == "moderate":
            complement_choice = moderate_complements

        if attribute is None:
            ret_phrase = "You look %s" % random.choice(complement_choice)
        else:
            ret_phrase = self.generate(
                "none",
                {
                    "subject": "Your %s" % attribute,
                    "verb": "look %s" % random.choice(complement_choice),
                },
                "present",
            )

        return ret_phrase

    def news(self, tense):

        headlines_nouns = [
            "stories",
            "articles",
            "headlines",
        ]

        headlines_adjectives = [["these"], ["some"], ["a", "few"], ["a", "couple"]]

        headlines_prepmodifiers = ["you"]

        choice = random.randint(0, 1)

        if choice == 1:
            ret_phrase = self.generate(
                "none",
                {
                    "subject": "I",
                    "object": random.choice(headlines_nouns),
                    "verb": "find",
                    "objmodifiers": random.choice(headlines_adjectives),
                    "preposition": "for",
                    "prepmodifiers": [random.choice(headlines_prepmodifiers)],
                },
                tense,
            )
        else:
            ret_phrase = self.generate(
                "none",
                {
                    "subject": "I",
                    "object": random.choice(headlines_nouns),
                    "verb": "find",
                    "objmodifiers": random.choice(headlines_adjectives),
                },
                tense,
            )

        return ret_phrase

    def article_interest(self, article_titles):
        ret_phrase = None

        if (
            random.randint(0, 2) == 0
        ):  # 1 in 3 chance the bot will express interest in a random article
            if article_titles is not None:
                article = random.choice(article_titles)
                article = article.rsplit("-", 1)[0]
                ret_phrase = "%s sounds particularly interesting" % article

        return ret_phrase

    def insult(self):
        return (
            "That's not very nice. Talk to me again when you have fixed your attitude"
        )

    def greet(self):
        """
        Creates a greeting phrase.
        :return:
        """

        greeting_words = ["Hi", "Hey", "Hello"]

        goofy_greetings = [
            "what's up?",
            "howdy",
            "what's crackin'?",
            "top of the morning to ya",
        ]

        choice = random.randint(0, 4)
        ret_phrase = ""

        if (choice == 0) or (choice == 3):  # time related
            ret_phrase = "Good %s" % self.time_of_day(datetime.datetime.now())
            if self.user_name is not None:
                if random.randint(0, 1) == 0:
                    ret_phrase = "%s %s" % (ret_phrase, self.user_name)
        elif (choice == 1) or (choice == 4):  # standard greeting
            ret_phrase = random.choice(greeting_words)
            if self.user_name is not None:
                if random.randint(0, 1) == 0:
                    ret_phrase = "%s %s" % (ret_phrase, self.user_name)
        elif choice == 2:  # goofy greeting
            ret_phrase = random.choice(goofy_greetings)

        return ret_phrase

    def weather(self, temperature, date, tense):
        """
        Generates a statement about the current weather.
        :param temperature:
        :param date:
        :param tense:
        :return:
        """

        ret_phrase = self.generate(
            "none",
            {
                "subject": "the temperature",
                "object": "%d degrees" % temperature,
                "verb": "is",
                "adverbs": ["%s" % self.time_of_day(date, with_adjective=True)],
            },
            tense,
        )
        return ret_phrase

    def forecast(self, forecast_obj):

        ret_phrase = ""
        forecast = ""

        if forecast_obj.get("forecast") is None:
            return ret_phrase
        else:
            forecast = forecast_obj.get("forecast")

        forecast_current = [
            "Currently, it's",
            "Right now, it's",
            "At the moment, it's",
            "It's",
            "It is",
        ]

        forecast_hourly = ["It's", "It will be", "Looks like it will be"]

        forecast_daily = [""]

        if forecast_obj.get("forecast_type") == "current":
            ret_phrase = "%s %s" % (random.choice(forecast_current), forecast)
        elif forecast_obj.get("forecast_type") == "hourly":
            ret_phrase = "%s %s" % (random.choice(forecast_hourly), forecast)
        elif forecast_obj.get("forecast_type") == "daily":
            ret_phrase = "%s %s" % (random.choice(forecast_daily), forecast)

        return ret_phrase

    def holiday(self, holiday_name):
        phrases = ["", "Looks like the next holiday is ", "The next important day is "]

        return "%s%s" % (random.choice(phrases), holiday_name)

    def meaning_of_life(self):
        phrases = ["42", "The meaning of life, the universe, and everything else is 42"]

        return random.choice(phrases)

    def name(self):
        return self.user_name

    def time_of_day(self, date, with_adjective=False):
        ret_phrase = ""
        if date.hour < 10:
            ret_phrase = "morning"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)
        elif (date.hour >= 10) and (date.hour < 18):
            ret_phrase = "afternoon"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)
        elif date.hour >= 18:
            ret_phrase = "evening"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)

        return ret_phrase

    def generate(self, utter_type, keywords, tense=None):
        """
        Input: a type of inquiry to create and a dictionary of keywords.
        Types of inquiries include 'what', 'who', 'where', 'why', 'how',
        and 'yes/no' questions. Alternatively, 'none' can be specified to
        generate a declarative statement.

        The dictionary is essentially divided into three core parts: the
        subject, the verb, and the object. Modifiers can be specified to these
        parts (adverbs, adjectives, etc). Additionally, an optional
        prepositional phrase can be specified.

        Example:

        nlg = NaturalLanguageGenerator(logging.getLogger())
        words = {'subject': 'you',
                 'verb': 'prefer',
                 'object': 'recipes',
                 'preposition': 'that contains',
                 'objmodifiers': ['Thai'],
                 'prepmodifiers': ['potatoes', 'celery', 'carrots'],
                 'adverbs': ['confidently'],
        }

        nlg.generate('yes_no', words)
        u'Do you confidently prefer Thai recipes that contains potatoes, celery and carrots?'
        nlg.generate('how', words)
        u'How do you confidently prefer Thai recipes that contains potatoes, celery and carrots?'
        """
        utterance = SPhraseSpec()
        subject = NPPhraseSpec(keywords["subject"])
        target = None
        if "object" in keywords:
            target = NPPhraseSpec(keywords["object"])
        preposition = PPPhraseSpec()

        if "preposition" in keywords:
            preposition.setPreposition(keywords["preposition"])

        if "prepmodifiers" in keywords:
            for modifier in keywords["prepmodifiers"]:
                preposition.addComplement(modifier)

        if "submodifiers" in keywords:
            for modifier in keywords["submodifiers"]:
                subject.addModifier(modifier)

        if "objmodifiers" in keywords:
            for modifier in keywords["objmodifiers"]:
                target.addModifier(modifier)

        if utter_type.lower() == "yes_no":
            utterance.setInterrogative(InterrogativeType.YES_NO)
        elif utter_type.lower() == "how":
            utterance.setInterrogative(InterrogativeType.HOW)
        elif utter_type.lower() == "what":
            utterance.setInterrogative(InterrogativeType.WHAT)
        elif utter_type.lower() == "where":
            utterance.setInterrogative(InterrogativeType.WHERE)
        elif utter_type.lower() == "who":
            utterance.setInterrogative(InterrogativeType.WHO)
        elif utter_type.lower() == "why":
            utterance.setInterrogative(InterrogativeType.WHY)

        if target is not None:
            target.addModifier(preposition)
        utterance.setSubject(subject)
        utterance.setVerb(keywords["verb"])
        if "adverbs" in keywords:
            for modifier in keywords["adverbs"]:
                utterance.addModifier(modifier)
        if target is not None:
            utterance.addComplement(target)

        if tense.lower() == "future":
            utterance.setTense(Tense.FUTURE)
        elif tense.lower() == "past":
            utterance.setTense(Tense.PAST)

        realiser = Realiser()
        output = realiser.realiseDocument(utterance).strip()
        return output
