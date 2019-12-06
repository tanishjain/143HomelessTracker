# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 12:47:54 2019

@author: 37584
"""

import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

#########################################Functions######################################

def draw_map_y(data, year, data_name):
    """
    This function is used to draw year wise heatmap from 2008 to 2019 data

    """
    print(str(year))
    waste = []
    for i in range(len(data)):
        d = data.iloc[i]
        if d['Date'].split('-')[0] == str(year) and d['Description'] == data_name:
            waste.append({
                                    'date':d['Date'],
                                    'category' : d['Category'],
                                    'longitude' : d['Location'].split(' ')[1][1:],
                                    'latitude' : d['Location'].split(' ')[2][:-1]
                                    })
    coordinates = []
    for i in waste:
        coordinates.append([i['latitude'], i['longitude']])
    
    latitude = 37.77
    longitude = -122.42
    # Create map and display it
    san_map = folium.Map(location=[latitude, longitude],tiles='Stamen Toner', zoom_start=13)
    # Display the map of San Francisco
    # add incidents to map
    HeatMap(coordinates, radius = 14).add_to(san_map)
    san_map.save(str(year) + '_' + str(data_name) + '.html')   
    
def draw_map_m(data, month, data_name):
    """
    This function is used to draw month wise heatmap from 2008 to 2019 data

    """
    print(str(month))
    waste = []
    for i in range(len(data)):
        d = data.iloc[i]
        if d['Date'].split('-')[1] == '0' + str(month) and d['Description'] == data_name:
            waste.append({
                                    'date':d['Date'],
                                    'category' : d['Category'],
                                    'longitude' : d['Location'].split(' ')[1][1:],
                                    'latitude' : d['Location'].split(' ')[2][:-1]
                                    })
    coordinates = []
    for i in waste:
        coordinates.append([i['latitude'], i['longitude']])
       
    latitude = 37.77
    longitude = -122.42
    # Create map and display it
    san_map = folium.Map(location=[latitude, longitude],tiles='Stamen Toner', zoom_start=13)
    # Display the map of San Francisco
    # add incidents to map
    HeatMap(coordinates, radius = 14).add_to(san_map)
    san_map.save(str(month) + '_' + str(data_name) + '.html') 
    
def draw_map_m_2(data, month, data_name):
    """
    This function is used to draw year wise heatmap from 2008 to 2019 data

    """
    print(str(month))
    waste = []
    for i in range(len(data)):
        d = data.iloc[i]
        if d['Date'].split('-')[1] == str(month) and d['Description'] == data_name:
            waste.append({
                                    'date':d['Date'],
                                    'category' : d['Category'],
                                    'longitude' : d['Location'].split(' ')[1][1:],
                                    'latitude' : d['Location'].split(' ')[2][:-1]
                                    })
    coordinates = []
    for i in waste:
        coordinates.append([i['latitude'], i['longitude']])
       
    latitude = 37.77
    longitude = -122.42
    # Create map and display it
    san_map = folium.Map(location=[latitude, longitude],tiles='Stamen Toner', zoom_start=13)
    # Display the map of San Francisco
    # add incidents to map
    HeatMap(coordinates, radius = 14).add_to(san_map)
    san_map.save(str(month) + '_' + str(data_name) + '.html') 


def heatmap_drawer(fname, month_or_year, waste_or_encamp):
    """
    This function is used to draw the heatmap according to year or month
    You can choose to draw the heatmap using human waste data or encamp data
    :param fname: file name to use
    :type fname: str
    :param month_or_year: month wise or year wise
    :type month_or_year: str ---'M' or 'Y'
    :param waste_or_encamp: use which data to draw
    :type waste_or_encamp: str --- 'W' or 'E'
    :return: html files
    """
    assert isinstance(fname, str)
    assert isinstance(month_or_year, str)
    assert isinstance(waste_or_encamp, str)
    assert fname[-4:] == '.csv'
    assert month_or_year == 'M' or month_or_year == 'Y'
    assert waste_or_encamp == 'W' or waste_or_encamp == 'E'
    
    data = pd.read_csv(fname)
    
    if month_or_year == 'Y':
        if waste_or_encamp == 'E':
            for i in range(2008, 2020):
                draw_map_y(data, i, 'Encampment Reports')
        elif waste_or_encamp == 'W':
            for i in range(2008, 2020):
                draw_map_y(data, i, 'Human or Animal Waste')
    elif month_or_year == 'M':
        if waste_or_encamp == 'E':
            for i in range(1, 10):
                draw_map_m(data, i, 'Encampment Reports')
            for i in range(10, 13):
                draw_map_m_2(data, i, 'Encampment Reports')
        elif waste_or_encamp == 'W':
            for i in range(1, 10):
                draw_map_m(data, i, 'Human or Animal Waste')
            for i in range(10, 13):
                draw_map_m_2(data, i, 'Human or Animal Waste')
