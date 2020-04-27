import requests
import json
import time
import csv
import math
from timeit import default_timer as timer

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


def replace_hungarian_characters(input_str):
    old_char = ['á', 'é', 'í', 'ó', 'ö', 'ő', 'ü', 'ű', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ö', 'Ő', 'Ü', 'Ű', 'Ú']
    new_char = ['a', 'e', 'i', 'o', 'o', 'o', 'u', 'u', 'u', 'A', 'E', 'I', 'O', 'O', 'O', 'U', 'U', 'U']

    iter_var = len(old_char)
    for i in range(iter_var):
        old_char_to_replace = str(old_char[i])
        replace_to = str(new_char[i])
        input_str = input_str.replace(old_char_to_replace, replace_to)

    return input_str


def calc_new_latitude(latitude, distance_in_meters):
    earth = 6378.137  # radius of the earth in kilometer
    pi = math.pi
    m = (1 / ((2 * pi / 360) * earth)) / 1000  # 1 meter in degree

    return round(latitude + (distance_in_meters * m), 6)


def calc_new_longitude(latitude, longitude, distance_in_meters):
    earth = 6378.137  # radius of the earth in kilometer
    pi = math.pi
    cos = math.cos
    m = (1 / ((2 * pi / 360) * earth)) / 1000  # 1 meter in degree

    new_longitude = longitude + (distance_in_meters * m) / cos(latitude * (pi / 180))
    return round(new_longitude, 6)


if __name__ == '__main__':
    collected_places = list()

    #start_latitude = 47.339733
    start_latitude = 47.510549
    #end_latitude = 47.636308
    end_latitude = 47.528515

    #start_longitude = 18.928242
    start_longitude = 19.030952
    #end_longitude = 19.260952
    end_longitude = 19.057551

    meters_to_increase_search = 150

    api = GooglePlacesAPIObj(get_api_key())

    search_types = ['restaurant', 'bakery', 'cafe']
    extended_id_list = list()
    duplications = list()
    search_parameters = list()

    actual_latitude = start_latitude

    prog_start = timer()

    while actual_latitude < end_latitude:

        actual_longitude = start_longitude

        while actual_longitude < end_longitude:

            for srch_type in search_types:
                start_time = timer()

                coordinates = str(actual_latitude) + ', ' + str(actual_longitude)

                print('Started to fetch: {}'.format(srch_type))
                places = api.search_places_by_coordinate(coordinates, "300", srch_type)
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

                            item_to_check = [2, 6]

                            for item in item_to_check:
                                place_row[item] = replace_hungarian_characters(str(place_row[item]))

                            collected_places.append(place_row)
                        else:
                            dupl_row = list()
                            dupl_row.append(place_extended_id)
                            duplications.append(dupl_row)

                    end_time = timer()
                    search_param_row = list()
                    search_param_row.append(actual_latitude)
                    search_param_row.append(actual_longitude)
                    search_param_row.append(round(end_time - start_time, 4))
                    search_param_row.append(srch_type)
                    search_parameters.append(search_param_row)

                    print(
                        str(actual_latitude) + '|' + str(actual_longitude) + '|' + str(round(end_time - start_time, 4)))

            actual_longitude = calc_new_longitude(actual_latitude, actual_longitude, meters_to_increase_search)

        actual_latitude = calc_new_latitude(actual_latitude, meters_to_increase_search)

    prog_end = timer()
    print_list_to_csv(collected_places, 'result.csv')
    print_list_to_csv(duplications, 'duplications.csv')
    print_list_to_csv(search_parameters, 'search_parameters.csv')
    print(round(prog_end-prog_start, 4))


