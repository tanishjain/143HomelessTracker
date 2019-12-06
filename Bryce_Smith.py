import pandas as pd
import numpy as np
import os
import re
import uszipcode
import time
import matplotlib.pyplot as plt

def add_ll(fname):
    '''
    This function add Longitude and Latitude columns to the file from the Location column
    :param fname: file name
    :return: geocoded file
    '''
    # from file
    project_data = pd.read_csv(fname)
    assert isinstance(project_data, pd.DataFrame)

    search = uszipcode.SearchEngine()
    location_list = list(project_data['Location'])
    longitude_list = []
    latitude_list = []
    zip_list = []

    count = 0
    mult = 1
    tracker = round(len(location_list)/100)
    start = time.time()
    print("Timing has begun")
    for location in location_list:
        count+=1
        if count == tracker:
            count = 0
            print('%d%s Finished'%(mult, '%'))
            end = time.time()
            print('Time Elapsed %d minutes' % ((end - start) / 60))
            mult +=1
        lo = (re.findall(r"[-+]?\d*\.\d+|\d+", location))[0]
        la = (re.findall(r"[-+]?\d*\.\d+|\d+", location))[1]

        if (-122.468939 <= float(lo) <= -122.415459) and (37.708131 <= float(la) <= 37.9):
            zp = search.by_coordinates(float(la), float(lo), returns=1)[0].zipcode
            # print(zp)
        else:
            zp = '' # get rid of values outside of our range

        longitude_list.append(lo)
        latitude_list.append(la)
        zip_list.append(zp)
    # print('Ended for loop')

    project_data.insert(len(project_data.columns) - 1, "Longitude", longitude_list, True)
    project_data.insert(len(project_data.columns) - 1, "Latitude", latitude_list, True)
    project_data.insert(len(project_data.columns) - 1, "Zip", zip_list, True)
    project_data.replace('', np.nan, inplace=True)  # replace empty cells with NaN
    project_data.dropna(inplace=True)  # drop rows with NaN

    # from file
    dir_path = os.path.dirname(os.path.realpath(fname))
    project_data.to_csv('%s/Geocoded_%s' % (dir_path, fname), index=None, header=True)

    print('Longitude, Latitude and zip codes have been added to %s'%fname)
    return project_data











def homeless_data_cleaner(fname, cols, data, keep_other_data = False):
    '''
    This function takes in a csv file, the columns we want to keep, the data in those columns, and then saves them
    to a csv file

    :param fname: name of input file
    :type fname: str

    :param cols: list of the 4 columns to keep from the original file in format: (date, category, description, location)
    :type cols: list of strings

    :param data: data to look for in those cols (homeless, loitering, etc)
    :type data: list of strings

    :param keep_other_data: determines if we want to keep the data that was removed in a separate file
    :type keep_other_data: bool

    :return: cleaned csv, and if keep_other_data is true another complimentary cleaned file
    '''
    assert isinstance(fname, str)
    assert isinstance(cols, list)
    assert all(isinstance(i, str) for i in cols)
    assert len(cols) == 4
    assert isinstance(data, list)
    assert all(isinstance(i, str) for i in data)
    assert len(data) > 0

    df = pd.read_csv(fname, usecols=cols)
    assert isinstance(df, pd.DataFrame)
    df = df[cols]


    if keep_other_data == True: # if we want to keep the discarded data
        data_not_homeless = []
        values = list(df[cols[1]].unique())
        values.append(list(df[cols[2]].unique()))
        # print(values)
        for i in values:    # grab non-homeless values
            if i in data:
                continue
            else:
                data_not_homeless.append(i)
        clean3 = df[df[cols[1]].isin(data_not_homeless)]  # catagory checked against the data we are looking for
        clean4 = df[df[cols[2]].isin(data_not_homeless)]  # descripiton checked against the data we are looking for
        combined_rows2 = pd.concat([clean3, clean4])  # combine all rows with relevant data
        combined_rows2 = pd.DataFrame.drop_duplicates(combined_rows2)  # drop duplicates
        combined_rows2.replace('POINT (0 0)', '', inplace=True)  # replace wrong data with empty cell
        combined_rows2.replace('POINT(-120.5 90)', '', inplace=True)  # replace wrong data with empty cell
        combined_rows2.replace('', np.nan, inplace=True)  # replace empty cells with NaN
        combined_rows2.dropna(subset=cols, inplace=True)  # drop rows with NaN
        # format all columns to have the same headers
        combined_rows2.columns = ['Date', 'Category', 'Description', 'Location']

        # format the dates
        combined_rows2['Date'] = pd.to_datetime(combined_rows2['Date'], yearfirst=True).dt.date

        # write our csv file
        dir_path = os.path.dirname(os.path.realpath(fname))
        export_csv2 = combined_rows2.to_csv('%s/Cleaned_Not_Homeless_%s' % (dir_path, fname), index=None, header=True)
        # print(data_not_homeless)



    # keep only the rows with the data we are looking for
    clean1 = df[df[cols[1]].isin(data)] # catagory checked against the data we are looking for
    clean2 = df[df[cols[2]].isin(data)]    # descripiton checked against the data we are looking for

    combined_rows = pd.concat([clean1, clean2])  # combine all rows with relevant data
    combined_rows = pd.DataFrame.drop_duplicates(combined_rows)    # drop duplicates

    # format all columns to have the same headers
    new_cols = ['Date', 'Category', 'Description', 'Location']
    combined_rows.columns = new_cols

    # remove rows with empty cells
    combined_rows.replace('POINT (0 0)', '', inplace=True)  # replace empty cells with NaN
    combined_rows.replace('POINT(-120.5 90)', '', inplace=True)  # replace empty cells with NaN
    combined_rows.replace('', np.nan, inplace=True)    # replace empty cells with NaN
    combined_rows.dropna(subset=new_cols, inplace=True)    # drop rows with NaN

    # format the dates
    combined_rows['Date'] = pd.to_datetime(combined_rows['Date'], yearfirst=True).dt.date

    # write our csv file
    dir_path = os.path.dirname(os.path.realpath(fname))
    export_csv = combined_rows.to_csv ('%s/Cleaned_%s'%(dir_path, fname), index = None, header=True)

    if keep_other_data == True:
        return export_csv, export_csv2, print('%s has been cleaned' % (fname))
    else:
        return export_csv, print('%s has been cleaned' % (fname))



