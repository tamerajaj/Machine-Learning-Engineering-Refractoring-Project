from sklearn.base import BaseEstimator, TransformerMixin

from kc_refactoring import (
    bath_bed_ratio_outlier,
    sqft_basement,
    fill_missings_view_wf,
    calculate_last_change,
    calculate_sqft_price,
    calculate_distance_to_wealth_center,
    calculate_distance_to_beach_promenade,
)


class KingCountyTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, kc_transform_function):
        self.kc_transform_function = kc_transform_function

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        # add your code here!
        # TRANSFER TO SOLUTION NOTEBOOK
        X = X.copy()
        X = self.kc_transform_function(X)
        return X


class BathRatioTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=bath_bed_ratio_outlier)


class SqftBasementTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=sqft_basement)


class MissingViewTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=fill_missings_view_wf)


class LastChangeTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=calculate_last_change)


class SqftPriceTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=calculate_sqft_price)


class DistanceToWealthTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=calculate_distance_to_wealth_center)


class DistanceToBeachTransformer(KingCountyTransformer):
    def __init__(self):
        super().__init__(kc_transform_function=calculate_distance_to_beach_promenade)
