import pandas as pd
from kc_preprocessing import PreprocessingKC

if __name__ == "__main__":
    data = pd.read_csv("../data/King_County_House_prices_dataset.csv")

    processor = PreprocessingKC()

    new_data, pipeline = processor.preprocess_fit_transform(data)

    new_data.to_csv(
        "../data/King_County_House_prices_dataset_preprocessed.csv", index=False
    )
