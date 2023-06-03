import json
from os import environ

import googlemaps
from google.oauth2 import service_account
from googlemaps.places import places_nearby

API_KEY = environ.get('API_KEY')


class GoogleMapsCityParser:
    """
    Class for parsing places in specified city
    """
    def __init__(self, api_key: str, city: str):
        self.api_key = api_key
        self.service_account_info = json.load(open("service_account.json"))
        self.google_credentials = service_account.Credentials.from_service_account_info(self.service_account_info)
        self.maps_client = googlemaps.Client(key=self.api_key)
        self.city = city

    def get_city_places_by_type(self, place_type: str) -> list:
        """
        Get all places in specified city by type
        :param city: city name
        :param place_type: place type
        :return: list of places
        """
        city_geocode = self.maps_client.geocode(self.city)
        if not city_geocode:
            raise Exception("City not found")
        places = places_nearby(self.maps_client, location=city_geocode[0]['geometry']['location'], radius=15_000, type=place_type)
        return places['results']

    def print_places_info(self, place_type: str):
        """
        Prints places info
        :param place_type: place type
        """
        places = self.get_city_places_by_type(place_type)
        for place in places:
            print(place['name'])
            print(place['vicinity'])
            print(place.get('rating'))
            print(place.get('user_ratings_total'))
            print("Categories:", place['types'])
            print(place.get('opening_hours'))
            print()


parser = GoogleMapsCityParser(API_KEY, "Tbilisi")
parser.print_places_info("gym")
