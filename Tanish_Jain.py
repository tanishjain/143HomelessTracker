import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import uszipcode

##################################  FUNCTIONS  ################################

def add_ll(project_data):
    """
    Function to geocode the dataset. Adds a zip code for each case based on coordinates.
    
    :param: project_data
    :type: pd.DataFrame
        
    :return: pd.DataFrame
    """
    assert isinstance(project_data, pd.DataFrame)
    
    search = uszipcode.SearchEngine()               #Set up SearchEngine() function from uszipcode
    location_list = list(project_data['Location'])  #Get list of each report
    longitude_list = []                             #Create list to store longitude
    latitude_list = []                              #Create list to store latitude
    zip_list = []                                   #Create list to store zip code

    #Iterate through every location and update longitude, latitude, zip code lists
    for location in location_list:
        lo = (re.findall(r"[-+]?\d*\.\d+|\d+", location))[0]    #Extract longitude from Location string
        la = (re.findall(r"[-+]?\d*\.\d+|\d+", location))[1]    #Extract latitude from Location string
        zp = search.by_coordinates(float(la), float(lo), returns=1)[0].zipcode #Get zip code for coordinate
        longitude_list.append(lo)
        latitude_list.append(la)
        zip_list.append(zp)
    
    #Add the Longitude, Latitude, Zip Code data in new columns in dataframe
    project_data.insert(len(project_data.columns)-1, "Longitude", longitude_list, True)
    project_data.insert(len(project_data.columns)-1, "Latitude", latitude_list, True)
    project_data.insert(len(project_data.columns)-1, "Zip", zip_list, True)
    
    return project_data

def create_corr_mat(data, annot_sz=30):
    """
    Plot correlation matrix for given dataset. Returns correlation matrix.
    
    :param: data
    :type: pd.DataFrame
    
    :param: annot_sz
    :type: int
    
    :return: pd.DataFrame
    """
    assert isinstance(data, pd.DataFrame)
    assert isinstance(annot_sz, int)      
    corr = data.corr()
    
    ax = plt.figure()
    ax.set_facecolor('xkcd:black')
    mat = sns.heatmap(corr, vmin=-1, vmax=1, center=0, cmap=sns.diverging_palette(20, 220, n=200), square=True, annot=True, annot_kws={"size": annot_sz})
    mat.set_xticklabels(mat.get_xticklabels(), rotation=30, horizontalalignment='right');
    mat.set_yticklabels(mat.get_yticklabels(), rotation=0, horizontalalignment='right')
    mat.tick_params(axis='x', colors='white')
    mat.tick_params(axis='y', colors='white')
    plt.show()
    
    return corr

def autolabel(rects, ax):    
    """
    Attach a text label above each bar in rects, displaying its height.
    
    :param: rects
    :type: matplotlib.container.BarContainer
    """
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords='offset points',
                     ha='center', va='bottom', color='white', size=10)

##############################################################################
#%% RUN THIS SECTION TO GEOCODE THE DATASET
project_data = pd.read_csv('Complete Dataset.csv')
project_data = add_ll(project_data)