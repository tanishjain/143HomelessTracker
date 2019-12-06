import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import uszipcode

#%%
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

def autolabel(rects):
     #“”"Attach a text label above each bar in *rects*, displaying its height.“”"
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

#%% RUN THIS SECTION FOR GEOCODED DATASET
project_data = pd.read_csv('Full Dataset.csv')
toilet_data = pd.read_csv('public_restrooms_sf.csv')
crime_data = pd.read_csv('Police Dataset2.csv')

#%% Correlation between Homeless Reports and Toilets by Zip Code
homeless_reports = project_data.groupby('Zip')['Latitude'].count().to_frame()
toilet_data = toilet_data.groupby('zip')['location'].count().to_frame()

num_toilets = []

for zipcode in list(homeless_reports.index):   
    try:
        num_toilets.append(toilet_data.loc[int(zipcode)][0])
    except:
        num_toilets.append(0)

homeless_reports = homeless_reports.rename(columns={'Latitude':'Incident Count'})
homeless_reports.insert(len(homeless_reports.columns), "Toilet Count", num_toilets, True)

#Create correlation matrix for each variable (occurence by zip code)
create_corr_mat(homeless_reports)

#%% Correlation between Human Waste and general Homeless Reports
other_reports = project_data[project_data['Description'] != 'Human or Animal Waste']
poop_reports = project_data[project_data['Description'] == 'Human or Animal Waste']

other_reports = other_reports.groupby('Zip').count()
poop_reports = poop_reports.groupby('Zip').count()
other_reports.insert(0, "Waste Reports", poop_reports.Category, True)
all_reports = other_reports[['Waste Reports','Date']]
all_reports = all_reports.rename(columns={'Date':'Homeless Reports'})

#Create correlation matrix for each variable (occurence by zip code)
create_corr_mat(all_reports)

#%%

#Split the dataset by the category of report (variable) (occurence by zip code)
cat0 = project_data[project_data['Description'] == 'Human or Animal Waste'].groupby('Zip').count()
cat1 = project_data[project_data['Description'] == 'CIVIL SIDEWALKS, CITATION'].groupby('Zip').count()
cat2 = project_data[project_data['Description'] == 'Encampment Reports'].groupby('Zip').count()
cat3 = project_data[project_data['Description'] == 'Encampment items'].groupby('Zip').count()
cat4 = project_data[project_data['Description'] == 'Individual Concerns'].groupby('Zip').count()
cat5 = project_data[project_data['Description'] == 'LODGING WITHOUT PERMISSION'].groupby('Zip').count()
cat6 = project_data[project_data['Description'] == 'Loitering'].groupby('Zip').count()
cat7 = project_data[project_data['Description'] == 'OBSTRUCTING HEALTH FACILITY, PLACE OF WORSHIP, OR SCHOOL'].groupby('Zip').count()
cat8 = project_data[project_data['Description'] == 'Other'].groupby('Zip').count()

#Create dataset with each variable (occurence by zip code)
cat8.insert(0, 'Waste Reports', cat0.Category, True)
cat8.insert(0, 'Civil Sidewalks Citation', cat1.Category, True)
cat8.insert(0, 'Encampment Reports', cat2.Category, True)
cat8.insert(0, 'Encampment items', cat3.Category, True)
cat8.insert(0, 'Individual Concerns', cat4.Category, True)
cat8.insert(0, 'Lodging without Permission', cat5.Category, True)
cat8.insert(0, 'Loitering', cat6.Category, True)
cat8.insert(0, 'Obstruction', cat7.Category, True)
cat8 = cat8.rename(columns={'Category':'Other'})
all_reports = cat8[['Waste Reports','Civil Sidewalks Citation','Encampment Reports','Encampment items','Individual Concerns','Lodging without Permission','Loitering','Obstruction','Other']]

#Create correlation matrix for each variable (occurence by zip code)
create_corr_mat(all_reports)

#%%

crime_reports = crime_data.groupby('Zip').count()
homeless_reports = project_data.groupby('Zip').count()
crime_reports = crime_reports.rename(columns={'Category':'Crime Reports'})
crime_reports.insert(0, 'Homeless Reports', homeless_reports.Category, True)
crime_reports = crime_reports[['Homeless Reports','Crime Reports']]

#Create correlation matrix for each variable (occurence by zip code)
create_corr_mat(crime_reports)

#%%
# https://sfgov.org/scorecards/safety-net/homeless-population

'''

Data from https://sfgov.org/scorecards/safety-net/homeless-population
'''

#Data
years = range(2005,2020,2)
population = [5404, 5703, 5823, 5669, 7008, 6775, 6858, 8011]

x = np.arange(len(years))   #labels for x axis
width = 0.8                 #width of the bars
fig, ax = plt.subplots(facecolor='black', figsize=(5,10))
rects1 = ax.bar(x - width / 2, population, width, color='#37C9EF', alpha=.8)

ax.set_ylabel('Homeless Count', size=30)
ax.set_xlabel('Years', size=30)
ax.set_xticks(x)
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='y', labelcolor='white')
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.set_facecolor('black')

autolabel(rects1)