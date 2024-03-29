# Studying the dynamics of San Francisco's Homeless Population

	This project was meant to find all data that may be used as a proxy for measuring homeless 
	populations in San Francisco. 

Then using this data we hoped to answer several questions: 
- How good of a measure are the variables that weare using?
- Do people experiencing homelessness congregate near public restrooms, and are there enough public restrooms available to serve San Francisco’s growing homeless population?
- Do correlations between homeless populations and crime exist? and if so, what are they?
- Do homeless people move through San Francisco with any predictability?

	In pursuing this, we first had to find usable datasets. We found several that we deemed suitable. First we went to https://data.sfgov.org/City-Infrastructure/311-Cases/vw6y-z8j6 and downloaded their 311 reports. This is very large dataset, but on looking through the unique values in it we were able to find several that were directly correlated with homelessness: “Encapments,” “Homeless Concerns” and a third set that we sought to prove had a high correlation with our other variables, “Human or animal waste.” The features pulled included the category, description, location (geographical point), and the date.
These sets were cleaned and sorted using the “Data_cleaner()” function.


	We then found 2 police report datasets at https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783 and https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry . From these sets we identified categories and descriptions that were associated with homelessness, 'Lodging Without Permission', 'Civil Sidewalks, Citation', 'Civil Sidewalks, Warning', 'Loitering', 'Obstructing Health Facility, Place of Worship, or School', 'Civil Sidewalks, Violation', 'Lodging in Park', and 'Civil Sidewalks, Booking’. We then were able to separate the files into sets that were “associated with homelessness” and “not associated with homelessness.” The features pulled included the category, description, location (geographical point), and the date. The cleaner separates the files into two catagories, homeless-related and non-homeless related, and you have the option of keeping the two sets in separate files, or just keeping the homeless related data in a csv file.
These sets were cleaned and sorted using the “Data_cleaner()” function.

	Once we had these sets, we extracted their latitude and longitude, and from those added a column containing their zipcodes. 
This was done using the “add_ll()” function.

	From there we set about creating bar graphs, histograms, and heatmaps that would best convey the data that we found. After experimenting with multiple methods we decided that we should first establish the legitimacy of our variables by creating a correlation matrix.
This was done using the "create_corr_mat(data)" function. This function takes as the input the relevant dataset (in our case, sorted by zip codes; i.e., the rows correspond to various SFO zip codes and columns correspond to various variables), and plots the correlation matrix between the dataset variables. Note that the input dataset must be formatted in a very specific way, with each column representing different variables.
	
	We then wanted to show the relationship between human waste, and public restrooms and decided that a bar plot and heat map would visualize our data well.
This was done using the 'plothist_rest()' function and the heatmap_drawer() respectively.

	To show correlations (or lack therof) it was decided that side by side bar plots would be best.
This was done using the "bar_plot()" to create single and double bar graphs.

	Finally we wanted to show the movement of homeless populations over time, and realised that a heatmap would be excellent for this. We then compiled images by year, and by monthly average into gifs to allow the data to be easily understood.
This was done using the "heatmap_drawer()" function to create month wise or year wise heatmap using the human waste data or encampment data in html form. The function needs a filename to extract data and then when you select second parameter 'M' for month wise of 'Y' for year wise, third parameter 'W' for human waste data and 'E' for encampment data. After we got the maps then we used some tool to combine the maps into gifs.
