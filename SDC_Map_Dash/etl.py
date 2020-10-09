#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 13:24:41 2020

@author: sashaqanderson
"""

import datetime
import pandas as pd
from collections import Counter
import numpy as np

def create_dfs(sample_data):
    # Drop rows with no location for mapping 
    sample_data = sample_data[sample_data['spatial'].notna()].copy()
    sample_data['spatial'] = sample_data['spatial'].replace(' degrees','', regex=True)
    
    #split the spatial data and find the center point. Add center lon/lat to sample_data.
    df = sample_data.spatial.str.split(expand=True,)
    df = df.replace(',','', regex=True)
    for i in df.columns:    
        df[i] = pd.to_numeric(df[i], errors='coerce')
    df['lat'] = (df[1] + df[3])/2.0
    df['lon'] = (df[0] + df[2])/2.0
    sample_data['lat'] = df['lat']
    sample_data['lon'] = df['lon']
    # Remove rows with invalid lon/lat
    sample_data = sample_data[sample_data['lon'].notna()]
    sample_data = sample_data[sample_data['lon'] < 181]
    
    df2 = sample_data[['datasource.displayname', 'description', 'idinfoBegdate', 'idinfoCaldate', 'idinfoEnddate',
            'placeKeyword', 'usgsThesaurusKeyword', 'lon', 'lat']].copy()
    
    #combine keywords into one column
    # df2['kw'] = df2['keyword'] + df2['usgsThesaurusKeyword'] + df2['isoTopicKeyword']
    # df2.kw.fillna(df2.keyword, inplace=True)
    # df2.kw.fillna(df2.usgsThesaurusKeyword, inplace=True)
    # df2.kw.fillna(df2.isoTopicKeyword, inplace=True)
    
    # del df2['keyword']
    # del df2['usgsThesaurusKeyword']
    # del df2['isoTopicKeyword']
    
    # fill NA in beg/end date with CalDate and convert to integer
    df2.idinfoBegdate.fillna(df2.idinfoCaldate, inplace=True)
    df2.idinfoEnddate.fillna(df2.idinfoCaldate, inplace=True)
    df2['idinfoBegdate'] = df2['idinfoBegdate'].astype(str).str.strip('[]')
    df2['idinfoBegdate'] = df2['idinfoBegdate'].astype(str).str.strip("''")
    df2['idinfoEnddate'] = df2['idinfoEnddate'].astype(str).str.strip('[]')
    df2['idinfoEnddate'] = df2['idinfoEnddate'].astype(str).str.strip("''")
    df2['beg_year'] = df2['idinfoBegdate'].astype(str).str[0:4]
    df2['end_year'] = df2['idinfoEnddate'].astype(str).str[0:4]
    #replace pres/Pres with current year
    today = datetime.datetime.now()
    df2['end_year'].replace(['pres'], today.year, inplace=True)
    df2['end_year'].replace(['Pres'], today.year, inplace=True)
    
    df2.drop(['idinfoBegdate', 'idinfoEnddate', 'idinfoCaldate'], axis=1, inplace=True)
  
    df2.columns = ['sci_center', 'descr', 'place_kw', 'kw', 'lon', 'lat',
            'beg_year', 'end_year']

    # Use to drop beg/end year values are 'pres', 'Unkn', 'nan', 'Not' instead of replace
    # df_dates = df2[(df2['beg_year'] != 'nan') & (df2['beg_year'] != 'Unkn') & (df2['end_year'] != 'Unkn') 
    #                 & (df2['beg_year'] != 'unkn') & (df2['beg_year'] != 'Not') & (df2['end_year'] != 'Not')
    #                 & (df2['end_year'] != 'Not ')]
    # df_dates['end_year'] = pd.to_numeric(df_dates['end_year'])
    # df_dates['beg_year'] = pd.to_numeric(df_dates['beg_year'])
    
    #eplace beg_date with 1900 and end date with present year for null date values
    df2['beg_year'].replace(['nan'], '1900', inplace=True)
    df2['beg_year'].replace(['Unkn'], '1900', inplace=True)
    df2['beg_year'].replace(['unkn'], '1900', inplace=True)
    df2['beg_year'].replace(['Not'], '1900', inplace=True)
    df2['beg_year'].replace(['Not '], '1900', inplace=True)
    df2['end_year'].replace(['nan'], today.year, inplace=True)
    df2['end_year'].replace(['Unkn'], today.year, inplace=True)
    df2['end_year'].replace(['unkn'], today.year, inplace=True)
    df2['end_year'].replace(['Not'], today.year, inplace=True)
    df2['end_year'].replace(['Not '], today.year, inplace=True)
    #date year as integer
    df2['end_year'] = df2['end_year'].astype(int)
    df2['beg_year'] = df2['beg_year'].astype(int)
    #replace na Science Centers with "Undeteremined" & sort
    df2.sci_center.fillna('Undeteremined', inplace=True)
    df2.sort_values(by='sci_center', inplace = True)
    
    # ## df for tab 3
    # #global data (not the best way to find global data)
    # # placekeyword: world, earth, United States, Coterminous United States,continental united states, Asia, Africa
    # df_earth = df2[(df2['place_kw'] == 'World') | (df2['place_kw'] == 'Earth') | df2['place_kw'].str.contains('Africa') |
    #                 df2['place_kw'].str.contains('Asia') | df2['place_kw'].str.contains('Greenland') | df2['place_kw'].str.contains('Brazil') |
    #                 df2['place_kw'].str.contains('Nepal') | df2['place_kw'].str.contains('urope')]
    
    # ## df for tab 2
    # df_US = df2[(df2['place_kw'] == 'United States') | (df2['place_kw'] == 'United States of America') |
    #             (df2['place_kw'] == 'Continental United States') | df2['place_kw'].str.contains('terminous')]
    # new = df2.merge(df_earth,on=['sci_center','descr', 'place_kw', 'lon', 'lat', 'kw', 'beg_year'],how='left')
    
    # # non-global data with date
    # df_continent = new[new.end_year_y.isnull()]
    # df_continent.drop('end_year_y', axis=1, inplace=True)
    
    # #mappable data (not US or global)
    # new2 = df_continent.merge(df_US,on=['sci_center','descr', 'place_kw', 'lon', 'lat', 'kw', 'beg_year'],how='left')
    
    # ## df for tab 1
    # df_map= new2[new2.end_year.isnull()]
    # df_map.drop('end_year', axis=1, inplace=True)
    
    return df2

# sample_data = pd.read_csv('sdc_sample.csv')
# df_map = create_dfs(sample_data)
# SC = set(df_map['sci_center'])
# sorted_SC = sorted(SC)


# sample_data = pd.read_csv('sdc_sample.csv')
# df_map, df_US, df_earth = create_dfs(sample_data)
# options = [item for item in set(df_map['sci_center'])]
# print(options)
# df_ms = df_map.copy()
# df_ms['sci_center'] = df_ms['sci_center'].fillna('')
# df_ms['kw'] = df_ms['kw'].fillna('')  
# result = df_ms.loc[df_ms['sci_center'] == "Fort Collins Science Center"]

    
# eco = ['ecosystem', 'ecology', 'ecol', 'eco']
# org = ['species', 'biological', 'plants', 'animal', 'species', 'fish', 'wildlife', 'birds', 'diversity', 'habitat', 'population']
# em = ['oil', 'petroleum', 'gas', 'rock', 'dissolved', 'isotopes', 'chemical', 'mineral', 'geochemistry', 'mine']
# lan = ['erosion', 'soil', 'sediment', 'rock', 'logging', 'geospatial', 'geophysical', 'agriculture', 'coastal', 'land']
# nh = ['earthquake', 'seismic', 'hazard', 'volcanic','volcano', 'volcan']
# wat = ['water', 'groundwater', 'river', 'wetland', 'aquifer', 'hydrology', 'ocean', 'flood', 'reservoir', 'bathymetry', 'marine', 'flow', 'aquatic']


# contains = [result['kw'].str.contains(i) for i in eco]
# result = result[np.all(contains, axis=0)]
# print(result.to_dict("records"))
# keywords = pd.DataFrame(df_map['kw'].str.split(',', expand=True).stack())
# keywords[0] = keywords[0].str.replace(r"[\"\',]", '')
# keywords[0] = keywords[0].str.replace('[','')
# keywords[0] = keywords[0].str.replace(']','')
# keywords[0] = keywords[0].str.replace('(','')
# keywords[0] = keywords[0].str.replace(')','')
# keywords[0] = keywords[0].str.strip()
# keywords[0] = keywords[0].str.lower()
# keys = set(keywords[0])
# print(Counter(" ".join(keys).split()).most_common(200))
# print(len(keys)) #1431

#most common: 
    # Ecosystems: ecosystem, ecology (ecol)
    # Organisms: species, biological, plants, animal, species, fish, wildlife, birds, diversity habitat population
    # Energy & Minerals: oil, petroleum, gas, rock, dissolved, isotopes, chemical, mineral, geochemistry, mine
    # Land: erosion, soil, sediment, rock, logging, geospatial, geophysical, agriculture, coastal, land
    # Natural Hazard: arthquake/seismic, hazard, volcanic (vulcan)
    # Water: water, groundwater, river, wetland, aquifer, hydrology, ocean, flood, reservoir, bathymetry, marine, flow, aquatic
    # geologic GPS, geophysics, urban, aerial, contaminants (contam)



#use to select keywords from dataframe
# keywords = ['water quality']

# df_new = df_map[df_map['kw'].isin(keywords)]

# df_ms = df_map.copy()

# eco = ['ecosystem', 'ecology', 'ecol', 'eco']
# org = ['species', 'biological', 'plants', 'animal', 'species', 'fish', 'wildlife', 'birds', 'diversity', 'habitat', 'population']
# em = ['oil', 'petroleum', 'gas', 'rock', 'dissolved', 'isotopes', 'chemical', 'mineral', 'geochemistry', 'mine']
# lan = ['erosion', 'soil', 'sediment', 'rock', 'logging', 'geospatial', 'geophysical', 'agriculture', 'coastal', 'land']
# nh = ['earthquake', 'seismic', 'hazard', 'volcanic','volcano', 'volcan']
# wat = ['water', 'groundwater', 'river', 'wetland', 'aquifer', 'hydrology', 'ocean', 'flood', 'reservoir', 'bathymetry', 'marine', 'flow', 'aquatic']
# df_ms['kw'] = df_ms['kw'].fillna('')
# contains = [df_ms['kw'].str.contains(i) for i in eco]
# result = df_ms[np.all(contains, axis=0)]

# result = result.loc[df_ms['sci_center'] == "Fort Collins Science Center"]
