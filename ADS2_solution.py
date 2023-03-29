# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 17:33:38 2023

@author: Ridmi Weerakotuwa
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_climate_data(filename):
    """
    This function reads indicator specific csv file and metadata file in World
    Bank climate data and returns two dataframes:
    one with years as columns and one with countries as columns.
    """

    # read data from csv
    df_data = pd.read_csv(filename, skiprows = 4)

    # create a new dataframe to filter five usefull indicators
    df_climate_change = df_data[
        (df_data["Indicator Name"] == "Population growth (annual %)") |
        (df_data["Indicator Name"] == "Forest area (sq. km)") |
        (df_data["Indicator Name"] == "CO2 emissions (kt)") |
        (df_data["Indicator Name"] == "Agricultural land (% of land area)") |
        (df_data["Indicator Name"] == "Access to electricity (% of population)")
        ].reset_index(drop = True)

    # drop all unnecessary columns
    df_climate_change = df_climate_change.drop(['Indicator Code',
                                                'Unnamed: 66',
                                                '2020',
                                                '2021'], axis = 1)

    # drop the years between 1960 to 1990
    df_climate_change = df_climate_change.drop(df_climate_change.iloc[:, 3:33],
                                               axis = 1)

    # create a dataframe to get years as columns
    df_year = df_climate_change.copy()

    # remove all NaNs to clean the dataframe
    df_year = df_climate_change.dropna(axis = 0)

    # set the country name as index
    df_climate_change = df_climate_change.set_index('Country Name')

    # transpose the dataframe to get countries as columns
    df_country = df_climate_change.transpose()

    # clean the transposed dataframe
    df_country = df_country.dropna(axis = 1)

    # return both year and country dataframes
    return df_year, df_country

df_year, df_country = read_climate_data("Climate.csv")

print(df_year)
# extract 5 countries for statistical analysis
#df_countries = df_country[["Brazil","United States"]]
