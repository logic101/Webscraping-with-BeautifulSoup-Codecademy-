import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
webpage = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html', 'html.parser')
#Create a BeautifulSoup object
soup = BeautifulSoup(webpage.content)
#Get the ratings for the chocolates
rating = soup.find_all(attrs = {'class' : 'Rating'})
ratings = []
for r in rating[1:]:
  r1 = r.get_text()
  #Convert the ratings to floats
  ratings.append(float(r1))
#Plot a histogram for the ratings to see the distribution.
plt.hist(ratings)
plt.show()
#Get the companies
company = []
makers = soup.find_all(attrs = {'class' : 'Company'})
for m in makers[1:]:
  m1 = m.get_text()
  company.append(m1)
#Create a dataframe consisting of two columns: The company and ratings for each bar,
df = pd.DataFrame({'Company' : company,'Ratings' : ratings })
#create a variable grouped to hold the top 10 companies with highest average ratings
grouped = df.groupby(['Company']).Ratings.mean().nlargest(11).reset_index()
#print(grouped)
#Get the cocoa percentage in each chocolate bar and add it to dataframe
cocoa_percentage = []
cocoa_percents = soup.find_all(attrs = {'class' : 'CocoaPercent'})
for c in cocoa_percents[1:]:
  c1 = float(c.get_text().strip('%'))
  cocoa_percentage.append(c1)
df['CocoaPercentage'] = cocoa_percentage
print(df)
#create a scatter plot for the ratings and cocoa percentage to determine whether or not higher cocoa percentages attract higher ratings.
plt.clf()
plt.scatter(df.CocoaPercentage, df.Ratings, edgecolor = None)
#Draw a line of best fit using NumPy
z = np.polyfit(df.CocoaPercentage, df.Ratings, 1)
line_function = np.poly1d(z)
plt.plot(df.CocoaPercentage, line_function(df.CocoaPercentage), "r--")
plt.show()

