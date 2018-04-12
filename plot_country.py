import csv
import numpy as np
import scipy.stats as stats
from IPython.core.pylabtools import figsize
import matplotlib.pyplot as plt

def get_country_avgs(country='Africa',
      in_file="GlobalLandTemperaturesByCountry.csv",
      out_file='avgs.csv'):
   _months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
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
   countries = []
   for i in range(data.shape[0]):
      # grab the country name at index 3
      if data[i][3] not in country_dict:
         country_dict[data[i][3]] = []
         countries.append(data[i][3])
      # np.append(country_dict[data[i][3]], data[i])
      country_dict[data[i][3]].append(data[i])

   for key,value in country_dict.items():
      country_dict[key] = np.array(value)

   print("Number of countries: {}".format(len(countries)))
   print("Number of entries for {}: {}".format(country, country_dict[country].shape))
   print("Example {} entry in country_dict: {}".format(country, country_dict[country][0]))
   print("Entries ranging from {} - {}".format(
      country_dict[country][0][0],
      country_dict[country][-1][0]))

   avgs_dict = {}
   errs_dict = {}
   for k in range(len(countries)):
      sums = [0]*12
      errs = [0]*12
      counts = [0]*12
      c = country_dict[countries[k]]
      for i in range(c.shape[0]):
         month = int(c[i][0][-5:-3])
         if (not np.isnan(c[i][1])) and (not np.isnan(c[i][2])):
            sums[month-1] += c[i][1]
            errs[month-1] += c[i][2]
            counts[month-1] += 1

      counts = np.array(counts)
      sums = np.array(sums)
      errs = np.array(errs)

      avgs_dict[countries[k]] = np.divide(sums, counts)
      errs_dict[countries[k]] = np.divide(errs, counts)

   out = []
   for c in countries:
      out.append(np.column_stack((avgs_dict[c], errs_dict[c])))
   out = np.array(out)

   with open(out_file, 'w', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow(["Month", "Avg. Surface Temperature", "Avg. Uncertainty", "Country"])
      for j in range(out.shape[0]):
         for k in range(out.shape[1]):
            writer.writerow([_months[k], "{0:.3f}".format(out[j,k,0]),
                                         "{0:.3f}".format(out[j,k,1]),
                                         countries[j]])

   return out, countries

if __name__ == '__main__':
   a, b = get_country_avgs()

