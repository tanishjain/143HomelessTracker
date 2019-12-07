def plothist_rest(dataframe_reports, dataframe_restrooms, save_plot):
	'''
	Purpose: To plot histograms of incident reports against number of restrooms
			 as a function of zipcode
	
	
	Input:

	Param: dataframe_reports
	Type: A pandas dataframe
	Description: Dataframe with the list of incidences

	Param: dataframe_restrooms
	Type: A pandas dataframe
	Description: Dataframe with list of restrooms

	Param: save
	Type: bool
	Description: Indication of whether to save the figure or not


	Output:

	None
	'''
	import pandas as pd
	import numpy as np
	from matplotlib import pyplot as plt
	from matplotlib.lines import Line2D

	assert isinstance(dataframe_reports, pd.DataFrame)
	assert isinstance(dataframe_restrooms, pd.DataFrame)
	assert isinstance(save_plot, bool)

	list1 = list(dataframe_reports.Zip)
	categories = list(set(list1))
	list2 = list(dataframe_restrooms.zip)
	count = np.zeros((2, 25))
	for zipcode in categories:
	    count[0, categories.index(zipcode)] = list1.count(zipcode)
	    count[1, categories.index(zipcode)] = list2.count(zipcode)
	count[0, :] = count[0, :]/sum(count[0, :])
	count[1, :] = count[1, :]/sum(count[1, :])
	fig = plt.figure(facecolor = 'black')
	ax = plt.subplot(111, facecolor='black')
	bins1 = [3*i + 1 for i in range(0, 25)]
	bins2 = [3*i + 2 for i in range(0, 25)]
	ax.bar(bins1, count[0, :], color = '#13538A', label = 'Incidences', alpha = 0.9)
	ax.bar(bins2, count[1, :], color = '#37C9EF', label = 'Restrooms', alpha = 0.8)
	ax.set_ylabel('Count Density')
	ax.set_xlabel('Zipcode')
	ax.set_xticks([])
	ax.yaxis.label.set_color('white')
	ax.xaxis.label.set_color('white')
	plt.yticks([])
	custom_lines = [Line2D([0], [0], color='#13538A', alpha = 0.9, lw=4),
	                Line2D([0], [0], color='#37C9EF', alpha = 0.8, lw=4)]
	ax.legend(custom_lines, ['Incidences', 'Restrooms'])
	if save_plot:
		plt.savefig('test.png', facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
	plt.show()


def create_colorbar(dataframe, save_plot):
	'''
	Purpose: Create a colorbar for a range of values in a dataframe


	Input:

	Param: dataframe
	Type: a pandas dataframe
	Description: Dataframe with the list of incidences

	Param: save_plot
	Type: bool
	Description: Indication of whether to save the figure or not


	Output:

	None	
	'''
	import pylab as pl
	import numpy as np
	import pandas as pd

	assert isinstance(dataframe, pd.DataFrame)

	a = np.array([[0,len(dataframe)]])
	pl.figure(figsize=(9, 1.5), facecolor='black')
	img = pl.imshow(a, cmap="jet")
	pl.gca().set_visible(False)
	cax = pl.axes([0.1, 0.2, 0.8, 0.6])
	cax.tick_params(axis = 'x', labelcolor='white', colors='white')
	pl.colorbar(orientation='horizontal', cax=cax)
	if save_plot:
		pl.savefig("colorbar.png", facecolor=fig.get_facecolor(), edgecolor='none', dpi=200)
