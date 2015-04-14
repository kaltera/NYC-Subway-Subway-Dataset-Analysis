__author__ = 'ylucas'

import pandas
from ggplot import *

csv_file = "data.csv"
data = pandas.read_csv(csv_file)


# Rainy vs Non-Rainy Plot
plot = ggplot(data, aes('ENTRIESn_hourly',fill='rain')) + geom_histogram(binwidth=250,alpha=0.8) +\
       scale_x_continuous(limits=(0,7000)) + scale_y_continuous(limits=(0,9000)) +\
       xlab("\nNo. of Entries") + ylab("Occurences\n") + ggtitle("Occurences of No. of Entries for Rainy (Blue) and Non-Rainy (Red) Days \n")

print plot

# Relationship between Temperature and Pressure for non-rainy days
data = data[['weather_lat','weather_lon','DATEn','tempi','pressurei']][data['rain'] == 0].drop_duplicates()
plot = ggplot(data, aes(x='tempi',y='pressurei')) + geom_point() + stat_smooth(method="glm", color='blue') + \
       xlab("\nTemperature (Fahrenheit)") + ylab("Pressure (inches Hg)\n") + ggtitle("Relationship between Pressure and Temperature \n")

print plot


