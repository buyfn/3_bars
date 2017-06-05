import json
import sys
import os
import math
from functools import reduce


def load_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='cp1251') as file_handler:
        return json.load(file_handler)


def print_bar(bar):
    print('Название: ' + bar['Name'])
    print('Количество мест: ' + str(bar['SeatsCount']))
    print('Адрес: ' + bar['Address'])


def get_bar_size(bar):
    return bar['SeatsCount']


def get_biggest_bar(data):
    return max(data, key=get_bar_size)


def get_smallest_bar(data):
    return min(data, key=get_bar_size)


def get_closest_bar(data, longitude, latitude):
    def closer_bar(bar1, bar2):
        dist1 = distance_between_points(latitude,
                                        longitude,
                                        float(bar1['Latitude_WGS84']),
                                        float(bar1['Longitude_WGS84']))
        dist2 = distance_between_points(latitude,
                                        longitude,
                                        float(bar2['Latitude_WGS84']),
                                        float(bar2['Longitude_WGS84']))
        return bar2 if dist2 < dist1 else bar1

    return reduce(closer_bar, data)


def distance_between_points(latitude1, longitude1, latitude2, longitude2):
    dist_y = abs(latitude2 - latitude1)
    dist_x = abs(longitude2 - longitude1)
    return math.sqrt((dist_x**2 + dist_y**2))


def get_user_coordinates():
    while True:
        latitude = input('Введи широту, на которой сейчас сидишь: ')
        longitude = input('Введи долготу, на которой сейчас сидишь: ')
        try:
            return float(latitude), float(longitude)
        except ValueError:
            print('\nНепонятные координаты. Введи еще раз, только цифрами.')


if __name__ == '__main__':
    current_directory = os.getcwd()
    try:
        path = os.path.join(current_directory, sys.argv[1])
    except IndexError:
        sys.exit('Нужно указать файл с данными о барах')

    bars = load_data(path)

    latitude, longitude = get_user_coordinates()
    closest_bar = get_closest_bar(bars, longitude, latitude)
    biggest_bar = get_biggest_bar(bars)
    smallest_bar = get_smallest_bar(bars)

    print('\nБлижайший бар')
    print_bar(closest_bar)

    print('\nСамый большой бар')
    print_bar(biggest_bar)

    print('\nСамый маленький бар')
    print_bar(smallest_bar)
