"""
cross_val.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt


def logistic_regression_cv(
    train_features: pd.DataFrame,
    train_labels: np.ndarray,
    k_folds: int,
    lambdas: np.ndarray,
    random_state: int = 42,
    max_iter: int = 5000,
):
    """
    Using LogisticRegression and GridSearchCV from sklearn, set up a cross validation.

    IMPLEMENTATION INSTRUCTIONS:
        - First create a LogisticRegression model object that:
            - Uses L2 regularization
            - Uses the solver `lbfgs`
            - Uses the parameter `random_state` passed into this function
            - Uses the parameter `max_iter` passed into this function
        - Then create a GridSearchCV object that:
            - Uses the LogisticRegression model object you created
            - Runs a cross validation with `k_folds` folds
            - Uses "roc_auc" as the scoring metric
            - Uses the parameter `n_jobs` set to -1
        - Fit the GridSearchCV object to the training data and return the resulting
            GridSearchCV object.

    Parameters:
        train_features: The training features as a Pandas DataFrame
        train_labels: The training labels as a NumPy ndarray
        k_folds: The number of folds to use in cross validation
        lambdas: The list of lambda values to use in cross validation
        random_state: The random seed to use when training the model
        max_iter: The maximum number of iterations to use when training the model

    Returns:
        log_reg_cv: The GridSearchCV object
    """

    # Overwrite this variable in your implementation
    log_reg_cv = None


    # ==================== YOUR CODE HERE ====================
    log_reg = LogisticRegression(random_state=random_state, max_iter=max_iter, penalty='l2', solver='lbfgs')
    param_grid_C = 1/lambdas
    log_reg_cv =  GridSearchCV(log_reg, param_grid={'C': param_grid_C}, cv=k_folds, n_jobs=-1, scoring='roc_auc').fit(train_features, train_labels)
    
    # ==================== YOUR CODE HERE ====================
    

    # Return the best model
    return log_reg_cv


def gradient_boosting_cv(
    train_features: pd.DataFrame,
    train_labels: np.ndarray,
    k_folds: int,
    n_estimators_list: np.ndarray,
    random_state: int = 42,
):
    """
    Using GradientBoostingClassifier and GridSearchCV from sklearn, set up a cross validation.

    IMPLEMENTATION INSTRUCTIONS:
        - First create a GradientBoostingClassifier model object that:
            - Uses the parameter `random_state` passed into this function
        - Then create a GridSearchCV object that:
            - Uses the GradientBoostingClassifier model object you created
            - Runs a cross validation with `k_folds` folds
            - Uses "roc_auc" as the scoring metric
            - Uses the parameter `n_jobs` set to -1
        - Fit the GridSearchCV object to the training data and return the resulting
            GridSearchCV object.

    Parameters:
        train_features: The training features as a Pandas DataFrame
        train_labels: The training labels as a NumPy ndarray
        k_folds: The number of folds to use in cross validation
        n_estimators: The list of n_estimators values to use in cross validation
        random_state: The random seed to use when training the model

    Returns:
        grad_boost_cv: The GridSearchCV object
    """

    # Overwrite this variable in your implementation
    grad_boost_cv = None


    # ==================== YOUR CODE HERE ====================
    grad_boost_model = GradientBoostingClassifier(random_state=random_state)
    grad_boost_cv =  GridSearchCV(grad_boost_model, param_grid={'n_estimators': n_estimators_list}, cv=k_folds, 
                               n_jobs=-1, scoring='roc_auc').fit(train_features, train_labels)
    
    
    # ==================== YOUR CODE HERE ====================
    

    # Return the best model
    return grad_boost_cv
