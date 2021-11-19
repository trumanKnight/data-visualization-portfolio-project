import os
import sys

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
#############################################################################################################

#setting up PATH variables to access and direct files created by the script
PATH = os.path.dirname(os.getcwd())
dPATH = PATH + '/data/'
sPATH = PATH + '/scripts/'
iPATH = PATH + '/images/'
#############################################################################################################

#load data into df

df = pd.read_csv(dPATH + 'all_data.csv')
#############################################################################################################

#create a data frame with the Average GDP per country over the full time frame, sorted by largest to smallest

GDP_descending = df.groupby('Country', as_index=False)[['Country','GDP']].mean()
GDP_average_descending = GDP_descending.sort_values('GDP', ascending = False, ignore_index  = True)
#############################################################################################################

#create a plot of the Average GDP by country, and save it

time_span = df.Year.max() - df.Year.min() + 1

fig = plt.figure(figsize = (12,12))
ax = sns.barplot(data = GDP_average_descending, x = 'Country', y = 'GDP')
plt.xticks(rotation = 45)
ax.set_title(f'Trailing {time_span} Year Average GDP by Country', fontsize=12)

plt.savefig(iPATH + f'Trailing {time_span} Year Average GDP by Country.PNG')
plt.clf()
#############################################################################################################

#create a plot for GDP over Time by country, and save it
fig = plt.figure(figsize = (12,12))
ax = sns.lineplot(data = df, x = 'Year', y = 'GDP', hue = 'Country')

plt.savefig(iPATH + 'GDP vs. Time -- hue = Country.PNG')
plt.clf()
#############################################################################################################

#Create a 2x3 display of plots showing Life Expectancy v GDP, and save it

countries = list(df['Country'].unique())

i = 1
fig = plt.figure(figsize = (20,20))
for country in countries:
	df_temp = df[df.Country == country]
	ax = fig.add_subplot(2,3,i)
	sns.regplot(data = df_temp, x = 'Life expectancy at birth (years)', y = 'GDP')
	plt.title(f'{country} Life Expectancy vs. GDP')
	i += 1

plt.savefig(iPATH + 'Life Expectancy vs. GDP -- 2x3.PNG')
plt.clf()
#############################################################################################################

#calculating each 
total_GDP_by_year = df.groupby('Year').sum()['GDP']

for row in df.index:
	index = df.iloc[row]['Year']
	df.loc[row, 'Total GDP'] = total_GDP_by_year[index]
df['Pct of GDP'] = df['GDP'] / df['Total GDP']*100

i = 1
fig = plt.figure(figsize = (20,20))
for country in countries:
	df_temp = df[df.Country == country]

	ax = fig.add_subplot(2,3,i)
	sns.regplot(data = df_temp, x = 'Year', y = 'Pct of GDP', label = 'Pct Total GDP')
	ax.legend(loc = 'upper left')

	ax2 = ax.twinx()
	sns.regplot(data = df_temp, x = 'Year', y = 'Life expectancy at birth (years)', label = 'Life Expectancy', color = 'red')
	ax2.legend(loc = 'upper right')

	plt.title(f'{country} Life Expectancy\nvs. GDP')

	i += 1
plt.subplots_adjust(wspace = .3)
plt.savefig(iPATH + 'Life Ex v Time vs. Pct Total GDP v Time.PNG')
plt.clf()

fig = plt.figure(figsize = (20,20))

prev_GDP = df.groupby('Country')['GDP'].shift()
df['GDP % Growth'] = ( df.GDP - prev_GDP ) / prev_GDP *100

prev_total_GDP = df.groupby('Country')['Total GDP'].shift()
df['Total GDP % Growth'] = ( df['Total GDP'] - prev_total_GDP ) / prev_total_GDP * 100

i = 1
for country in df.Country.unique():
    ax = fig.add_subplot(2,3,i)
    sns.lineplot(data = df[df.Country == country], x = 'Year', y = 'GDP % Growth', label = f'{country}')
    sns.lineplot(data = df[df.Country == country], x = 'Year', y = 'Total GDP % Growth', color = 'black', label = 'Total GDP % Growth')
    plt.title(f'{country} YoY GDP % Growth)')
    plt.legend()
    i += 1
plt.savefig(f'{iPATH}YoY GDP Pct Growth.PNG')
plt.clf()