####################################### Load Files ####################################################
# # file 1
# homeless_data_cleaner("Police_Department_Incident_Reports__2018_to_Present.csv",
#                       ['Incident Date', 'Incident Description','Incident Subcategory', 'point'],
#                       ['Lodging Without Permission', 'Civil Sidewalks, Citation', 'Civil Sidewalks, Warning'
#                           ,'Loitering', 'Obstructing Health Facility, Place of Worship, or School',
#                        'Civil Sidewalks, Violation', 'Lodging in Park', 'Civil Sidewalks, Booking'],
#                       keep_other_data=True)
#
# # file 2
# # columns in this file are uppercase:
# colum = ['Lodging Without Permission', 'Civil Sidewalks, Citation', 'Civil Sidewalks, Warning'
#                           ,'Loitering', 'Obstructing Health Facility, Place of Worship, or School',
#                        'Civil Sidewalks, Violation', 'Lodging in Park', 'Civil Sidewalks, Booking']
# for i in range(len(colum)): colum[i] = colum[i].upper()
# homeless_data_cleaner("Police_Department_Incident_Reports__Historical_2003_to_May_2018.csv",
#                       ['Date', 'Category', 'Descript', 'Location'], colum,
#                       keep_other_data=True)
#
# # file 3
# homeless_data_cleaner('311_Cases.csv', ['Opened','Category', 'Request Type', 'Point'],
#                       ['Encampments', 'Human or Animal Waste', 'Homeless Concerns'])










def file_combiner(fnames, fout):
    '''
    this function combines csv files
    :param fnames: names of files to be combined
    :type fnames: list of str
    :param fout: name of output file
    :type fout: str
    :return: combined files
    '''
    assert isinstance(fnames, list)
    assert all(isinstance(i, str) for i in fnames)
    assert isinstance(fout, str)

    # combine all cleaned files
    combined_csv = pd.concat([pd.read_csv(f) for f in fnames])
    combined_csv = pd.DataFrame.drop_duplicates(combined_csv)  # drop duplicates

    # export to csv
    return combined_csv.to_csv("%s"%fout, index=False, encoding='utf-8-sig'), print('Files Combined')


