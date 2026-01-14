# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 10:09:27 2026

@author: user
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Agricaltural Exports - US 2011", page_icon=":seedling:", layout="wide")
st.title(":seedling: US Agricaltural Exports in 2011")

link = "https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv"
df = pd.read_csv(link)

df.drop("category", axis=1, inplace=True)
df.rename(columns={'total fruits':'fruits', 'total veggies':'veggies', 'total exports': 'total'}, inplace=True)


# list of categories
categories = ['beef', 'pork', 'poultry', 'dairy', 'fruits', 'veggies', 'corn', 'wheat', 'cotton']

# creating misc. category
df['misc.'] = df['total'] - df[categories].sum(axis=1)
categories.append('misc.')

# Create a new list of categories with 'total exports' as the first element
choropleth_categories = ['total'] + categories
# melting the data to a long format 
df_cat = pd.melt(frame=df, id_vars=['code', 'state'], 
                 value_vars=categories, var_name='category', value_name='export')

# Sidebar for choropleth category selection
st.sidebar.header("Filter Data by Export Category: ")

