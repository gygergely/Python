import requests
import json
import time

CONFIG_FILE = 'config.json'


class GooglePlacesAPIObj(object):
    def __init__(self, api_key):
        super(GooglePlacesAPIObj, self).__init__()
        self.apiKey = api_key

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places_from_api = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params=params)
        results = json.loads(res.content)
        places_from_api.extend(results['results'])

        time.sleep(2)

        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params=params)
            results = json.loads(res.content)
            places_from_api.extend(results['results'])
            time.sleep(2)
        return places_from_api

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params=params)
        place_details = json.loads(res.content)
        return place_details


def get_api_key():
    with open(CONFIG_FILE) as config_file:
        data = json.load(config_file)

    return data['google_places_api_key']


if __name__ == '__main__':
    collected_places = list()

    start_latitude = 47.339733
    end_latitude = 47.636308

    start_longitude = 18.928242
    end_longitude = 19.260952

    api = GooglePlacesAPIObj(get_api_key())

    search_types = ['restaurant', 'hotel', 'bakery', 'cafe']

    places = api.search_places_by_coordinate("47.510520, 19.030952", "1000", "lawyer")
    print(len(places))

    fields_to_retrieve = ['name', 'formatted_address', 'types', 'url']

    if len(places) > 0:
        for place in places:
            place_row = list()
            details = api.get_place_details(place['place_id'], fields_to_retrieve)

            place_row.append(place['place_id'])
            place_row.append(place['name'])
            place_row.append(place['business_status'])
            place_row.append(place['geometry']['location']['lat'])
            place_row.append(place['geometry']['location']['lng'])
            place_row.append(details['result']['formatted_address'])
            place_row.append(details['result']['types'])
            place_row.append(details['result']['url'])

            collected_places.append(place_row)

        print('')