######################################## Files to Combine #########################################################
# combine all files in the list
all_homeless_filenames = ['Geocoded_Cleaned_311_Cases.csv',
                          'Geocoded_Cleaned_Police_Department_Incident_Reports__2018_to_Present.csv',
                          'Geocoded_Cleaned_Police_Department_Incident_Reports__Historical_2003_to_May_2018.csv']
not_homeless_police_reports = ['Geocoded_Cleaned_Not_Homeless_Police_Department_Incident_Reports__2018_to_Present.csv',
                          'Geocoded_Cleaned_Not_Homeless_Police_Department_Incident_Reports__Historical_2003_to_May_2018.csv']
homeless_police_reports = ['Geocoded_Cleaned_Police_Department_Incident_Reports__Historical_2003_to_May_2018.csv',
                           'Geocoded_Cleaned_Police_Department_Incident_Reports__2018_to_Present.csv']

# file_combiner(homeless_police_reports, 'Complete_Geocoded_Homeless_Police_Reports.csv')
# file_combiner(not_homeless_police_reports, 'Complete_Geocoded_Non_homeless_Police_reports.csv')
# file_combiner(all_homeless_filenames, 'Complete_Geocoded_Homeless_Related_Data.csv')


############################# Add Latitude Longitude and Zipcodes ################################################
# add zip codes, latitude, and longitude
# add_ll('Cleaned_Police_Department_Incident_Reports__2018_to_Present.csv')
# add_ll('Cleaned_Not_Homeless_Police_Department_Incident_Reports__Historical_2003_to_May_2018.csv')
# add_ll('Cleaned_311_Cases.csv')



######################################## Variable Checks ############################################################
# df = pd.read_csv('Complete Dataset.csv')
# print(df['Description'].unique())
# print(df['Category'].unique())
# print(df['Category'].value_counts())
# print(df['Description'].value_counts())











