import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import folium


# We connect to our database and explore the columns and rows it contains

df = pd.read_csv('C:/Users/vaned/Documents/Analisis con python/mexico_crime.csv')
df.shape
df.head()
df.tail()
df.columns
df.describe()


# We look for any NaN(Not a Numeric value) and assess if we should delete them

df.isna().sum()


# Group the type_of_crime column and sum the count column, then sort it. 
# Understand which types of crimes had more cases registered
crime_counts = df.groupby('type_of_crime')['count'].sum()
print (crime_counts)
crime_counts_sorted = crime_counts.sort_values(ascending=False)
print(crime_counts_sorted)

# Group the month column and sum the count column, then sort it.
# Understand in which month there were more cases registered
month_counts = df.groupby('month')['count'].sum()
month_counts_sorted = month_counts.sort_values(ascending=False)
print(month_counts_sorted)

# Group the subtype_of_crime column and sum the count column, then sort it.
subcrime_counts = df.groupby('subtype_of_crime')['count'].sum()
subcrime_counts_sorted = subcrime_counts.sort_values(ascending=False)
print(subcrime_counts_sorted)


# Location estimates

# Mean
print(f'Promedio: {df["count"].mean()}')

# Median 
print(f'Media: {df["count"].median()}')

# Truncated mean = More robust mean by removing a percentage of data at the beginning and end
print(f'Media truncada, eliminando el 5% de datos: {stats.trim_mean(df["count"], 0.05)}')

# Standard Deviation
print(f'Desviacion estandar: {df["count"].std()}')


# Order Stadistics

# Range
df['count'].max() - df['count'].min()

# Percentiles
# It indicates that at least a % of the dataframe have a certain value or less. 
print(f'Valor mínimo: {df["count"].min()}')
print(f'Percentil 10: {df["count"].quantile(0.1)}')
print(f'Percentil 25: {df["count"].quantile(0.25)}')
print(f'Percentil 50: {df["count"].median()}')
print(f'Percentil 50: {df["count"].quantile(0.5)}')
print(f'Percentil 75: {df["count"].quantile(0.75)}')
print(f'Percentil 80: {df["count"].quantile(0.8)}')
print(f'Percentil 90: {df["count"].quantile(0.9)}')
print(f'Valor máximo: {df["count"].max()}')

# Interquartile range
# Understand to which value our data is most near - to the minimum or to the maximum
print(f'Rango intercuartilico: {df["count"].quantile(0.75) - df["count"].quantile(0.25)}') 


# Visualize the distribution of our data with Boxplots

# Boxplot 1
sns.boxplot(x=df['count']).set(style="whitegrid")
plt.show()

# Boxplot 2
# Graph a vertical line right at the average of our data
sns.set(style="whitegrid")
sns.boxplot(x=df['count'])
plt.axvline(df['count'].mean(), c='y')

grouped_data = df.groupby(['year', 'entity_code', 'entity', 'affected_legal_good', 'type_of_crime',
       'subtype_of_crime', 'modality', 'month']).agg({'count': 'sum'}).reset_index()

# Boxplot 3
subtype_to_filter = 'Drug dealing'
filtered_data_subtype = grouped_data.query(f'subtype_of_crime == "{subtype_to_filter}"')
sns.boxplot(x='year', y='count', data=filtered_data_subtype)
plt.title(f'Boxplot for {subtype_to_filter}')
plt.show()

# Boxplot 4
# Given that the most registered 'subtype_of_crime' was 'Family Violence'
# We want to visualize how it is distributed throughout the years
subtype_to_filter = 'Family Violence'
filtered_data_subtype = grouped_data.query(f'subtype_of_crime == "{subtype_to_filter}"')
sns.boxplot(x='year', y='count', data=filtered_data_subtype)
plt.title(f'Boxplot for {subtype_to_filter}')
plt.show()

# Boxplot 5
# We add an aditional filter, to see only the registered cases in the Capital 'Ciudad de México'
entity_to_filter = 'Ciudad de México'
subtype_to_filter = 'Family Violence'

filtered_data = grouped_data.query(f'entity == "{entity_to_filter}" and subtype_of_crime == "{subtype_to_filter}"')
sns.boxplot(x='year', y='count', data=filtered_data)
plt.title(f'Boxplot for {subtype_to_filter} en {entity_to_filter}')
plt.show()

# Boxplot 6
# We keep analyzing the currencies of 'Family Violence' within different states of Mexico
entity_to_filter = 'Nuevo León'
subtype_to_filter = 'Family Violence'

