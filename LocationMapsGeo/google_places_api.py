import requests
import json
import time
import csv

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


def print_list_to_csv(input_list, file_name):
    with open(file_name, 'w', newline="", encoding='utf-8') as result_file:
        wr = csv.writer(result_file)
        wr.writerows(input_list)


if __name__ == '__main__':
    collected_places = list()

    start_latitude = 47.339733
    end_latitude = 47.636308

    start_longitude = 18.928242
    end_longitude = 19.260952

    api = GooglePlacesAPIObj(get_api_key())

    search_types = ['restaurant', 'bakery', 'cafe']
    extended_id_list = list()
    duplications = list()

    for srch_type in search_types:
        print('Started to fetch: {}'.format(srch_type))
        places = api.search_places_by_coordinate("47.510520, 19.030952", "1000", srch_type)
        print(len(places))

        fields_to_retrieve = ['name', 'formatted_address', 'types', 'url']

        if len(places) > 0:
            for place in places:
                place_row = list()

                place_extended_id = str(place['place_id']) + srch_type

                if (extended_id_list.count(place_extended_id) == 0) or (len(extended_id_list) == 0):
                    details = api.get_place_details(place['place_id'], fields_to_retrieve)
                    extended_id_list.append(place_extended_id)

                    place_row.append(place_extended_id)
                    place_row.append(place['place_id'])

                    additional_keys_from_place = ['name', 'business_status']

                    for key in additional_keys_from_place:
                        try:
                            place_row.append(place[key])
                        except KeyError:
                            place_row.append('NotAvailable')

                    place_row.append(place['geometry']['location']['lat'])
                    place_row.append(place['geometry']['location']['lng'])
                    place_row.append(details['result']['formatted_address'])
                    place_row.append(details['result']['types'])
                    place_row.append(details['result']['url'])
                    place_row.append(srch_type)

                    old_char = ['á', 'é', 'í', 'ó', 'ö', 'ő', 'ü', 'ű', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ö', 'Ő', 'Ü', 'Ű', 'Ú']
                    new_char = ['a', 'e', 'i', 'o', 'o', 'o', 'u', 'u', 'u', 'A', 'E', 'I', 'O', 'O', 'O', 'U', 'U', 'U']

                    item_to_check = [2, 6]

                    for item in item_to_check:
                        iter_var = len(old_char)
                        for i in range(iter_var):
                            old_char_to_replace = str(old_char[i])
                            replace_to = str(new_char[i])
                            str_to_replace = str(place_row[item])
                            place_row[item] = str_to_replace.replace(old_char_to_replace, replace_to)

                    collected_places.append(place_row)
                else:
                    duplications.append(extended_id_list)

    print_list_to_csv(collected_places, 'result.csv')
    print_list_to_csv(duplications, 'duplications.csv')


