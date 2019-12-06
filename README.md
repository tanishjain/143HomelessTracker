# 143HomelessTracker

	This project was meant to find all data that may be used as a proxy for measuring homeless 
	populations in San Francisco. 

Then using this data we hoped to answer several questions: 
- Do people experiencing homelessness congregate near public restrooms, and are there enough public restrooms available to serve San Francisco’s growing homeless population?
- Do correlations between homeless populations and crime exist? and if so, what are they?
- Do homeless people move through San Francisco with any predictability?

	In pursuing this, we first had to find usable datasets. We found several that we deemed suitable. First we went to https://data.sfgov.org/City-Infrastructure/311-Cases/vw6y-z8j6 and downloaded their 311 reports. This is very large dataset, but on looking through the unique values in it we were able to find several that were directly correlated with homelessness: “Encapments,” “Homeless Concerns” and a third set that we sought to prove had a high correlation with our other variables, “Human or animal waste.” The features pulled included the category, description, location (geographical point), and the date.
These sets were cleaned and sorted using the “Data_cleaner()” function.


	We then found 2 police report datasets at https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783 and https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-Historical-2003/tmnf-yvry . From these sets we identified categories and descriptions that were associated with homelessness, 'Lodging Without Permission', 'Civil Sidewalks, Citation', 'Civil Sidewalks, Warning', 'Loitering', 'Obstructing Health Facility, Place of Worship, or School', 'Civil Sidewalks, Violation', 'Lodging in Park', and 'Civil Sidewalks, Booking’. We then were able to separate the files into sets that were “associated with homelessness” and “not associated with homelessness.” The features pulled included the category, description, location (geographical point), and the date.
These sets were cleaned and sorted using the “Data_cleaner()” function.

	Once we had these sets, we extracted their latitude and longitude, and from those added a column containing their zipcodes. 
This was done using the “add_ll()” function

	From there we set about creating bar graphs, histograms, and heatmaps that would best convey the data that we found.
This was done using the "bar_plot()" to create single and double bar graphs.
We also used the function and the ###############etc
