from __future__ import annotations
import time
from pathlib import Path
from typing import Tuple, Any

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the dataset from a CSV file."""
    return pd.read_csv(file_path)


def summarize_data(df: pd.DataFrame) -> None:
    """Print basic statistics and info about the DataFrame."""
    print("Data Summary:")
    print(df.describe())
    print("\nMissing Values:", df.isnull().sum().sum())


def plot_class_distribution(df: pd.DataFrame) -> None:
    """Plot the distribution of fraud vs. non-fraud cases."""
    counts = df['Class'].value_counts(normalize=True) * 100
    sns.barplot(x=counts.index, y=counts.values)
    plt.title('Class Distribution (%)')
    plt.xlabel('Class')
    plt.ylabel('Percentage')
    plt.xticks([0, 1], ['No Fraud', 'Fraud'])
    plt.show()


def balance_data(df: pd.DataFrame, method: str = 'undersample') -> pd.DataFrame:
    """Balance the dataset either by undersampling or oversampling."""
    fraud = df[df['Class'] == 1]
    non_fraud = df[df['Class'] == 0]

    if method == 'undersample':
        non_fraud_sample = non_fraud.sample(len(fraud), random_state=42)
        balanced = pd.concat([non_fraud_sample, fraud])
    else:
        non_fraud_sample = non_fraud.sample(len(fraud), replace=True, random_state=42)
        balanced = pd.concat([non_fraud_sample, fraud])

    return balanced.sample(frac=1, random_state=42)  # Shuffle


def reduce_dimensionality(X: np.ndarray, method: str = 'pca', n_components: int = 2) -> np.ndarray:
    """Reduce data to n_components using PCA, TSNE, or TruncatedSVD."""
    match method.lower():
        case 'pca':
            reducer = PCA(n_components=n_components, random_state=42)
        case 'tsne':
            reducer = TSNE(n_components=n_components, random_state=42)
        case 'svd':
            reducer = TruncatedSVD(n_components=n_components, random_state=42)
        case _:
            raise ValueError(f"Unknown reduction method: {method}")
    return reducer.fit_transform(X)


def train_and_evaluate(X: np.ndarray, y: np.ndarray) -> RandomForestClassifier:
    """Split data, train RandomForest, and evaluate performance."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    start = time.time()
    model.fit(X_train, y_train)
    elapsed = time.time() - start
    print(f"Training completed in {elapsed:.2f} seconds.")

    y_pred = model.predict(X_test)
    print("Classification Report:")
    print(classification_report(y_test, y_pred, digits=4))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return model


def main() -> None:
    data_path = Path("data/creditcard.csv")
    df = load_data(data_path)
    summarize_data(df)
    plot_class_distribution(df)

    balanced_df = balance_data(df, method='undersample')
    features = balanced_df.drop(columns=['Class'])
    labels = balanced_df['Class'].values

    reduced_features = reduce_dimensionality(features.values, method='pca')
    _ = train_and_evaluate(reduced_features, labels)


if __name__ == '__main__':
    main()
