from kc_transformer_pipelines import (
    BathRatioTransformer,
    SqftBasementTransformer,
    MissingViewTransformer,
    LastChangeTransformer,
    SqftPriceTransformer,
    DistanceToWealthTransformer,
    DistanceToBeachTransformer,
)

from sklearn.pipeline import Pipeline


class PreprocessingKC:
    def __init__(self):
        # Data cleaning Pipeline
        self.data_cleaning_pipeline = Pipeline(
            [
                ("bath_ratio", BathRatioTransformer()),
                ("sqft_basement", SqftBasementTransformer()),
                ("missing_view", MissingViewTransformer()),
            ]
        )
        self.preprocessor_pipe = Pipeline(
            [
                ("last_change", LastChangeTransformer()),
                ("sqft_price", SqftPriceTransformer()),
                ("distance_to_wealth", DistanceToWealthTransformer()),
                ("distance_to_beach", DistanceToBeachTransformer()),
            ]
        )

        self.preprocessor_pipe = Pipeline(
            [
                ("data_cleaning", self.data_cleaning_pipeline),
                ("preprocessor", self.preprocessor_pipe),
            ]
        )

    def preprocess_fit_transform(self, df):
        return self.preprocessor_pipe.fit_transform(df), self.preprocessor_pipe

    def preprocess_transform(self, df):
        return self.preprocessor_pipe.transform(df)
