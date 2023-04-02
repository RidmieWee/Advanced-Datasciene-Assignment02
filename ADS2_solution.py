# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 17:33:38 2023

@author: Ridmi Weerakotuwa
"""

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

from scipy.stats import skew, kurtosis


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
        (df_data["Indicator Name"] ==
         "Renewable energy consumption (% of total final energy consumption)")
    ].reset_index(drop=True)

    df_climate_change["Indicator Name"] = df_climate_change["Indicator Name"].replace(
        ["Population growth (annual %)",
         "Forest area (sq. km)",
         "CO2 emissions (kt)",
         "Agricultural land (sq. km)",
         "Renewable energy consumption (% of total final energy consumption)"],
        ["Population growth(%)",
         "Forest area(km^2)",
         "CO2 emissions(kt)",
         "Agricultural land(km^2)",
         "Renew. energy consump(%)"])

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


# function to extract data for specific countries
def extract_country_data(country_name):
    """
    This function get the country name as an argument and create a new
    dataframe with data of given country
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

    # return the dataframe
    return df_state


# function to compare statistical properties of each indicators per state
def individual_country_statisctic(country_name):
    """
    This function get the country name as an argument and produce the
    comparison of the statistical properties of indicators for given country
    """

    # call thefunction to create country dataframe
    df_state = extract_country_data(country_name)

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
individual_indicator_statistics("Population growth(%)")
individual_indicator_statistics("Forest area(km^2)")
individual_indicator_statistics("CO2 emissions(kt)")
individual_indicator_statistics("Agricultural land(km^2)")
individual_indicator_statistics("Renew. energy consump(%)")

# extrcact useful countries
df_Brazil = extract_country_data('Brazil')
df_Germany = extract_country_data('Germany')
df_USA = extract_country_data('United States')

# assign the columns into new dataframe
df_bcols = df_Brazil.columns
df_gcols = df_Germany.columns
df_ucols = df_USA.columns

# find the skewness, round it to 2 decimals and put it into dictionary
brazil_skew = df_Brazil.apply(skew).round(2).to_dict()
Germany_skew = df_Germany.apply(skew).round(2).to_dict()
USA_skew = df_USA.apply(skew).round(2).to_dict()

# find the kutosis, round it to 2 decimals and put it into dictionary
brazil_kurtosis = df_Brazil.apply(kurtosis).round(2).to_dict()
Germany_kurtosis = df_Germany.apply(kurtosis).round(2).to_dict()
USA_kurtosis = df_USA.apply(kurtosis).round(2).to_dict()

# ignore warning
warnings.filterwarnings("ignore", message="Precision loss occurred in moment\
                        calculation due to catastrophic cancellation")

# create dictionary to store summary statistics
stats = {
    ("Variance", "Brazil"): {
        c: round(np.var(df_Brazil[c]), 2) for c in df_bcols
    },
    ("Variance", "Germany"): {
        c: round(np.var(df_Germany[c]), 2) for c in df_gcols
    },
    ("Variance", "USA"): {
        c: round(np.var(df_USA[c]), 2) for c in df_ucols
    },
    ("Skewness", "Brazil"): brazil_skew,
    ("Skewness", "Germany"): Germany_skew,
    ("Skewness", "USA"): USA_skew,
    ("Kutosis", "Brazil"): brazil_kurtosis,
    ("Kutosis", "Germany"): Germany_kurtosis,
    ("Kutosis", "USA"): USA_kurtosis
}

# assign statistics into a dataframe
df_statistics = pd.DataFrame(stats)

# print the summary statistics
print(df_statistics)

# create a df with usufull countries
df_countries = ["Brazil", "China", "Germany", "India", "United States"]

# create a loop to iterate over countries df
for c in df_countries:

    # extract the country data
    df_country1 = extract_country_data(c)

    # calculate the correlation
    df_corr = df_country1.corr()

    # print all correlation matrices
    print("Correlation matrix for indicators in",
          c, ":", "\n", "\n", df_corr, "\n")
