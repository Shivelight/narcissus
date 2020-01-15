from urllib.parse import quote

from narcissus.audio import play

GMAPS_URL = (
    "maps.googleapis.com/maps/api/staticmap?center={location}"
    "&zoom=13&scale=false&size=1200x600&maptype={maptype}"
    "&format=png&key={key}"
)


class GoogleMaps:
    def __init__(
        self, intent_mgr, api_token: str = "AIzaSyDIJ9XX2ZvRKCJcFRrl-lRanEtFUow4piM"
    ):
        self.api_token = api_token
        self.app = intent_mgr.app
        intent_mgr.register_intent("maps", self.process)

    def get_map_url(self, location, map_type="roadmap"):
        map_url = GMAPS_URL.format(
            location=location, maptype=map_type, key=self.api_token
        )
        return f"https://images.weserv.nl/?url={quote(map_url)}"

    def process(self, data):
        entities = data.entities
        location = None
        map_type = None
        if entities is not None:
            if "location" in entities:
                location = entities["location"][0]["value"]
            if "Map_Type" in entities:
                map_type = entities["Map_Type"][0]["value"]

        if location is not None:
            maps_url = self.get_map_url(location, map_type)
            self.app.mm_show_image({"url": maps_url})
            play(self.app.text_ts.synthesize(f"Sure. Here's a map of {location}."))
        else:
            self.app.mm_show_text_and_play(
                "I'm sorry, I couldn't understand what location you wanted."
            )


def setup(intent_manager):
    GoogleMaps(intent_manager)
