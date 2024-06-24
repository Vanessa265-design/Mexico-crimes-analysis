# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 21:15:35 2023
@author: vaned
"""
# Cuales son los tipos y subtipos de crimenes mas comunes

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import folium

df = pd.read_csv('C:/Users/vaned/Documents/Analisis con python/mexico_crime.csv')
df.shape
df.head()
df.tail()
df.columns
df.describe()
df.isna().sum()

crime_counts = df.groupby('type_of_crime')['count'].sum()
print (crime_counts)
crime_counts_sorted = crime_counts.sort_values(ascending=False)
print(crime_counts_sorted)
month_counts = df.groupby('month')['count'].sum()
month_counts_sorted = month_counts.sort_values(ascending=False)
print(month_counts_sorted)

subcrime_counts = df.groupby('subtype_of_crime')['count'].sum()
subcrime_counts_sorted = subcrime_counts.sort_values(ascending=False)
print(subcrime_counts_sorted)

# Estimados de locacion

# Promedio
print(f'Promedio: {df["count"].mean()}')

# Mediana 
print(f'Media: {df["count"].median()}')

# Media truncada = Promedio mas robusto al eliminar un porcentaje de datos al inicio y al final
print(f'Media truncada, eliminando el 5% de datos: {stats.trim_mean(df["count"], 0.05)}')

# Estimados de variabilidad, el mas comun es la desviacion estandar

print(f'Desviacion estandar: {df["count"].std()}')

# Estadisticos de orden

# Range
df['count'].max() - df['count'].min()

# Percentiles (cuantiles)
# El percentil indica que por lo menos 80% de los valores en el conjunto tienen este valor o un valor menor
# En pandas los percentiles son cuantiles (version fracciones)

print(f'Valor mínimo: {df["count"].min()}')
print(f'Percentil 10: {df["count"].quantile(0.1)}')
print(f'Percentil 25: {df["count"].quantile(0.25)}')
print(f'Percentil 50: {df["count"].median()}')
print(f'Percentil 50: {df["count"].quantile(0.5)}')
print(f'Percentil 75: {df["count"].quantile(0.75)}')
print(f'Percentil 80: {df["count"].quantile(0.8)}')
print(f'Percentil 90: {df["count"].quantile(0.9)}')
print(f'Valor máximo: {df["count"].max()}')

# Rango intercuartilico
print(f'Rango intercuartilico: {df["count"].quantile(0.75) - df["count"].quantile(0.25)}') 
# La mayoria de los datos estàn mucho mas cerca al valor minimo que al valor maximo 

# Boxplot 1
sns.boxplot(x=df['count']).set(style="whitegrid")
plt.show()
# Los boxplots son una manera de visualizar la distribución de nuestros datos usando percentiles.

# Boxplot 2
# Graficamos una linea vertical justo donde esta el promedio de nuestros datos.
sns.set(style="whitegrid")
sns.boxplot(x=df['count'])
plt.axvline(df['count'].mean(), c='y')

grouped_data = df.groupby(['year', 'entity_code', 'entity', 'affected_legal_good', 'type_of_crime',
       'subtype_of_crime', 'modality', 'month']).agg({'count': 'sum'}).reset_index()

# Boxplot 3
subtype_to_filter = 'Drug dealing'
filtered_data_subtype = grouped_data.query(f'subtype_of_crime == "{subtype_to_filter}"')
sns.boxplot(x='year', y='count', data=filtered_data_subtype)
plt.title(f'Boxplot para {subtype_to_filter}')
plt.show()

# Boxplot 4
subtype_to_filter = 'Family Violence'
filtered_data_subtype = grouped_data.query(f'subtype_of_crime == "{subtype_to_filter}"')
sns.boxplot(x='year', y='count', data=filtered_data_subtype)
plt.title(f'Boxplot para {subtype_to_filter}')
plt.show()

# Boxplot 5
entity_to_filter = 'Ciudad de México'
subtype_to_filter = 'Family Violence'

filtered_data = grouped_data.query(f'entity == "{entity_to_filter}" and subtype_of_crime == "{subtype_to_filter}"')
sns.boxplot(x='year', y='count', data=filtered_data)
plt.title(f'Boxplot para {subtype_to_filter} en {entity_to_filter}')
plt.show()

# Boxplot 6
entity_to_filter = 'Nuevo León'
subtype_to_filter = 'Family Violence'

filtered_data = grouped_data.query(f'entity == "{entity_to_filter}" and subtype_of_crime == "{subtype_to_filter}"')
sns.boxplot(x='year', y='count', data=filtered_data)
plt.title(f'Boxplot para {subtype_to_filter} en {entity_to_filter}')
plt.show()


# Score de Rango Intercuartílico (IQR-Score)
# Filtramos los valores atipicos. Limitamos el tamaño de los bigotes y filtramos todos los datos que exceden ese limite
iqr = df['count'].quantile(0.75) - df['count'].quantile(0.25)
filtro_inferior = df['count'] > df['count'].quantile(0.25) - (iqr * 1.5)
filtro_superior = df['count'] < df['count'].quantile(0.75) + (iqr * 1.5)
df_filtrado = df[filtro_inferior & filtro_superior]
sns.boxplot(df_filtrado['count'])


# Tabla de frecuencias 
# Otra manera de ver valores atipicos

counts = df['count']
counts.max() - counts.min()
pd.cut(counts, 20)

segmentos = pd.cut(counts, 20)
df['count'].groupby(segmentos).count()


# Histrogramas  
# una forma de ver nuestras tablas de frecuencia 
# El eje x es el rango de nuestros datos y se divide por segmentos
# El eje y indica el conteo de muestras en cada segmento.
sns.set(style='white')
sns.distplot(df['count'], kde=False, norm_hist=False, bins=30)

# Aumentamos el tamaño de nuestros bins para verlo con mayor granularidad 
sns.set(style='ticks')
sns.distplot(df['count'], kde=False, norm_hist=False, bins=100)


# Histograma con filtros 
year_to_filter = 2022
entity_to_filter = 'Ciudad de México'
subtype_to_filter = 'Family Violence'

filtered_data = df[(df['year'] == year_to_filter) & 
                   (df['entity'] == entity_to_filter) & 
                   (df['subtype_of_crime'] == subtype_to_filter)]

sns.set(style='whitegrid')
sns.distplot(filtered_data['count'], kde=False, norm_hist=False, bins=20)
plt.title(f'Histograma para {subtype_to_filter} en {entity_to_filter} en {year_to_filter}')
plt.show()

from scipy.stats import skew, kurtosis

import numpy as np

normal = np.random.normal(loc=0, scale=5, size=10000)

sns.distplot(normal, kde=False, norm_hist=False);

print(f'Curtosis: {kurtosis(normal)}')
print(f'Asimetría: {skew(normal)}')

asimetria_positiva = np.random.exponential(scale=1.0, size=10000)
sns.distplot(asimetria_positiva, kde=False, norm_hist=False);


# Grafica de barras

ax = sns.barplot(x='type_of_crime', y='count', data=grouped_data)
ax.set_title('Conteo de tipos de crimen en México')
ax.set_ylabel('Conteo')
plt.xticks(rotation=90)
plt.show()

entity_to_filter = 'Jalisco'
filtered_df = df[(df['entity'] == entity_to_filter)]

plt.figure(figsize=(10, 6))
sns.barplot(x='type_of_crime', y='count', data=filtered_df)
plt.title(f'Conteo de Type of Crime en {entity_to_filter}')
plt.xlabel('Tipo de Crimen')
plt.ylabel('Conteo')
plt.xticks(rotation=90)
plt.show()


# Tablas de contingencia

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
plt.title(f'Heatmap para Type of Crime en {entity_to_filter} - Mes {month_to_filter}')
plt.xlabel('Tipo de Crimen')
plt.ylabel('Entidad')
plt.show()


# Coeficiente de correlacion de Pearson

correlacion = df['year'].corr(df['count'])
print("Coeficiente de Correlación de Pearson:", correlacion)

plt.scatter(df['year'], df['count'])
plt.title('Scatter Plot de Año vs. Cantidad de Crímenes')
plt.xlabel('Año')
plt.ylabel('Cantidad de Crímenes')
plt.show()

sns.scatterplot(x='year', y='count', data=df)
plt.title('Scatter Plot de Año vs. Cantidad de Crímenes')
plt.xlabel('Año')
plt.ylabel('Cantidad de Crímenes')
plt.show()

matriz_correlacion = df[['year', 'count']].corr()
plt.figure(figsize=(8, 6))  
sns.heatmap(matriz_correlacion, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Mapa de Calor de Correlación')
plt.show()

# Tratar de crear variables dummy para una categoria: 
# Una variable dummy es representar variables categóricas en modelos que solo aceptan entradas numéricas.


df_dummy = pd.get_dummies(df, columns=['type_of_crime'])
df_dummy = df_dummy.drop(['affected_legal_good', 'entity', 'subtype_of_crime', 'modality', 'month', 'entity_code'], axis=1)
matriz_correlacion = df_dummy.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(matriz_correlacion, annot=False, cmap='coolwarm')
plt.title('Mapa de Calor de Correlación')
plt.show()

# Cambiando el formato 
df_dummy = pd.get_dummies(df, columns=['type_of_crime'])
df_dummy = df_dummy.drop(['affected_legal_good', 'entity', 'subtype_of_crime', 'modality', 'month', 'entity_code'], axis=1)
matriz_correlacion = df_dummy.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(matriz_correlacion, annot=False, cmap='coolwarm', linewidths=.5, cbar_kws={"shrink": 0.75})
plt.title('Mapa de Calor de Correlación')
plt.xticks(rotation=45) 
plt.yticks(rotation=0) 
plt.show()


# Filtrando solo las correlaciones con un valor absoluto mayor a 0.2
df_dummy = pd.get_dummies(df, columns=['type_of_crime'])
df_dummy = df_dummy.drop(['affected_legal_good', 'entity', 'subtype_of_crime', 'modality', 'month', 'entity_code'], axis=1)
matriz_correlacion = df_dummy.corr()
umbral_correlacion = 0.2
matriz_correlacion_filtrada = matriz_correlacion[(matriz_correlacion > umbral_correlacion) | (matriz_correlacion < -umbral_correlacion)]
plt.figure(figsize=(10, 8))
sns.heatmap(matriz_correlacion_filtrada, annot=False, cmap='coolwarm', linewidths=.5, cbar_kws={"shrink": 0.75})
plt.title('Mapa de Calor de Correlación Filtrado')
plt.xticks(rotation=45)  
plt.yticks(rotation=0)
plt.show()


# Filtrando por entidad y las correlaciones con un valor absoluto mayor a 0.2
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

# Filtro por el subtipo de crimen mas alto registrado:
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