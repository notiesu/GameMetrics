import pandas as pd
import numpy as np
import re


from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime


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


""" Reading the excel file into a pandas dataframe"""
data = pd.read_excel("Soccer:Football/DataSets/all_goalkeepers.xlsx")

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
clean_data.to_excel("Soccer:Football/DataSets/cleaned_all_goalkeepers.xlsx")

clean_data = pd.read_excel("Soccer:Football/DataSets/cleaned_all_goalkeepers.xlsx")


""" Cleaned data has 616 observations"""
print(clean_data.info())
print(data.info())