filtered_data = grouped_data.query(f'entity == "{entity_to_filter}" and subtype_of_crime == "{subtype_to_filter}"')
sns.boxplot(x='year', y='count', data=filtered_data)
plt.title(f'Boxplot for {subtype_to_filter} en {entity_to_filter}')
plt.show()


# Interquartile Range Score (IQR-Score)
# We filter the outliers. We limit the size of whiskers and filter all data that exceeds that limit
iqr = df['count'].quantile(0.75) - df['count'].quantile(0.25)
filtro_inferior = df['count'] > df['count'].quantile(0.25) - (iqr * 1.5)
filtro_superior = df['count'] < df['count'].quantile(0.75) + (iqr * 1.5)
df_filtrado = df[filtro_inferior & filtro_superior]
sns.boxplot(df_filtrado['count'])


# Table of frequency
# Another way to look at the atipical values 

counts = df['count']
counts.max() - counts.min()
pd.cut(counts, 20)

segmentos = pd.cut(counts, 20)
df['count'].groupby(segmentos).count()


# Histrograms 
# Another way to see our table of frequency
# The x axis is the range of our data and it is divided by segments 
# The axis y indicates the count of our sample on each segment 
sns.set(style='white')
sns.distplot(df['count'], kde=False, norm_hist=False, bins=30)

# We increase the size of our bins to visualize it with more granularity 
sns.set(style='ticks')
sns.distplot(df['count'], kde=False, norm_hist=False, bins=100)


# Through a Histogram we want to see 'Family Violence' cases that were registered during 2022 in 'Ciudad de México' 
year_to_filter = 2022
entity_to_filter = 'Ciudad de México'
subtype_to_filter = 'Family Violence'

filtered_data = df[(df['year'] == year_to_filter) & 
                   (df['entity'] == entity_to_filter) & 
                   (df['subtype_of_crime'] == subtype_to_filter)]

sns.set(style='whitegrid')
sns.distplot(filtered_data['count'], kde=False, norm_hist=False, bins=20)
plt.title(f'Histogram for {subtype_to_filter} in {entity_to_filter} during {year_to_filter}')
plt.show()

from scipy.stats import skew, kurtosis

import numpy as np

normal = np.random.normal(loc=0, scale=5, size=10000)

sns.distplot(normal, kde=False, norm_hist=False);

print(f'Curtosis: {kurtosis(normal)}')
print(f'Asimetría: {skew(normal)}')

asimetria_positiva = np.random.exponential(scale=1.0, size=10000)
sns.distplot(asimetria_positiva, kde=False, norm_hist=False);


# Bar Graph 

ax = sns.barplot(x='type_of_crime', y='count', data=grouped_data)
ax.set_title('Crimes registered in Mexico')
ax.set_ylabel('Count')
plt.xticks(rotation=90)
plt.show()

# Bar Graph for crimes registered in Jalisco
entity_to_filter = 'Jalisco'
filtered_df = df[(df['entity'] == entity_to_filter)]

plt.figure(figsize=(10, 6))
sns.barplot(x='type_of_crime', y='count', data=filtered_df)
plt.title(f'Crimes registered in {entity_to_filter}')
plt.xlabel('Type of Crime')
plt.ylabel('Count')
plt.xticks(rotation=90)
plt.show()


# Contingency tables

pd.crosstab(df['entity'], df['type_of_crime'])

contingency_table = pd.crosstab(index=df['entity'], columns=df['type_of_crime'], values=df['count'], aggfunc='sum', margins=True, margins_name='Total')
print(contingency_table)

contingency_table = pd.crosstab(index=[df['entity'], df['month']], columns=df['type_of_crime'], values=df['count'], aggfunc='sum', margins=True, margins_name='Total')
print(contingency_table)

entity_to_filter = 'Ciudad de México'
month_to_filter = 'December'
filtered_data = df[(df['entity'] == entity_to_filter) & (df['month'] == month_to_filter)]
contingency_table_filtered = pd.crosstab(index=filtered_data['entity'], columns=filtered_data['type_of_crime'], values=filtered_data['count'], aggfunc='sum', margins=True, margins_name='Total')
plt.figure(figsize=(12, 10))
sns.heatmap(contingency_table_filtered.iloc[:-1, :-1], annot=True, fmt='d', cmap='Blues')
plt.title(f'Heatmap for Type of Crime in {entity_to_filter} during {month_to_filter}')
plt.xlabel('TYpe of Crime')
plt.ylabel('Entity')
plt.show()


# Coeficiente de correlacion de Pearson