def scatter_plot(fnames, cols):
    '''
    This function takes in two variables from two files and plots them against each other
    for instance, if you have homeless and non-homeless data, and the columns location and date
    it will plot date and location on the x and y axis, with homeless in blue, and the non-homeless data in
    white. The plots will also be sized according to the number of points in that spot
    :param fname: file names to use
    :type fname: list of str
    :param cols: columns to plot
    :type cols: list of str
    :return: color coded scatter plot of data
    '''
    assert isinstance(fnames, list)
    assert all(isinstance(i, str) for i in fnames)
    assert isinstance(cols, list)
    assert all(isinstance(i, str) for i in cols)
    assert len(fnames) == 2
    assert len(cols) == 2

    project_data1 = pd.read_csv(fnames[0], usecols=cols)  # non homeless
    project_data2 = pd.read_csv(fnames[1], usecols=cols)

    assert isinstance(project_data1, pd.DataFrame)
    assert isinstance(project_data2, pd.DataFrame)

    # add months and years columns
    project_data1['month'] = pd.DatetimeIndex(project_data1[cols[0]]).month
    project_data2['month'] = pd.DatetimeIndex(project_data2[cols[0]]).month
    project_data1['year'] = pd.DatetimeIndex(project_data1[cols[0]]).year
    project_data2['year'] = pd.DatetimeIndex(project_data2[cols[0]]).year
    # print(project_data1)

    # FULL DATES #####################
    count1_date = project_data1[cols[0]].value_counts()
    count1_labels = project_data1[cols[0]].value_counts().index.tolist()
    count2_date = project_data2[cols[0]].value_counts()
    count2_labels = project_data2[cols[0]].value_counts().index.tolist()
    # print(count1_date)
    # # print(count2_labels)

    # MONTHS #######################
    month1 = project_data1['month'].value_counts()
    month2 = project_data2['month'].value_counts()
    months = project_data2['month'].value_counts().index.tolist()
    months.sort()
    # print(months)
    months_cat = pd.CategoricalDtype(categories=months, ordered=True)
    month1.astype(months_cat)
    month2.astype(months_cat)
    # print(month1)

    # YEAR ########################
    year1 = project_data1['year'].value_counts()
    year2 = project_data2['year'].value_counts()
    norm_year1 = year1/sum(year1)
    norm_year2 = year2 / sum(year2)
    # print(norm_year1)
    years = project_data2['year'].value_counts().index.tolist()
    years.sort()
    # print(years)
    years_cat = pd.CategoricalDtype(categories=years, ordered=True)
    year1.astype(years_cat)
    year2.astype(years_cat)
    years_avg = (year2/(year1+year2))*100 # homeless/ non-homeless *100 = % of homeless
    print(years_avg)

    # Locations by zipcode #############################
    count1_location = project_data1[cols[1]].value_counts() # normaliza? ->round( /100)
    count2_location = project_data2[cols[1]].value_counts()
    location1_norm = count1_location/sum(count1_location)
    location2_norm = count2_location/sum(count2_location)
    # print(location1_norm)
    # print(location2_norm)

    # dates now contains a sorted list of dates
    dates1 = project_data1[cols[0]]
    dates2 = project_data2[cols[0]]
    dates = pd.concat([dates1, dates2])  # combine all rows with relevant data
    dates = list(dates.unique())
    dates.sort()
    # print(dates)

    # zips now contains a sorted list of zip codes
    zips1 = project_data1[cols[1]]
    zips2 = project_data2[cols[1]]
    zips = pd.concat([zips1, zips2])  # combine all rows with relevant data
    zips = list(zips.unique())
    zips.sort()
    # print(zips)

    # order locations and dates
    dates_cat = pd.CategoricalDtype(categories=dates, ordered=True)
    zips_cat = pd.CategoricalDtype(categories=zips, ordered=True)
    count1_date.astype(dates_cat)
    count2_date.astype(dates_cat)
    count1_location.astype(zips_cat)
    count2_location.astype(zips_cat)
    # print(count1_date)
    # print(count2_date)
    # print(count1_location)

    # FULL DATE ############################
    combined_dates = pd.DataFrame(data={'Homeless Crime': count2_date, 'Non-Homeless Crime': count1_date, 'Dates': dates})
    # combined_dates = combined_dates.set_index('Dates')
    # combined_dates.fillna(0, inplace=True)
    combined_dates.replace(0, np.nan, inplace=True)  # replace empty cells with NaN   # use only zips with both values
    combined_dates.dropna(inplace=True)  # drop rows with NaN
    # print(combined_dates.to_string())

    # MONTH ######################################
    combined_months = pd.DataFrame(data={'Homeless Crime': month2, 'Non-Homeless Crime': month1, 'Month': months})
    combined_months = combined_months.set_index('Month')
    # combined_months.fillna(0, inplace=True)
    # combined_months.replace(0, np.nan, inplace=True)  # replace empty cells with NaN   # use only zips with both values
    # combined_months.dropna(inplace=True)  # drop rows with NaN
    # print(combined_months)
    # print(combined_months.to_string())

    # YEAR #######################################
    combined_years = pd.DataFrame(data={'Homeless Reports':year2, 'Non-Homeless Crime': year1, 'Year': years})
    # combined_years.fillna(0, inplace=True)
    combined_years.replace(2018, np.nan, inplace=True)  # replace empty cells with NaN   # use only zips with both values
    combined_years.replace(2019, np.nan, inplace=True)  # replace empty cells with NaN   # use only zips with both values
    combined_years.dropna(inplace=True)  # drop rows with NaN
    combined_years['Year']= combined_years['Year'].astype(int)
    # combined_years['Non-Homeless Crime'] = combined_years['Non-Homeless Crime'].astype(int)
    # combined_years = combined_years.set_index('Year')
    print(combined_years)
    # print(combined_years.to_string())

    # Year Avg ########################################
    yearly_avg = pd.DataFrame(data={'% of Crime Related to Homelessness': years_avg,'Homeless Reports': year2, 'Year': years})
    yearly_avg.replace(2018, np.nan, inplace=True)  # replace empty cells with NaN   # use only zips with both values
    yearly_avg.replace(2019, np.nan, inplace=True)  # replace empty cells with NaN   # use only zips with both values
    yearly_avg.dropna(inplace=True)  # drop rows with NaN
    yearly_avg['Year']= yearly_avg['Year'].astype(int)
    # combined_years['Non-Homeless'] = combined_years['Non-Homeless'].astype(int)
    # yearly_avg = yearly_avg.set_index('Year')
    # print(yearly_avg)

    # LOCATION ############################################
    combined_locations = pd.DataFrame(data={'Homeless Report': count2_location,
                                            'Non-Homeless Crime': count1_location,
                                            'Zipcode': zips})
    # combined_locations = combined_locations.set_index('Zipcode')
    combined_locations.fillna(0, inplace=True)
    # combined_locations['Homeless Report']= combined_locations['Homeless Report'].astype(int)
    # combined_locations.replace(0, np.nan, inplace=True)  # replace empty cells with NaN   # use only zips with both values
    # combined_locations.dropna(inplace=True)  # drop rows with NaN
    # print(combined_locations)



    # BOOLS? ###################################################
    #----------------location----------
    homeless_loc = pd.DataFrame(data={'Report': count2_location, 'Homeless Related': True})

    non_homeless_loc = pd.DataFrame(data={'Report': count1_location, 'Homeless Related': False})
    # print(non_homeless)
    loc_set = pd.concat([homeless_loc, non_homeless_loc])
    # print(loc_set)
    loc_list = loc_set.index.tolist()
    loc_set = pd.DataFrame(
        data={'Number of Events': loc_set['Report'], 'Homeless Related': loc_set['Homeless Related'], 'Location': loc_list})
    combined_locations.fillna(0, inplace=True)
    combined_locations['Homeless Report']= combined_locations['Homeless Report'].astype(int)
    # print(loc_set)

    #--------------- years-----------
    homeless = pd.DataFrame(data={'Crime': year2, 'Homeless Related': True})
    homeless.astype(years_cat)
    non_homeless = pd.DataFrame(data={'Crime': year1, 'Homeless Related': False})
    non_homeless.astype(years_cat)
    # print(non_homeless)
    year_set = pd.concat([homeless, non_homeless])
    # print(year_set)
    year_index = year_set.index.tolist()
    year_set = pd.DataFrame(data={'Events': year_set['Crime'], 'Homeless Related': year_set['Homeless Related'], 'Year':year_index})
    year_set.replace(2018, np.nan, inplace=True)  # use only years we want
    year_set.replace(2019, np.nan, inplace=True)  #  use only years we want
    year_set.dropna(inplace=True)  # drop rows with NaN
    year_set['Year']= year_set['Year'].astype(int)
    # print(year_set)


    # Bar Graph:
    # ax = plt.gca()
    # combined_locations.plot(kind='bar', x='Zipcode', y='Non-Homeless', color='blue', ax=ax)
    # combined_locations.plot(kind='bar', x='Zipcode', y='Homeless', color='red', ax=ax)

    ## LmPlot
    # sns.lmplot('Zipcode', 'Homeless', data=combined_locations, fit_reg=False)
    # sns.lmplot('Zipcode', 'Non-Homeless', data=combined_locations, fit_reg=False, color='red')

    # # Heatmap
    # corr = combined_locations.corr()
    # sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns,
    #             cmap=sns.diverging_palette(220, 10, as_cmap=True))

    # Pairpliots
    # sns.pairplot(combined_locations)


    # # bar(h) graph
    # alternative_method = combined_locations.merge(combined_locations, left_index=True, right_index=True)
    # combined_dates.plot(kind='bar', legend = False)
    # f, ax = plt.subplots(figsize=(18, 5))  # set the size that you'd like (width, height)



    ############################### GRAPHS WE CARE ABOUT!!!##########################################
    #################################################################################################
    # combined_locations.plot(kind='bar', legend=True, colormap='Paired', width= .9, yticks=[])
    # yearly_avg.plot(kind='bar', legend=True, colormap='Paired', width= .9)

    # instances = list(pd.DatetimeIndex(df_complete[df_complete.Category.str.contains('Civil Sidewalks')].Date).year)
    # valid_years = list(set(pd.DatetimeIndex(df_complete.Date).year))
    # valid_years.sort()
    # count_year = np.zeros((1, len(valid_years[0: -2])))
    # for i in valid_years:
    #     if i < 2018:
    #         count_year[0, valid_years.index(i)] = instances.count(i)
    # plt.show()

    # fig, ax1 = plt.subplots()
    # ax2 = ax1  # set up the 2nd axis
    # ax1.bar(combined_years['Year'], combined_years['Homeless Reports'], legend=True, colormap='Paired', width= .9,
    #         yticks=[], alpha=0.2, color='orange', sharex=True)
    # ax2.plot(combined_years['Year'], combined_years['Homeless Reports'])  # plot the Revenue on axis #1

    # plt.show()

    # 'Number of Events': loc_set['Report'], 'Homeless Related': loc_set['Homeless Related'], 'Location': loc_list

    # sns.set()
    # home = combined_locations
    # sns.barplot(x="Zipcode", y="Non-Homeless Crime",
    #             data=home);
    # sns.barplot(x="Zipcode", y="Homeless Report",
    #             data=home, color='blue');
    #
    # plt.show()

    ##########################################################################################
    # combined_locations = pd.DataFrame(data={'Homeless Report': count2_location, 'Non-Homeless Crime': count1_location,
    #                                             'Zipcode': zips})
    x = np.arange(len(combined_locations['Zipcode'].tolist()))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(facecolor= 'black')
    rects1 = ax.bar(x - width / 2, combined_locations['Non-Homeless Crime'].tolist(), width, label='Non-Homeless Crime', color='#37c9ef', alpha = .8)
    rects2 = ax.bar(x + width / 2, combined_locations['Homeless Report'].tolist(), width, label='Homeless Person Reported', color='#13538a', alpha = .9)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of Incidents')
    ax.set_xlabel('Location')
    ax.set_title('Homelessness and Non-Homeless Related Crimes')
    ax.set_xticks(x)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_facecolor('black')
    ax.legend()
    # plt.savefig('Location.png', facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    # autolabel(rects1)
    # autolabel(rects2)

    #####################################################################################################
    # combined_years = pd.DataFrame(data={'Homeless Reports': year2, 'Non-Homeless Crime': year1, 'Year': years})

    x = np.arange(len(combined_years['Year'].tolist()))  # the label locations
    width = 0.45  # the width of the bars

    fig, ax = plt.subplots(facecolor= 'black')
    # ax.text(color='white')
    rects1 = ax.bar(x - width / 2, combined_years['Non-Homeless Crime'].tolist(), width, label='Non-Homeless Crime', color='#37c9ef', alpha = .8)
    rects2 = ax.bar(x + width / 2, combined_years['Homeless Reports'].tolist(), width, label='Homeless Person Reported', color='#13538a', alpha = .9)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # plt.text(color='white')
    ax.set_ylabel('Number of Incidents (Normalized)')
    ax.set_xlabel('Date (2003, 2017)')
    ax.set_title('Homelessness and Non-Homeless Related Crimes')
    ax.set_xticks(x)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.set_xticklabels(combined_years['Year'].tolist())
    ax.set_yticklabels([])
    ax.set_facecolor('black')
    ax.legend()
    # plt.savefig('Time.png', facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    # autolabel(rects1)
    # autolabel(rects2)


