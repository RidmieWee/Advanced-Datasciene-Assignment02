# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 17:33:38 2023

@author: Ridmi Weerakotuwa
"""

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# create function for read file
def read_climate_data(filename):
    """
    This function reads climate change data file included in World
    Bank climate data and returns two dataframes:
    one with years as columns and one with countries as columns.
    """

    # read data from csv
    df_data = pd.read_csv(filename, skiprows=4)

    # create a new dataframe to filter five usefull indicators
    df_climate_change = df_data[
        (df_data["Indicator Name"] == "Population growth (annual %)") |
        (df_data["Indicator Name"] == "Forest area (sq. km)") |
        (df_data["Indicator Name"] == "CO2 emissions (kt)") |
        (df_data["Indicator Name"] == "Agricultural land (sq. km)") |
        (df_data["Indicator Name"] == "Access to electricity (% of population)")
        ].reset_index(drop=True)

    # drop all unnecessary columns
    df_climate_change = df_climate_change.drop(['Indicator Code',
                                                'Unnamed: 66',
                                                '2020',
                                                '2021'], axis=1)

    # drop the years between 1960 to 1990
    df_climate_change = df_climate_change.drop(df_climate_change.iloc[:, 3:33],
                                               axis=1)

    # create a dataframe to get years as columns
    df_year = df_climate_change.copy()

    # remove all NaNs to clean the dataframe
    df_year = df_climate_change.dropna(axis=0)

    # set the country name as index
    df_climate_change = df_climate_change.set_index('Country Name')

    # transpose the dataframe to get countries as columns
    df_country = df_climate_change.transpose()

    # clean the transposed dataframe
    df_country = df_country.dropna(axis=1)

    # return both year and country dataframes
    return df_year, df_country


# function to compare statistical properties of each indicators per state
def individual_country_statisctic(country_name):
    """
    This function get the country name as an argument and produce the
    comparison of the statistical properties of indicators for given country
    """

    # extract the given country data
    df_state = df_country[country_name]

    # use iloc to extract columns for new df
    df_cols = df_state.iloc[1]

    # take the data less the header row
    df_state = df_state[2:]

    # assign new columns to the df
    df_state.columns = df_cols

    # convert data types to numeric
    df_state = df_state.apply(pd.to_numeric, errors='coerce')

    # extract statistical properties
    df_describe = df_state.describe().round(2)

    # extract column headers
    cols = df_describe.columns

    # get the half of length of ech column
    lencols = [int(len(c)/2) for c in cols]

    # get column names into 2 lines based on the length of each column
    df_describe.columns = pd.MultiIndex.from_tuples(tuple((c[:ln], c[ln:])
                                                          for c, ln in zip(
                                                                  cols,
                                                                  lencols)
                                                          ))

    # print the statistics
    print('========== The summary statistics for', country_name, '===========')
    print('\n')
    print(df_describe)
    print('==================================================================')
    print('\n')

    # return the statistics for each country
    return


def individual_indicator_statistics(indicator_name):
    """
    This function get the indicator name as an argument and produce the
    comparison of the statistical properties of countries for given indicator
    """

    # extract given indicatordata
    df_indicator = df_year[df_year['Indicator Name'] == indicator_name]

    # drop unneccesary columns
    df_indicator = df_indicator.drop(["Country Code", "Indicator Name"],
                                     axis=1)

    # extract the useful countries for further analysis
    df_indicator = df_indicator[
        (df_indicator["Country Name"] == "Brazil") |
        (df_indicator["Country Name"] == "China") |
        (df_indicator["Country Name"] == "Germany") |
        (df_indicator["Country Name"] == "India") |
        (df_indicator["Country Name"] == "United States")
        ].reset_index(drop=True)

    # set the country name as index
    df_indicator = df_indicator.set_index("Country Name")

    # transpose the df
    df_indicator = df_indicator.T

    # extract statistical properties
    df_describe = df_indicator.describe().round(2)

    # print the statistics
    print('========= The summary statistics for', indicator_name, '==========')
    print('\n')
    print(df_describe)
    print('==================================================================')
    print('\n')

    # return the statistics for each country
    return


# call the function for read file and generate 2 dataframes
df_year, df_country = read_climate_data("Climate.csv")

# call the function to extract stat properties of each indicator per state
individual_country_statisctic('Brazil')
individual_country_statisctic('Germany')
individual_country_statisctic('United States')

# call the function to extract stat properties of each country per indicator
individual_indicator_statistics("Population growth (annual %)")
individual_indicator_statistics("Forest area (sq. km)")
individual_indicator_statistics("CO2 emissions (kt)")
individual_indicator_statistics("Agricultural land (sq. km)")
individual_indicator_statistics("Access to electricity (% of population)")
