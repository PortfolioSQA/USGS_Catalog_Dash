#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 13:24:41 2020

@author: sashaqanderson
"""

import datetime
import pandas as pd

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
    df2.columns = ['sci_center', 'descr', 'all_kw', 'kw', 'lon', 'lat', 'title', 'beg_year', 'end_year']
    
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
    
    #This code is for the static sample data!!!!!!
    #I need to fix it to  reactively add more/less colors based on db science centers???
    # create a list of colors for each science center
    scs = df2.sci_center.unique()
    colors = ["#cc6666", "#663333", "#cc9999", "#f22000", "#8c3123", "#cc8166", "#ffd0bf", "#bf4d00", "#592400", "#402310", 
              "#f2aa79", "#806c60", "#d97400", "#734b1d", "#ffaa00", "#bf8f30", "#332b1a", "#ffd940", "#665c33", "#b3aa86", 
              "#8c8523", "#fffbbf", "#c2f200", "#334000", "#e5ff80", "#5d8c00", "#61f200", "#91e673", "#d0ffbf", "#688060", 
              "#16a600", "#1a661a", "#003307", "#20402d", "#00f281", "#73e6b0", "#bfffe1"," #008055", "#1a6657", "#608079", 
              "#00ccbe", "#8fbfbc", "#008f99", "#003c40", "#80e6ff", "#335c66", "#00aaff", "#002b40", "#86a4b3", "#303a40", 
              "#007ae6", "#4d7599", "#b6cef2", "#001140", "#1a2e66", "#4d6199", "#001180", "#3043bf", "#434659", "#a099cc", 
              "#14004d", "#5200cc", "#8c40ff", "#b380ff", "#241a33", "#4e3366", "#a159b3", "#daace6", "#796080", "#b300bf", 
              "#3c0040", "#73006b", "#ff00cc", "#ff80e5", "#33001b", "#e63995", "#a6537f", "#592d44", "#4d3944", "#73002e", 
              "#e6acc3", "#e5003d", "#bf3056", "#ff80a2", "#806068", "#401016", "#663341", "#400011", "#994d61", "#2e0073",
              "#1a0040"]
    
    df3 = pd.DataFrame()
    df3['scs'] = scs
    df3['colors'] = colors
    
    df4 = pd.merge(df2,df3,left_on=['sci_center'], right_on = ['scs'], how = 'left')
    df4.pop("scs")

    return df4

# sample_data = pd.read_csv('sdc_sample.csv')
# df = create_dfs(sample_data)



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