correlacion = df['year'].corr(df['count'])
print("Coeficiente de Correlación de Pearson:", correlacion)

# Scatter Plot 1
plt.scatter(df['year'], df['count'])
plt.title('Scatter Plot')
plt.xlabel('Year')
plt.ylabel('Amount of Crimes registered')
plt.show()

# Scatter Plot 2
sns.scatterplot(x='year', y='count', data=df)
plt.title('Scatter Plot')
plt.xlabel('Year')
plt.ylabel('Amount of Crimes registered')
plt.show()

# Correlation Matrix
matriz_correlacion = df[['year', 'count']].corr()
plt.figure(figsize=(8, 6))  
sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.show()

# We create 'dummy' variables for a category: 
# A 'dummy' variable represents categoric variables in models that only accept numeric values.

# Correlation Heatmap with dymmy variables
df_dummy = pd.get_dummies(df, columns=['type_of_crime'])
df_dummy = df_dummy.drop(['affected_legal_good', 'entity', 'subtype_of_crime', 'modality', 'month', 'entity_code'], axis=1)
matriz_correlacion = df_dummy.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(matriz_correlacion, annot=False, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

# We change the format
df_dummy = pd.get_dummies(df, columns=['type_of_crime'])
df_dummy = df_dummy.drop(['affected_legal_good', 'entity', 'subtype_of_crime', 'modality', 'month', 'entity_code'], axis=1)
matriz_correlacion = df_dummy.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(matriz_correlacion, annot=False, cmap='coolwarm', linewidths=.5, cbar_kws={"shrink": 0.75})
plt.title('Correlation Heatmap')
plt.xticks(rotation=45) 
plt.yticks(rotation=0) 
plt.show()


# Filter the correlations to an absolute value greater than 0.2
df_dummy = pd.get_dummies(df, columns=['type_of_crime'])
df_dummy = df_dummy.drop(['affected_legal_good', 'entity', 'subtype_of_crime', 'modality', 'month', 'entity_code'], axis=1)
matriz_correlacion = df_dummy.corr()
umbral_correlacion = 0.2
matriz_correlacion_filtrada = matriz_correlacion[(matriz_correlacion > umbral_correlacion) | (matriz_correlacion < -umbral_correlacion)]
plt.figure(figsize=(10, 8))
sns.heatmap(matriz_correlacion_filtrada, annot=False, cmap='coolwarm', linewidths=.5, cbar_kws={"shrink": 0.75})
plt.title('Correlation Heatmap with filters')
plt.xticks(rotation=45)  
plt.yticks(rotation=0)
plt.show()


# Filter by entity and the correlations to an absolute value greater than 0.2
entity_to_filter = 'Ciudad de México'
umbral_correlacion = 0.2
df_filtered = df[df['entity'] == entity_to_filter]
df_dummy = pd.get_dummies(df_filtered, columns=['type_of_crime'])
df_dummy = df_dummy.drop(['affected_legal_good', 'entity', 'subtype_of_crime', 'modality', 'month', 'entity_code'], axis=1)
matriz_correlacion = df_dummy.corr()
matriz_correlacion_filtrada = matriz_correlacion[(matriz_correlacion > umbral_correlacion) | (matriz_correlacion < -umbral_correlacion)]
plt.figure(figsize=(10, 8))
sns.heatmap(matriz_correlacion_filtrada, annot=False, cmap='coolwarm', linewidths=.5, cbar_kws={"shrink": 0.75})
plt.title(f'Mapa de Calor de Correlación - {entity_to_filter}')
plt.xticks(rotation=45)
plt.yticks(rotation=0)  
plt.show()

# Bootstrap ç
df['type_of_crime'].sample(n=20, replace=False)
grouped_data['type_of_crime'].sample(n=20, replace=False)

estados_geo = f'https://gist.githubusercontent.com/Tlaloc-Es/5c82834e5e4a9019a91123cb11f598c0/raw/709ce9126861ef7a7c7cc4afd6216a6750d4bbe1/mexico.geojson'
m = folium.Map(location=[23.6345, -102.5528], zoom_start=5)

# Filter by the most registered subtime of crime:
family_violence = grouped_data[grouped_data['subtype_of_crime'] == 'Family Violence']

folium.Choropleth(
    geo_data=estados_geo,
    name='choropleth',
    data=family_violence,
    columns=['entity', 'count'],
    key_on= 'feature.properties.ENTIDAD',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total de Crímenes por Estado'
).add_to(m)

folium.LayerControl().add_to(m)

m
m.save("mapa.html")