#############################################################################################################
    # yearly_avg = pd.DataFrame(
    #     data={'% of Crime Related to Homelessness': years_avg, 'Homeless Reports': year2, 'Year': years})
    x = np.arange(len(yearly_avg['Year'].tolist()))  # the label locations
    width = 0.8  # the width of the bars

    fig, ax = plt.subplots(facecolor='black')
    # ax.text(color='white')
    rects1 = ax.bar(x - width / 2, yearly_avg['% of Crime Related to Homelessness'].tolist(), width, label='% of All Crime Related to Homelessness',
                    color='#37c9ef', alpha=.8)
    # rects2 = ax.bar(x + width / 2, yearly_avg['Homeless Reports'].tolist(), width, label='Homeless Person Reported',
    #                 color='#13538a', alpha=.9)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('% of Crime Related to Homelessness')
    ax.set_xlabel('Date (2003, 2017)')
    ax.set_title('Homelessness and Non-Homeless Related Crimes')
    ax.set_xticks(x)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='y', labelcolor='white')
    ax.set_xticklabels(yearly_avg['Year'].tolist())
    ax.set_facecolor('black')
    # ax.legend()

    plt.savefig('Yearly avg.png', facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)

    # def autolabel(rects):
    #     """Attach a text label above each bar in *rects*, displaying its height."""
    #     for rect in rects:
    #         height = rect.get_height()
    #         ax.annotate('{}'.format(height),
    #                     xy=(rect.get_x() + rect.get_width() / 2, height),
    #                     xytext=(0, 3),  # 3 points vertical offset
    #                     textcoords="offset points",
    #                     ha='center', va='bottom', color='white')
    #
    # autolabel(rects1)
    # autolabel(rects2)

    fig.tight_layout()

    plt.show()




######################### Function Caller ########################################
# scatter_plot(['Complete_Geocoded_Non_homeless_Police_reports.csv',
#               'Complete_Geocoded_Homeless_Police_Reports.csv'], ['Date', 'Zip'])
