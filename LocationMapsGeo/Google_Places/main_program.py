import json
import csv
import math
from timeit import default_timer as timer
import LocationMapsGeo.Google_Places.google_places_api as google_api

CONFIG_FILE = 'config.json'


def get_api_key():
    """
    Load the API key from the config file
    :return: API key (string)
    """
    with open(CONFIG_FILE) as config_file:
        data = json.load(config_file)

    return data['google_places_api_key']


def print_list_to_csv(input_list, file_name):
    """
    print a list to a csv file
    :param input_list: list to print to a csv
    :param file_name: csv file name
    :return: None
    """
    with open(file_name, 'w', newline="", encoding='utf-8') as result_file:
        wr = csv.writer(result_file)
        wr.writerows(input_list)


def replace_hungarian_characters(input_str):
    """
    Replacing hungarian characters in a string
    :param input_str: text to search for hungarian characters
    :return: string without special hungarian characters
    """
    old_char = ['á', 'é', 'í', 'ó', 'ö', 'ő', 'ü', 'ű', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ö', 'Ő', 'Ü', 'Ű', 'Ú']
    new_char = ['a', 'e', 'i', 'o', 'o', 'o', 'u', 'u', 'u', 'A', 'E', 'I', 'O', 'O', 'O', 'U', 'U', 'U']

    iter_var = len(old_char)
    for i in range(iter_var):
        old_char_to_replace = str(old_char[i])
        replace_to = str(new_char[i])
        input_str = input_str.replace(old_char_to_replace, replace_to)

    return input_str


def calc_new_latitude(latitude, distance_in_meters):
    """
    Calculating new latitude by meter
    :param latitude: starting latitude
    :param distance_in_meters: move in meters
    :return: new latitude
    """
    earth = 6378.137  # radius of the earth in kilometer
    pi = math.pi
    m = (1 / ((2 * pi / 360) * earth)) / 1000  # 1 meter in degree

    return round(latitude + (distance_in_meters * m), 6)


def calc_new_longitude(latitude, longitude, distance_in_meters):
    """
    Calculating new longitude
    :param latitude: point latitude
    :param longitude: starting longitude
    :param distance_in_meters: move in meters
    :return: new longitude
    """
    earth = 6378.137  # radius of the earth in kilometer
    pi = math.pi
    cos = math.cos
    m = (1 / ((2 * pi / 360) * earth)) / 1000  # 1 meter in degree

    new_longitude = longitude + (distance_in_meters * m) / cos(latitude * (pi / 180))
    return round(new_longitude, 6)


def collect_place_details(place_resp, details_resp):

    details_row = list()

    details_row.append(place_resp['place_id'])

    additional_keys_from_place = ['name', 'busines+s_status']

    for key in additional_keys_from_place:
        try:
            details_row.append(replace_hungarian_characters(str(place_resp[key])))
        except KeyError:
            details_row.append('NotAvailable')

    details_row.append(place_resp['geometry']['location']['lat'])
    details_row.append(place_resp['geometry']['location']['lng'])

    details_row.append(details_resp['result']['address_components'][4]['short_name'])
    details_row.append(details_resp['result']['address_components'][3]['long_name'])
    details_row.append(replace_hungarian_characters(str(details_resp['result']['formatted_address'])))
    details_row.append(sorted(details_resp['result']['types']))
    details_row.append(details_resp['result']['url'])

    return details_row


def haversine_formula(lat1, lon1, lat2, lon2, uom):
    """
    source: https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    if uom == 'm':
        return round(c * r * 1000, 0)
    elif uom == 'km':
        return round(c*r, 2)


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

    # meters to move the search circle midpoint (move on latitude or longitude
    meters_to_increase_search = 420

    api = google_api.GooglePlacesAPIObj(get_api_key())

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

                fields_to_retrieve = ['name', 'formatted_address', 'types', 'url', 'address_component',
                                      'permanently_closed']

                if len(places) > 0:
                    for place in places:
                        place_extended_id = str(place['place_id']) + srch_type

                        if (extended_id_list.count(place_extended_id) == 0) or (len(extended_id_list) == 0):
                            details = api.get_place_details(place['place_id'], fields_to_retrieve)
                            extended_id_list.append(place_extended_id)

                            place_row = list()
                            place_row.append(place_extended_id)
                            place_row.append(srch_type)

                            place_row = collect_place_details(place, details)

                            collected_places.append(place_row)
                        else:
                            dupl_row = list()
                            dupl_row.append(place_extended_id)
                            duplications.append(dupl_row)

                    end_time = timer()
                    
                    search_param_row = [actual_latitude,
                                        actual_longitude,
                                        round(end_time - start_time, 4),
                                        srch_type]

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


