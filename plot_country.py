import numpy as np
import scipy.stats as stats
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt

country = 'Africa'

# Grab our information from the data
data = np.genfromtxt("GlobalLandTemperaturesByCountry.csv",
      dtype=None,
      encoding=None,
      skip_header=1,
      delimiter=",",
      usecols=[0,1,2,3])

print("Data type: {}".format(type(data)))
print("Data shape: {}".format(data.shape))

country_dict = {}
for i in range(data.shape[0]):
   # grab the country name at index 3
   if data[i][3] not in country_dict:
      country_dict[data[i][3]] = []
   # np.append(country_dict[data[i][3]], data[i])
   country_dict[data[i][3]].append(data[i])

for key,value in country_dict.items():
   country_dict[key] = np.array(value)

n_country = len(country_dict)

print("Number of countries: {}".format(n_country))
print("Number of entries for {}: {}".format(country, country_dict[country].shape))
print("Example {} entry in country_dict: {}".format(country, country_dict[country][0]))
print("Entries ranging from {} - {}".format(
   country_dict[country][0][0],
   country_dict[country][-1][0]))

sums = [0]*12
errs = [0]*12
counts = [0]*12
c = country_dict[country]
for i in range(c.shape[0]):
   month = int(c[i][0][-5:-3])
   if (not np.isnan(c[i][1])) and (not np.isnan(c[i][2])):
      sums[month-1] += c[i][1]
      errs[month-1] += c[i][2]
      counts[month-1] += 1

counts = np.array(counts)
sums = np.array(sums)
errs = np.array(errs)

avgs = np.divide(sums, counts)
errs = np.divide(errs, counts)

