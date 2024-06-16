from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor


@dataclass
class datasets:
    train_X: pd.DataFrame
    valid_X: pd.DataFrame
    test_X: pd.DataFrame
    train_y: pd.Series
    valid_y: pd.Series
    test_y: pd.Series


def train_and_eval_model(
    model: XGBRegressor, ds: datasets, features_to_include: List[str]
):
    """Fits XGBRegressor on a subset of features using specified hyperparameters

    :param model: XGBRegressor model to train
    :param ds: datasets object containing train, validation, and test data
    :param features_to_include: list of features to include in training,
        these should be columns in ds.train_X
    :return predictions: dictionary of train, validation, and test predictions
    :return metrics: dictionary of train, validation, and test RMSE
    """
    assert all(
        [feature in ds.train_X.columns for feature in features_to_include]
    ), "All features must be columns in ds.train_X"

    model.fit(ds.train_X[features_to_include], ds.train_y)

    train_y_pred = model.predict(ds.train_X[features_to_include])
    valid_y_pred = model.predict(ds.valid_X[features_to_include])
    test_y_pred = model.predict(ds.test_X[features_to_include])

    predictions = {
        "train": train_y_pred,
        "valid": valid_y_pred,
        "test": test_y_pred,
    }

    metrics = {
        "train": np.sqrt(mean_squared_error(ds.train_y, train_y_pred)),
        "valid": np.sqrt(mean_squared_error(ds.valid_y, valid_y_pred)),
        "test": np.sqrt(mean_squared_error(ds.test_y, test_y_pred)),
    }

    return predictions, metrics


def run_hparam_search(
    ds: datasets,
    features_to_include: List[str],
    max_depth_options: List[int] = [1, 2, 3],
    learning_rate_options: List[float] = [0.001, 0.01, 0.1, 0.2, 0.3],
    n_estimators_options: List[int] = [2, 5, 10, 25, 50],
):
    """Runs hyperparameter search for XGBRegressor, selecting best model based on
        validation rmse

    :param ds: datasets object containing train, validation, and test data
    :param features_to_include: list of features to include in training,
        these should be columns in ds.train_X
    :param max_depths: list of max_depths to try
    :param learning_rates: list of learning_rates to try
    :param n_estimators: list of n_estimators to try
    :return best_metrics: dictionary of train, validation, and test RMSE for best model
    :return best_params: dictionary of best hyperparameters
    """
    # Initialize variables to track best model
    best_metrics = {"train": np.inf, "valid": np.inf, "test": np.inf}
    best_params = None

    # Iterate over xgboost parameters
    for max_depth in max_depth_options:
        for learning_rate in learning_rate_options:
            for n_estimators in n_estimators_options:
                model_params = {
                    "max_depth": max_depth,
                    "learning_rate": learning_rate,
                    "n_estimators": n_estimators,
                }

                model = XGBRegressor(
                    random_state=0,
                    **model_params,
                )

                # Train model
                _, model_metrics = train_and_eval_model(
                    ds=ds, model=model, features_to_include=features_to_include
                )

                # Update best model if validation rmse improved
                if model_metrics["valid"] < best_metrics["valid"]:
                    best_metrics = model_metrics
                    best_params = model_params

    return best_metrics, best_params


def select_features_with_lasso(
    ds: datasets, features_to_select_from: List[str], alpha: float = 0.1
) -> List[bool]:
    """Selects features using Lasso regression
    :param ds: datasets object containing train, validation, and test data
    :param features_to_select_from: list of features to select from,
        these should be columns in ds.train_X
    :param alpha: regularization parameter for Lasso regression
        (higher values -> more regularization -> fewer features selected)
    """
    # Exclude examples with missing values
    train_X = ds.train_X[features_to_select_from].dropna(axis="index")
    train_y = ds.train_y.loc[train_X.index]

    # Scale features
    scaler = StandardScaler()
    scaler.fit(train_X.values)

    # Select features using Lasso regression
    sel_ = SelectFromModel(Lasso(alpha=alpha, random_state=0))
    sel_.fit(scaler.transform(train_X.values), train_y.values)

    # Get list of features with nonzero coefficients from Lasso regression
    mask_of_features_to_keep = sel_.get_support()
    features_to_keep = train_X.columns[np.where(mask_of_features_to_keep)[0]]

    return features_to_keep
