# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 17:33:38 2023

@author: Ridmi Weerakotuwa
"""

# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from scipy.stats import skew, kurtosis


# =============================================================================
# This senction consist of all the functions
# =============================================================================


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
        (df_data["Indicator Name"] == "Urban population") |
        (df_data["Indicator Name"] == "Forest area (% of land area)") |
        (df_data["Indicator Name"] == "CO2 emissions (metric tons per capita)") |
        (df_data["Indicator Name"] == "Arable land (% of land area)") |
        (df_data["Indicator Name"] ==
         "Renewable energy consumption (% of total final energy consumption)")
    ].reset_index(drop=True)

    df_climate_change["Indicator Name"] = df_climate_change["Indicator Name"].replace(
        ["Urban population",
         "Forest area (% of land area)",
         "CO2 emissions (metric tons per capita)",
         "Arable land (% of land area)",
         "Renewable energy consumption (% of total final energy consumption)"],
        ["Urban population",
         "Forest area(%)",
         "CO2 emissions(mt)",
         "Arable land(%)",
         "Renew. energy consump(%)"])

    # drop all unnecessary columns
    df_climate_change = df_climate_change.drop(["Indicator Code",
                                                "Unnamed: 66",
                                                "2020",
                                                "2021"], axis=1)

    # drop the years between 1960 to 1990
    df_climate_change = df_climate_change.drop(df_climate_change.iloc[:, 3:33],
                                               axis=1)

    # create a dataframe to get years as columns
    df_year = df_climate_change.copy()

    # remove all NaNs to clean the dataframe
    df_year = df_climate_change.dropna(axis=0)

    # set the country name as index
    df_climate_change = df_climate_change.set_index("Country Name")

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
    df_state = df_state.apply(pd.to_numeric, errors="coerce")

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
    print("========== The summary statistics for", country_name, "===========")
    print("\n")
    print(df_describe)
    print("==================================================================")
    print("\n")

    # return the statistics for each country
    return


# function to compare statistical properties of each countries per indicator
def individual_indicator_statistics(indicator_name):
    """
    This function get the indicator name as an argument and produce the
    comparison of the statistical properties of countries for given indicator
    """

    # extract given indicatordata
    df_indicator = df_year[df_year["Indicator Name"] == indicator_name]

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
    print("========= The summary statistics for", indicator_name, "==========")
    print("\n")
    print(df_describe)
    print("==================================================================")
    print("\n")

    # return the statistics for each country
    return


# function to get correlation over time
def correlation_per_year(country_name):
    """
    This function get the country name as an argument and produce the
    correlation over time for selected indicators
    """

    # define the window size
    window_size = 5

    # extract the country data
    df_data = df_countries[df_countries["Country Name"] == country_name]

    # filter the dataframe for the indicators you want to analyze
    indicators = ['Urban population',
                  'Forest area(%)',
                  'CO2 emissions(mt)',
                  'Forest area(%)',
                  'Arable land(%)']

    df_filtered = df_data[df_data['Indicator Name'].isin(indicators)]

    df_filtered['Year'] = df_filtered['Year'].astype(int)

    # pivot the dataframe to have year as index and indicators as columns
    df_pivot = df_filtered.pivot(index='Year',
                                 columns='Indicator Name',
                                 values='Total')

    # calculate the correlation matrix for each rolling window
    corr_matrix_over_time = df_pivot.rolling(window_size).corr()

    # select only the correlations between different indicators
    corr_matrix_over_time = corr_matrix_over_time.unstack().iloc[:,
                                                                 window_size-4::window_size]

    # drop null values
    corr_matrix_over_time.dropna()

    # print the result
    print(corr_matrix_over_time)

    # end the function
    return


# function to create multiple line charts for CO2 emmission
def plt_co2_emission_line_chart(df):
    """ This ia a function to create a lineplot with multiple lines.
    This function takes datafrme as an argument, and use year as x axis
    and the total CO2 emission as y axis and plot lines for each country"""

    # create dataframes for countries
    df_brazil = df[df["Country Name"] == "Brazil"]
    df_germany = df[df["Country Name"] == "Germany"]
    df_china = df[df["Country Name"] == "China"]
    df_india = df[df["Country Name"] == "India"]
    df_USA = df[df["Country Name"] == "United States"]
    df_UK = df[df["Country Name"] == "United Kingdom"]

    # make the figure
    plt.figure()

    # use multiple x and y for plot multiple lines
    plt.plot(df_brazil["Year"], df_brazil["Total"], label="Brazil")
    plt.plot(df_china["Year"], df_china["Total"], label="China")
    plt.plot(df_germany["Year"], df_germany["Total"], label="Germany")
    plt.plot(df_india["Year"], df_india["Total"], label="India")
    plt.plot(df_USA["Year"], df_USA["Total"], label="USA")
    plt.plot(df_UK["Year"], df_UK["Total"], label="UK")

    # labeling
    plt.xlabel("Year", labelpad=(10), fontweight="bold")
    plt.ylabel("CO2 emissions (mt)", labelpad=(10), fontweight="bold")

    # add a title and legend
    plt.title("Total CO2 emissions by country ", fontweight="bold", y=1.1)
    plt.legend(loc='center left',
               bbox_to_anchor=(1, 0.5),
               fancybox=True,
               shadow=True)

    plt.xticks(rotation=90)

    # save the plot as png
    plt.savefig("CO2_line_chart.png")

    # show the plot
    plt.show()

    # end the function
    return


# function to create multiple line charts for urban population
def plot_urban_pop_line_chart(df):
    """ This ia a function to create a lineplot with multiple lines.
    This function takes datafrme as an argument, and use year as x axis
    and the total urban population n as y axis and plot lines for each country"""

    # create dataframes for countries
    df_brazil = df[df["Country Name"] == "Brazil"]
    df_germany = df[df["Country Name"] == "Germany"]
    df_china = df[df["Country Name"] == "China"]
    df_india = df[df["Country Name"] == "India"]
    df_USA = df[df["Country Name"] == "USA"]
    df_UK = df[df["Country Name"] == "UK"]

    # make the figure
    plt.figure()

    # use multiple x and y for plot multiple lines
    plt.plot(df_brazil["Year"], df_brazil["Total"], label="Brazil")
    plt.plot(df_china["Year"], df_china["Total"], label="China")
    plt.plot(df_germany["Year"], df_germany["Total"], label="Germany")
    plt.plot(df_india["Year"], df_india["Total"], label="India")
    plt.plot(df_USA["Year"], df_USA["Total"], label="USA")
    plt.plot(df_UK["Year"], df_UK["Total"], label="UK")

    # labeling
    plt.xlabel("Year", labelpad=(10), fontweight="bold")
    plt.ylabel("Population", labelpad=(10), fontweight="bold")

    # add a title and legend
    plt.title("Urban population by country ", fontweight="bold", y=1.1)
    plt.legend()

    plt.xticks(rotation=90)

    # save the plot as png
    plt.savefig("Urb_line_chart.png")

    # show the plot
    plt.show()

    # end the function
    return


# create a function for plot bar chart
def plot_renew_energy_bar_graph(df):
    """ This ia a function to create a grouped bar chart.
    This function takes datafrme as anargument, and plot
    multiple bars grouped by country. """

    # create dataframes for plot bar graph
    df_1990 = df[df["Year"] == "1990"]
    df_1995 = df[df["Year"] == "1995"]
    df_2000 = df[df["Year"] == "2000"]
    df_2005 = df[df["Year"] == "2005"]
    df_2010 = df[df["Year"] == "2010"]
    df_2015 = df[df["Year"] == "2015"]

    # make the figure
    plt.figure()

    # create the position of bars
    x_pos = np.arange(len(df_1990))

    # create x labels
    tick_labels = ["Australia", "Brazil", "Canada",
                   "China", "Germny", "India", "Japan", "UK", "USA"]

    # plot the bars
    plt.bar(x_pos - 0.2,
            df_1990["Total"],
            width=0.1,
            label="1990",
            color="#0b84a5")
    plt.bar(x_pos - 0.1,
            df_1995["Total"],
            width=0.1,
            label="1995",
            color="#f6c85f")
    plt.bar(x_pos,
            df_2000["Total"],
            width=0.1,
            label="2000",
            color="#9dd866")
    plt.bar(x_pos + 0.1,
            df_2005["Total"],
            width=0.1,
            label="2005",
            color="#ca472f")
    plt.bar(x_pos + 0.2,
            df_2010["Total"],
            width=0.1,
            label="2010",
            color="#8dddd0")
    plt.bar(x_pos + 0.3,
            df_2015["Total"],
            width=0.1,
            label="2015",
            color="#6f4e7c")

    # labeling
    plt.xlabel("Country", labelpad=(10), fontweight="bold")
    plt.ylabel("Renewable energy consumption(% energy consump.)",
               fontsize=(8), labelpad=(10), fontweight="bold")
    plt.xticks(x_pos, tick_labels, rotation=90)

    # add the title and legends
    plt.title("Renewable energy consumption by country",
              fontweight="bold", y=1.1)
    plt.legend()

    # save the figure as png
    plt.savefig("renew_energy_bar_chart.png")

    # show the plot
    plt.show()

    # end the function
    return


# function to create multiple line charts for forest area
def plot_forest_area_line_chart(df):
    """ This ia a function to create a lineplot with multiple lines.
    This function takes datafrme as an argument, and use year as x axis
    and the total forest area as y axis and plot dashed lines for each country"""

    # create dataframes for countries
    df_aus = df[df["Country Name"] == "Australia"]
    df_brazil = df[df["Country Name"] == "Brazil"]
    df_canada = df[df["Country Name"] == "Canada"]
    df_china = df[df["Country Name"] == "China"]
    df_germany = df[df["Country Name"] == "Germany"]
    df_india = df[df["Country Name"] == "India"]
    df_japan = df[df["Country Name"] == "Japan"]
    df_USA = df[df["Country Name"] == "United States"]
    df_UK = df[df["Country Name"] == "United Kingdom"]

    # make the figure
    plt.figure()

    # use multiple x and y for plot multiple lines
    plt.plot(df_aus["Year"], df_aus["Total"],
             linestyle='dashed', label="Australia")
    plt.plot(df_brazil["Year"], df_brazil["Total"],
             linestyle='dashed', label="Brazil")
    plt.plot(df_canada["Year"], df_canada["Total"],
             linestyle='dashed', label="Canada")
    plt.plot(df_china["Year"], df_china["Total"],
             label="China")
    plt.plot(df_germany["Year"], df_germany["Total"],
             linestyle='dashed', label="Germany")
    plt.plot(df_india["Year"], df_india["Total"],
             linestyle='dashed', label="India")
    plt.plot(df_japan["Year"], df_japan["Total"],
             linestyle='dashed', label="Japan")
    plt.plot(df_USA["Year"], df_USA["Total"], label="USA")
    plt.plot(df_UK["Year"], df_UK["Total"], linestyle='dashed', label="UK")

    # labeling
    plt.xlabel("Year", labelpad=(10), fontweight="bold")
    plt.ylabel("Forest area (%)", labelpad=(10), fontweight="bold")

    # add a title and legend
    plt.title("Total forest area by country ", fontweight="bold", y=1.1)
    plt.legend(loc='center left',
               bbox_to_anchor=(1, 0.5),
               fancybox=True,
               shadow=True)

    plt.xticks(rotation=90)

    # save the plot as png
    plt.savefig("forest_line_chart.png")

    # show the plot
    plt.show()

    # end the function
    return


# function to create multiple line charts for CO2 emmission
def plot_arable_land_line_chart(df):
    """ This ia a function to create a lineplot with multiple lines.
    This function takes datafrme as an argument, and use year as x axis
    and the total aggri. land as y axis and plot dashed lines for each country"""

    # create dataframes for countries
    df_aus = df[df["Country Name"] == "Australia"]
    df_brazil = df[df["Country Name"] == "Brazil"]
    df_canada = df[df["Country Name"] == "Canada"]
    df_china = df[df["Country Name"] == "China"]
    df_germany = df[df["Country Name"] == "Germany"]
    df_india = df[df["Country Name"] == "India"]
    df_japan = df[df["Country Name"] == "Japan"]
    df_USA = df[df["Country Name"] == "United States"]
    df_UK = df[df["Country Name"] == "United Kingdom"]

    # make the figure
    plt.figure()

    # use multiple x and y for plot multiple lines
    plt.plot(df_aus["Year"], df_aus["Total"],
             linestyle='dashed', label="Australia")
    plt.plot(df_brazil["Year"], df_brazil["Total"],
             linestyle='dashed', label="Brazil")
    plt.plot(df_canada["Year"], df_canada["Total"],
             linestyle='dashed', label="Canada")
    plt.plot(df_china["Year"], df_china["Total"], label="China")
    plt.plot(df_germany["Year"], df_germany["Total"],
             linestyle='dashed', label="Germany")
    plt.plot(df_india["Year"], df_india["Total"],
             linestyle='dashed', label="India")
    plt.plot(df_japan["Year"], df_japan["Total"],
             linestyle='dashed', label="Japan")
    plt.plot(df_USA["Year"], df_USA["Total"], label="USA")
    plt.plot(df_UK["Year"], df_UK["Total"], linestyle='dashed', label="UK")

    # labeling
    plt.xlabel("Year", labelpad=(10), fontweight="bold")
    plt.ylabel("Arable land (%)", labelpad=(10), fontweight="bold")

    # add a title and legend
    plt.title("Total arable land by country ", fontweight="bold", y=1.1)
    plt.legend(loc='center left',
               bbox_to_anchor=(1, 0.5),
               fancybox=True,
               shadow=True)

    plt.xticks(rotation=90)

    # save the plot as png
    plt.savefig("arable_line_chart.png")

    # show the plot
    plt.show()

    # end the function
    return


def plot_heat_map(country_name):
    """ This ia a function to create a heatmap for country specific indicators.
    This function takes country as an argument, and use plot correlation between indicators"""

    # extract the given country data
    df_data = extract_country_data(country_name)

    # create correlation matrix
    corr_matrix = df_data.corr()

    # plot heatmap
    sns.heatmap(corr_matrix, cmap='coolwarm', annot=True)

    # rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45)

    # set the plot title
    plt.title('Correlation between Indicators in ' +
              country_name, fontweight="bold", y=1.05)
    plt.xlabel("")
    plt.ylabel("")

    # save the plot as png
    plt.savefig("heat_map.png")

    # show the plot
    plt.show()

    # end the function
    return


def plot_heat_map2(country_name):
    """ This ia a function to create a heatmap for country specific indicators.
    This function takes country as an argument, and use plot correlation between indicators"""

    # extract the given country data
    df_data = extract_country_data(country_name)

    # create correlation matrix
    corr_matrix = df_data.corr()

    # plot heatmap
    sns.heatmap(corr_matrix, cmap='YlGnBu', annot=True)

    # rotate the x-axis labels by 45 degrees
    plt.xticks(rotation=45)

    # set the plot title
    plt.title('Correlation between Indicators in ' +
              country_name, fontweight="bold", y=1.05)
    plt.xlabel("")
    plt.ylabel("")

    # save the plot as png
    plt.savefig("heat_map2.png")

    # show the plot
    plt.show()

    # end the function
    return


# =============================================================================
# This section is the main program of this code. In here all the pre
# processing requirements and calling functions done
# =============================================================================


# call the function for read file and generate 2 dataframes
df_year, df_country = read_climate_data("Climate.csv")

# call the function to extract stat properties of each indicator per state
individual_country_statisctic("Brazil")
individual_country_statisctic("Germany")
individual_country_statisctic("United States")

# call the function to extract stat properties of each country per indicator
individual_indicator_statistics("Urban population")
individual_indicator_statistics("Forest area(%)")
individual_indicator_statistics("CO2 emissions(mt)")
individual_indicator_statistics("Arable land(%)")
individual_indicator_statistics("Renew. energy consump(%)")

# extrcact useful countries
df_Brazil = extract_country_data("Brazil")
df_Germany = extract_country_data("Germany")
df_USA = extract_country_data("United States")

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

# transform the df_year dataframe seperate years columns into one year column
df_year_new = pd.melt(df_year,
                      id_vars=["Country Name",
                               "Country Code",
                               "Indicator Name"
                               ],
                      value_vars=df_year.iloc[:, 3:-1].columns,
                      var_name="Year",
                      value_name=("Total"))

# explore the new dataframe
print(df_year_new.head())

# create a list of countrues for further analysis
countries = ["Australia", "Brazil", "Canada", "China",
             "Germany", "India", "Japan", "United Kingdom", "United States"]

# crete new dataframe with reuqired country data
df_countries = df_year_new.groupby(
    'Country Name').filter(lambda x: x.name in countries)

# extract data for co2 emission
df_countries_co2 = df_countries[df_countries["Indicator Name"]
                                == "CO2 emissions(mt)"]

# explore new dataframe
print(df_countries_co2.head())

# extract data for population growth
df_countries_urb_pop = df_countries[
    df_countries["Indicator Name"] == "Urban population"
]

# change some country names into aabbreviations
df_countries_urb_pop.loc[df_countries_urb_pop["Country Name"]
                         == "United States", "Country Name"] = "USA"
df_countries_urb_pop.loc[df_countries_urb_pop["Country Name"]
                         == "United Kingdom", "Country Name"] = "UK"


# explore new dataframe
print(df_countries_urb_pop.head())

# extrace data for renew. energy comsump.
df_countries_renew_energy = df_countries[
    df_countries['Indicator Name'] == "Renew. energy consump(%)"
].sort_values(by="Country Name", ascending=True)

# explore new dataframe
print(df_countries_renew_energy.head())

# extrace data for forest area
df_countries_forest = df_countries[df_countries["Indicator Name"]
                                   == "Forest area(%)"]

# explore new dataframe
print(df_countries_forest.head())

# extrace data for aggricultural land
df_countries_arable = df_countries[df_countries["Indicator Name"] ==
                                   "Arable land(%)"]

# explore new dataframe
print(df_countries_arable)

# call function to create CO2 emission multiple line chart
plt_co2_emission_line_chart(df_countries_co2)

# call function to create population growth boxplots
plot_urban_pop_line_chart(df_countries_urb_pop)

# call function to create renew. energy consumption bar charts
plot_renew_energy_bar_graph(df_countries_renew_energy)

# call function to create forest area multiple dashed line charts
plot_forest_area_line_chart(df_countries_forest)

# call function to create forest area multiple dashed line charts
plot_arable_land_line_chart(df_countries_arable)

# call the function to create correlation heatmap for china and USA
plot_heat_map("China")
plot_heat_map2("United States")
