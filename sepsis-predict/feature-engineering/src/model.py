"""
BIOMEDIN 215: Assignment 4
model.py

This file contains functions that you must implement.

NOTE: You do not need to edit or implement any of the code in this file.
"""

import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
import numpy as np


def fit_model(joined: pd.DataFrame, label_df: pd.DataFrame):
    """
    THIS IS A PROVIDED FUNCTION. You do not need to edit this function.

    Fits the model and prints the AUC ROC score. The model pipeline should be
    defined in this function.

    Parameters:
        joined (pd.DataFrame): The joined feature matrix
        label_df (pd.DataFrame): The dataframe containing the labels
    """

    # Determine final feature matrix and label vector
    df = pd.merge(label_df, joined, how="left")

    # Extract features and labels
    X = df.drop(columns=label_df.columns)
    y = df["label"].astype(int)

    # Set up a training control configuration for cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Preprocessing steps
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    # Create an elastic net
    logistic_elastic_net = LogisticRegression(
        penalty="elasticnet", solver="saga", l1_ratio=1, max_iter=10000, C=1000
    )

    # Combine the preprocessing and model into a pipeline
    pipeline = Pipeline(
        [
            ("imputer", imputer),
            ("scaler", scaler),
            ("logistic_elastic_net", logistic_elastic_net),
        ]
    )

    # Use a list to store scores for each fold
    scores_list = []

    # Manually loop over the splits and fit the model, wrapping with tqdm for a progress bar
    for train_index, test_index in tqdm(
        cv.split(X, y), unit="fold", total=cv.get_n_splits()
    ):
        # Split the data
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # Fit and evaluate the pipeline
        pipeline.fit(X_train, y_train)
        score = roc_auc_score(y_test, pipeline.predict_proba(X_test)[:, 1])
        scores_list.append(score)
        print(f"Fold 1 ROC AUC Score: {score:.4f}")

    scores = np.array(scores_list)

    # Print the results
    print("Mean ROC AUC Score:", scores.mean())
