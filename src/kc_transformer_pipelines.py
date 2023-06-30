from sklearn.base import BaseEstimator, TransformerMixin  # type: ignore
import numpy as np
import pandas as pd


class KingCountyTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, kc_transform_function):
        self.kc_transform_function = kc_transform_function

    def fit(self, X: pd.DataFrame, y=None):
        return self


class BathRatioTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=self.bath_bed_ratio_outlier)

    def transform(self, X: pd.DataFrame, y=None):
        # add your code here!
        # TRANSFER TO SOLUTION NOTEBOOK
        X = X.copy()
        X = self.kc_transform_function(X)
        return X

    def bath_bed_ratio_outlier(self, df: pd.DataFrame):
        df = df.copy()
        df["bath_bed_ratio"] = df["bathrooms"] / df["bedrooms"]
        for idx, ratio in enumerate(df["bath_bed_ratio"]):
            if ratio >= 2:
                df.drop(idx, inplace=True)
            elif ratio <= 0.10:
                df.drop(idx, inplace=True)
        return df


class SqftBasementTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=self.sqft_basement)

    def transform(self, X: pd.DataFrame, y=None):
        # add your code here!
        # TRANSFER TO SOLUTION NOTEBOOK
        X = X.copy()
        X = self.kc_transform_function(X)
        return X

    def sqft_basement(self, df: pd.DataFrame):
        df = df.copy()
        df["sqft_basement"] = df["sqft_basement"].replace("?", np.nan)
        df["sqft_basement"] = df["sqft_basement"].astype(float)
        df["sqft_basement"] = df["sqft_living"] - df["sqft_above"]
        return df


class MissingViewTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=self.fill_missings_view_wf)

    def transform(self, X: pd.DataFrame, y=None):
        # add your code here!
        # TRANSFER TO SOLUTION NOTEBOOK
        X = X.copy()
        X = self.kc_transform_function(X)
        return X

    def fill_missings_view_wf(self, df: pd.DataFrame):
        df = df.copy()
        df["view"] = df["view"].fillna(0)
        df["waterfront"] = df["waterfront"].fillna(0)
        return df


class LastChangeTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=self.calculate_last_change)

    def transform(self, X: pd.DataFrame, y=None):
        # add your code here!
        # TRANSFER TO SOLUTION NOTEBOOK
        X = X.copy()
        X = self.kc_transform_function(X)
        return X

    def calculate_last_change(self, df: pd.DataFrame):
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


class SqftPriceTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=self.calculate_sqft_price)

    def transform(self, X: pd.DataFrame, y=None):
        # add your code here!
        # TRANSFER TO SOLUTION NOTEBOOK
        X = X.copy()
        X = self.kc_transform_function(X)
        return X

    def calculate_sqft_price(self, df: pd.DataFrame):
        df = df.copy()
        df["sqft_price"] = (df.price / (df.sqft_living + df.sqft_lot)).round(2)
        return df


class DistanceToWealthTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=self.calculate_distance_to_wealth_center)

    def transform(self, X: pd.DataFrame, y=None):
        # add your code here!
        # TRANSFER TO SOLUTION NOTEBOOK
        X = X.copy()
        X = self.kc_transform_function(X)
        return X

    def calculate_distance_to_wealth_center(self, df: pd.DataFrame):
        df = df.copy()
        # Absolute difference of latitude between centre and property
        df["delta_lat"] = np.absolute(47.62774 - df["lat"])
        # Absolute difference of longitude between centre and property
        df["delta_long"] = np.absolute(-122.24194 - df["long"])
        # Distance between centre and property
        df["center_distance"] = (
            (
                (df["delta_long"] * np.cos(np.radians(47.6219))) ** 2
                + df["delta_lat"] ** 2
            )
            ** (1 / 2)
            * 2
            * np.pi
            * 6378
            / 360
        )
        return df


class DistanceToBeachTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(
            kc_transform_function=self.calculate_distance_to_beach_promenade
        )

    def transform(self, X: pd.DataFrame, y=None):
        # add your code here!
        # TRANSFER TO SOLUTION NOTEBOOK
        X = X.copy()
        X = self.kc_transform_function(X)
        return X

    def calculate_distance_to_beach_promenade(self, df: pd.DataFrame):
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
        distances = (
            np.sqrt(delta_long_corr**2 + delta_lat**2) * 2 * np.pi * 6378 / 360
        )

        # Find the minimum distance to waterfront for each point
        water_distance = np.min(distances, axis=1)

        # Add the water distance column to the dataframe
        df["water_distance"] = water_distance

        return df


# TODO: Note that the following class is how we would implement a transformer. The usage of inheritance is not
#  necessary. And maybe it is better to keep transformation classes separated with sharing the fit method.
class columnDropperTransformer:
    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, y=None):
        X = X.copy()
        return X.drop(self.columns, axis=1)

    def fit(self, X, y=None):
        return self
