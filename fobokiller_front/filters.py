import streamlit as st
import pandas as pd
import os

#importing csv file
path = os.path.join(os.path.dirname(__file__),'data/final_resto_list.csv')
df = pd.read_csv(path,index_col=0)

#creating unique categories list
liste_cat = list(df['categories'].str.split(', ', expand=False))
categories = set([item for sublist in liste_cat for item in sublist])

#creating price_range dict

price_range={
    '€':1,
    '€€':2,
    '€€€':3,
    '€€€€':4
}

#creating arrondissement dict


def selector(k):
    if k == 1 | k == 11:
        return 'st'
    if k == 2 | k == 12:
        return 'nd'
    if k == 3 | k == 13:
        return 'rd'
    return 'st'


arrondissements = {str(k) + selector(k): 75000 + k for k in range(1, 21)}
