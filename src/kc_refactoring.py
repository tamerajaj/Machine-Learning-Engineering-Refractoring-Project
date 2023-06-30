# Basic imports
import pandas as pd
import numpy as np


# Machine Learning libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin


# Data Preparation
def bath_bed_ratio_outlier(df):
    df = df.copy()
    df["bath_bed_ratio"] = df["bathrooms"] / df["bedrooms"]
    for idx, ratio in enumerate(df["bath_bed_ratio"]):
        if ratio >= 2:
            df.drop(idx, inplace=True)
        elif ratio <= 0.10:
            df.drop(idx, inplace=True)
    return df


def sqft_basement(df):
    df = df.copy()
    df["sqft_basement"] = df["sqft_basement"].replace("?", np.nan)
    df["sqft_basement"] = df["sqft_basement"].astype(float)
    df["sqft_basement"] = df["sqft_living"] - df["sqft_above"]
    return df


def fill_missings_view_wf(df):
    df = df.copy()
    df["view"] = df["view"].fillna(0)
    df["waterfront"] = df["waterfront"].fillna(0)
    return df


def calculate_last_change(df):
    df = df.copy()
    last_known_change = []
    for idx, yr_re in df.yr_renovated.items():
        if str(yr_re) == "nan" or yr_re == 0.0:
            last_known_change.append(df.yr_built[idx])
        else:
            last_known_change.append(int(yr_re))
    df["last_known_change"] = last_known_change
    df.drop("yr_renovated", axis=1, inplace=True)
    df.drop("yr_built", axis=1, inplace=True)
    return df


# Feature Engineering
def calculate_sqft_price(df):
    df = df.copy()
    df["sqft_price"] = (df.price / (df.sqft_living + df.sqft_lot)).round(2)
    return df


def calculate_distance_to_wealth_center(df):
    df = df.copy()
    # Absolute difference of latitude between centre and property
    df["delta_lat"] = np.absolute(47.62774 - df["lat"])
    # Absolute difference of longitude between centre and property
    df["delta_long"] = np.absolute(-122.24194 - df["long"])
    # Distance between centre and property
    df["center_distance"] = (
        ((df["delta_long"] * np.cos(np.radians(47.6219))) ** 2 + df["delta_lat"] ** 2)
        ** (1 / 2)
        * 2
        * np.pi
        * 6378
        / 360
    )
    return df


def calculate_distance_to_beach_promenade(df):
    df = df.copy()

    # Filter the dataframe to include only waterfront locations
    water_locations = df[df["waterfront"] == 1][["long", "lat"]].values

    # Get the coordinates of all points
    points = df[["long", "lat"]].values

    # Calculate the differences in longitude and latitude
    delta_long = points[:, 0][:, np.newaxis] - water_locations[:, 0]
    delta_lat = points[:, 1][:, np.newaxis] - water_locations[:, 1]

    # Apply correction to longitude differences based on latitude
    delta_long_corr = delta_long * np.cos(np.radians(water_locations[:, 1]))

    # Calculate the distances using the Haversine formula
    distances = np.sqrt(delta_long_corr**2 + delta_lat**2) * 2 * np.pi * 6378 / 360

    # Find the minimum distance to waterfront for each point
    water_distance = np.min(distances, axis=1)

    # Add the water distance column to the dataframe
    df["water_distance"] = water_distance

    return df
