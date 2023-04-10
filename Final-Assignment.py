#This project is designed to simulate a full workflow of a Data Analyst from getting data off the Database to manipulate it with the use of Python and Pandas module to present it through matplotlib module or Tableau.
#The concept is that we are given a dataset that contains Liquor Sales in the state of Iowa in USA between 2012-2020 and we are asked to find the most popular item per zipcode and the percentage of sales per store in the period between 2016-2019.
#We are also asked to visualize the Data and present them in either a matplotlib format or in Tableau Public.
#Every calculation and transformation of Data has to happen through a Python Script.
#The following steps are just a recommendation, we suggest you trying and think outside the box while working with this data and maybe take different paths.
#Step 1.
#Add the Dataset provided to Workbench.
#Step 2.
#Use a Query to get all the columns of the table between the years 2016-2019
#Step 3.
#Export the data to an CSV file like shown below
#Step 4.
#Use Python and Pandas to Aggregate the CSV data so we can get the most popular item sold based on zip code and percentage of sales per store.
#Step 5.
#Use Matplotlib or Tableau with the newly made CSV file and present your Data.
#Step 6.
#Write a report of the steps you did and what difficulties you faced.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from csv
df = pd.read_csv('finance_liquor_sales.csv')
print(df.head())
popular_items = df.groupby(['zip_code', 'item_description'])['bottles_sold'].sum().reset_index()
popular_items = popular_items.sort_values(['zip_code', 'bottles_sold'], ascending=[True, False])
popular_items = popular_items.groupby('zip_code').first()
sales_2016_2019 = df[(df['date'] >= '2016-01-01') & (df['date'] <= '2019-12-31')]
total_sales = sales_2016_2019['sale_dollars'].sum()
store_sales = sales_2016_2019.groupby('store_number')['sale_dollars'].sum().reset_index()
store_sales['sales_percentage'] = store_sales['sale_dollars'] / total_sales * 100
top_items = df.groupby('item_description')['volume_sold_liters'].sum().reset_index()
top_items = top_items.sort_values('volume_sold_liters', ascending=False).head(10)
sns.set_style('whitegrid')
sns.barplot(x='item_description', y='volume_sold_liters', data=top_items)
plt.xticks(rotation=90)
plt.title('Top 10 Items Sold by Volume')
plt.xlabel('Item Description')
plt.ylabel('Volume Sold (Liters)')
plt.show()
# Filter the data for the desired time period
sales_2016_2019 = df[(df['date'] >= '2016-01-01') & (df['date'] <= '2019-12-31')]

# Group the data by zip code and item, and sum up the bottles sold
bottles_sold_by_zip_item = sales_2016_2019.groupby(['zip_code', 'item_description'])['bottles_sold'].sum().reset_index()

# Group the data by store and sum up the sales dollars
sales_by_store = sales_2016_2019.groupby(['store_number'])['sale_dollars'].sum().reset_index()

# Merge the two data frames together
merged_data = pd.merge(bottles_sold_by_zip_item, df[['store_number', 'zip_code']].drop_duplicates(), on='zip_code')
merged_data = pd.merge(merged_data, sales_by_store, on='store_number')

# Calculate the percentage of sales for each store
merged_data['sales_percentage'] = merged_data['sale_dollars'] / merged_data['sale_dollars'].sum()

# Create the scatter plot
plt.scatter(merged_data['zip_code'], merged_data['bottles_sold'], c=merged_data['sales_percentage'], cmap='Blues')
plt.colorbar(label='Percentage of Sales')
plt.xlabel('Zip Code')
plt.ylabel('Bottles Sold')
plt.title('Bottles Sold vs. Zip Code, Colored by Percentage of Sales')
plt.show()