#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 13:24:41 2020

@author: sashaqanderson
"""

import datetime
import pandas as pd
import numpy as np

def Convert_to_String(string):
    if isinstance(string, str):
        string = string.replace("'", "") 
        string = string.replace("[", "") 
        string = string.replace("]", "") 
        li = list(string.split(", "))
        str1 = ' '.join(li)
        return str1
    else:
        return ''

def Convert_to_List(string):
    if isinstance(string, str):
        string = string.replace("'", "") 
        string = string.replace("[", "") 
        string = string.replace("]", "") 
        li = list(string.split(", "))
        return li
    else:
        return []

def f(row):
    val = Convert_to_String(row['usgsThesaurusKeyword'])
    return val 

def g(row):
    val = Convert_to_List(row['usgsThesaurusKeyword'])
    return val
# 

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
    
    #prepare wordcloud column - all_kw
    df_wc = sample_data.copy()
    df_wc['all_kw'] = df_wc['keyword'] + df_wc['usgsThesaurusKeyword'] + df_wc['isoTopicKeyword'] #+ df_wc['placeKyword']
    df_wc.all_kw.fillna(df_wc.keyword, inplace=True)
    df_wc.all_kw.fillna(df_wc.usgsThesaurusKeyword, inplace=True)
    df_wc.all_kw.fillna(df_wc.isoTopicKeyword, inplace=True)
    
    df2 = df_wc[['datasource.displayname', 'description', 'idinfoBegdate', 'idinfoCaldate', 'idinfoEnddate',
            'all_kw', 'usgsThesaurusKeyword', 'lon', 'lat', 'title']].copy()
    
    #make usgs keywords a list of strings (was a string of a list) for the directory and a clean string for search
    df2["usgsThesaurusKeyword"] = df2["usgsThesaurusKeyword"].str.lower()
    df2['usgsThesString'] = df2.apply(f, axis=1)
    # df2['usgsThesList'] = df2.apply(g, axis=1) works at the end for some reason, not here
    
    #keywords to lower case
    df2["all_kw"] = df2["all_kw"].str.lower()
    #remove words from keyword column (USGS etc) for Wordcloud
    remove_words = ['usgs', 'gt']
    pat = r'\b(?:{})\b'.format('|'.join(remove_words))
    df2['all_kw'] = df2['all_kw'].str.replace(pat, '')
    #remove punctuation from keyword column
    df2["all_kw"] = df2['all_kw'].str.replace('[^\w\s]',' ')
    df2['all_kw'] = df2['all_kw'].str.replace('[\d]', '')
    #strip trailing whitespaces etc
    df2 = df2.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

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
  
    #clean up columns
    df2.drop(['idinfoBegdate', 'idinfoEnddate', 'idinfoCaldate'], axis=1, inplace=True)
    df2.columns = ['sci_center', 'descr', 'all_kw',
       'usgsThesaurusKeyword', 'lon', 'lat', 'title', 'usgsThesString',
       'beg_year', 'end_year']
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
    
    #replace na Science Centers with "Undetermined" & sort
    df2.sci_center.fillna('Undetermined', inplace=True)
    df2.sort_values(by='sci_center', inplace = True)

    df2['usgsThesList'] = df2.apply(g, axis=1)
    return df2

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

# sample_data = pd.read_csv('sdc_sample.csv')
# df_map = create_dfs(sample_data)
# joined_list = df_map.usgsThesList.tolist()
# usgs_thes_short = flatten_list(joined_list)
# usgs_thes_short = set(usgs_thes_short)
# usgs_thes_short = sorted(usgs_thes_short)
# # print(usgs_thes_short[0:10])


# import pickle

# # with open("usgs_thes_short.txt", "wb") as fp:   #Pickling
# #     pickle.dump(usgs_thes_short, fp)

# # with open("usgs_thes_short.txt", "rb") as fp:   # Unpickling
# #     b = pickle.load(fp)

# with open("proc_data.csv", "wb") as fp:   #Pickling
#     pickle.dump(df_map, fp)

# with open("proc_data.csv", "rb") as fp:   # Unpickling
#     c = pickle.load(fp)





# # get a set of sorted science centers
# SC = set(df_map['sci_center'])
# sorted_SC = sorted(SC)


# print(df_map.columns)
# # df_map['usgsThesList'] = df_map.apply(g, axis=1)
# print(df_map['usgsThesList'])
# print(type(df_map['usgsThesList']))

# joined_list = df_map.usgsThesList.tolist()
# usgs_thes_short = flatten_list(joined_list)
# usgs_thes_short = set(usgs_thes_short)
# usgs_thes_short = sorted(usgs_thes_short)
# print(usgs_thes_short)


# df3 = df_map[df_map['usgsThesString'].notna()]
# df_th = df3.loc[df3['usgsThesString'].str.contains('wildlife')] 
# df_th
# .remove.remove_punctuation(text: df['all_kw'][2])
 
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

