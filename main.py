import json
from os import environ

import googlemaps
from googlemaps.places import places_nearby

API_KEY = environ.get('API_KEY')

class GoogleMapsCityParser:
    """
    Class for parsing places in specified city
    """
    def __init__(self, api_key: str, city: str):
        self.api_key = api_key
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

    def save_to_json(self, place_type: str, json_file: str):
        """
        Save requested gym list to json file
        """
        places = self.get_city_places_by_type(place_type)
        json_places = json.dumps(places)
        
        with open(json_file, 'w') as outfile:
            print('Save requestd gym list into file {}'.format(json_file))
            json.dump(json_places, outfile)


parser = GoogleMapsCityParser(API_KEY, "Tbilisi")
parser.save_to_json("gym", 'gym_list.json')
