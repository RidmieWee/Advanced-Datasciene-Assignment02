# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 17:33:38 2023

@author: Ridmi Weerakotuwa
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_climate_data(filename, metadata):

    # read each indicator data from csv
    df_data = pd.read_csv(filename, header = 2)

    # read metadata sv file
    df_meta = pd.read_csv(metadata)

    # clean the df_data columns with all NaNs
    df_data = df_data.dropna(axis=1, how='all')

    # drop unnecessary columns in df_data
    df_data = df_data.drop(['Indicator Code'], axis=1)

    # clean the rows with NaNs in df_data
    df_data = df_data.dropna()

    # filter the required columns
    df_meta = df_meta[['Country Code', 'Region', 'IncomeGroup']]

    # clean the df_meta data frame
    df_meta = df_meta.dropna()

    # merge the dataframes based on the country code
    df_year = pd.merge(df_data, df_meta, on='Country Code', how='inner')

    # set the country name as index
    df_countries = df_year.set_index('Country Name')

    # transpose the data to have countries as columns
    df_countries = df_countries.transpose()

    # clean the transposed dataframe
    df_countries = df_countries.dropna()

    # return both the original and transposed dataframes
    return df_year, df_countries

df_year, df_countries = read_climate_data("Access to electricity.csv", "metadata.csv")
