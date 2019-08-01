#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 12:09:01 2019

@author: deborahkhider

Express lat lon explicitly from summary output

"""

import pandas as pd
import numpy as np

data = pd.read_csv("sorghum-output-summary.csv")
coor = list(data['location'])
lat =[]
lon=[]

for item in coor:
    word = item.split()
    if word[1] is 'North':
        lat.append(float(word[0]))
    else:
        lat.append(-float(word[0]))
    if word [4] is 'East':
        lon.append(float(word[3]))
    else:
        lon.append(-float(word[3]))

headers = list(data)

data2 = {'latitude':lat,'longitude':lon}

for item in headers:
    if item is not 'location':
        data2[item] = data[item]

df = pd.DataFrame(data2)

df.to_csv("sorghum.csv")