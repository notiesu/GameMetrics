#IMPORTS
import pandas as pd
import numpy as np
import re


from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime

################################################################

#DEFINES CHANGE AS NEEDED
RAW_GK_XLSX_PATH = "./DataSets/all_goalkeepers.xlsx"
CLEAN_GK_XLSX_PATH = "./DataSets/cleaned_all_goalkeepers.xlsx"

"""
GP - Games Played
GS - Games Started
MINS - Minutes Played
SHTS - Shots
SV - Saves
GA - Goals Allowed
GAA - Goals Against Average
PKG/A - Penalty Kicks Goals/Attempts
W - Wins
L - Losses
T - Ties
ShO - Shutouts
W% - Winning Percentage
Sv% - Save Percentage
Year - Year
Season - Season
"""

""" ------------------------------------------GOAL KEEPERS DATA------------------------------------------ """

""" Reading the excel file into a pandas dataframe"""
data = pd.read_excel(RAW_GK_XLSX_PATH)

""" Converting column to strings"""
data["PKG/A"] = data["PKG/A"].astype(str)


""" Function to remove zeroes from a column"""


def remove_zeroes(dataframe, column_name):
    return dataframe[dataframe[column_name] != "0/0"]


""" Function to convert the date into the properly formatted fraction"""


def convert_date_string_to_fraction(value):
    if isinstance(value, str) and re.match(r"\d{4}-\d{2}-\d{2}", value):
        date_part = value[:10]
        date_obj = datetime.strptime(date_part, "%Y-%m-%d")
        return f"{date_obj.month}/{date_obj.day}"
    elif pd.isnull(value):
        return "0/0"
    else:
        return value


""" Function to convert the PKG/A to decimal form"""


def convert_fraction_to_decimal(fraction_str):
    try:
        numerator, denominator = fraction_str.split("/")
        return float(numerator) / float(denominator)
    except ValueError:
        return None


""" Applying the function to the column and verifying the results after removing the zeroes"""
data = remove_zeroes(data, "PKG/A")
data["PKG/A"] = data["PKG/A"].apply(convert_date_string_to_fraction)
print(data["PKG/A"].head())


""" Creating a cleaned file without NA values"""

clean_data = data.dropna()
clean_data["PKG/A"] = clean_data["PKG/A"].apply(convert_fraction_to_decimal)
clean_data.to_excel(CLEAN_GK_XLSX_PATH)

clean_data = pd.read_excel(CLEAN_GK_XLSX_PATH)


""" Cleaned data has 616 observations"""
print(clean_data.info())
print(data.info())

""" Finding Outliers"""

""" Function for Displaying boxplots with outliers in red with their numbered index"""


def boxplots(dataframe):
    num_cols = dataframe.select_dtypes(include=["number"]).columns.tolist()
    for col in num_cols:
        plt.figure(figsize=(10, 6))
        bp = plt.boxplot(
            dataframe[col].dropna(), flierprops=dict(markerfacecolor="r", marker="o")
        )

        for flier in bp["fliers"]:
            y = flier.get_ydata()
            x = flier.get_xdata()
            for i in range(len(y)):

                plt.text(
                    x[i],
                    y[i],
                    f"{dataframe[col][dataframe[col] == y[i]].index[0]}",
                    color="blue",
                )

        plt.title(col)
        plt.show()


""" Display the box plots"""
boxplots(clean_data)

""" Function to remove the outliers"""


def remove_outliers(dataframe):
    indices_to_drop = set()
    num_cols = dataframe.select_dtypes(include=["number"]).columns.tolist()

    for col in num_cols:
        Q1 = dataframe[col].quantile(0.25)
        Q3 = dataframe[col].quantile(0.75)
        IQR = Q3 - Q1
        outlier_indices = dataframe[
            (dataframe[col] < (Q1 - 1.5 * IQR)) | (dataframe[col] > (Q3 + 1.5 * IQR))
        ].index
        indices_to_drop.update(outlier_indices)

    cleaned_dataframe = dataframe.drop(index=list(indices_to_drop))
    return cleaned_dataframe


""" Removing and viewing results"""
clean_data_no_outliers = remove_outliers(clean_data)
print(clean_data_no_outliers)

""" 513 entries"""
clean_data_no_outliers.info()
""" ------------------------------------------MATCHES DATA------------------------------------------ """
# print("Matches Data ------------------------------------")
# data = pd.read_excel("Soccer:Football/DataSets/matches.xlsx")


# print("Cleaned Matches ----- ")
# clean_matches_data = data.dropna(thresh=len(data.columns) - 75)
# clean_matches_data.info()

# clean_matches_data.to_excel("Soccer:Football/DataSets/cleaned_matches.xlsx")
# missing_info = clean_matches_data.isnull().sum() / len(data)
# print(missing_info)
