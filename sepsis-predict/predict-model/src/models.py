"""
models.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np


def logistic_regression(
    X_train: pd.DataFrame,
    Y_train: np.ndarray,
    lambda_: float,
    random_state: int = 42,
    max_iter: int = 10000,
) -> LogisticRegression:
    """
    Set up a Logistic Regression model that uses L2 regularization and fit it to
    the training data. Return the resulting model object.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below in the specified location.
        - Use sklearn's LogisticRegression function to create the model.
            It may be helpful to read the documentation for LogisticRegression:
            https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
        - Your implementation of the LogisticRegression function should:
            - Use the appropriate `penalty`
            - Use the solver `lbfgs`
            - Utilize all of the other parameters passed into this function appropriately
        - Use the fit function to fit the model to the training data.
        - Return the resulting fit model object.
        - Do NOT modify the input dataframes.
    """

    # Overwrite this variable in your implementation
    log_reg_model = None


    # ==================== YOUR CODE HERE ====================
    C = 1/lambda_ ## Inverse of regularization strength
    log_reg_model = LogisticRegression(random_state=random_state, max_iter=max_iter, penalty='l2', C=C, solver='lbfgs').fit(X_train, Y_train)
    # ==================== YOUR CODE HERE ====================
    

    return log_reg_model


def gradient_boosted_tree(
    X_train: pd.DataFrame,
    Y_train: np.ndarray,
    n_estimators: int,
    random_state: int = 42,
) -> GradientBoostingClassifier:
    """
    Set up a Gradient Boosted Tree model and fit it to the training data.
    Return the resulting model object.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below in the specified location.
        - Use sklearn's GradientBoostingClassifier function to create the model.
            It may be helpful to read the documentation for GradientBoostingClassifier:
            https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html
        - Your implementation of the GradientBoostingClassifier function should:
            - Use the parameter `random_state` passed into this function
            - Use the parameter `n_estimators` passed into this function
        - Use the fit function to fit the model to the training data.
        - Return the resulting fit model object.
        - Do NOT modify the input dataframes.

    Parameters:
        X_train: A dataframe containing the training features
        Y_train: A numpy array containing the training labels
        n_estimators: The number of estimators to use in the model
        random_state: The random state to use in the model

    Returns:
        A GradientBoostingClassifier model object
    """

    # Overwrite this variable in your implementation
    grad_boost_model = None

    # ==================== YOUR CODE HERE ====================
    grad_boost_model = GradientBoostingClassifier(n_estimators=n_estimators, random_state=random_state).fit(X_train, Y_train)
    
    # ==================== YOUR CODE HERE ====================
    

    return grad_boost_model


def get_log_reg_coefficients(
    log_reg: LogisticRegression,
):
    """
    Collects the coefficients from a LogisticRegression model object and returns
    them in a list. The order of the coefficients should match the order of the
    features in the model.

    This is a helper function for get_top_features. The coefficients of logistic
    regression and gradient boosted trees are stored differently, so we need to
    have separate functions to access the coefficients of each model.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below in the specified location.
        - You should only need to write one line of code in this function.
            - Hint: Look at the documentation for LogisticRegression:
                https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
        - Return the coefficients from the LogisticRegression model object.
        - Do NOT modify the input dataframes.
    """

    # Overwrite this variable in your implementation
    coefficients = None


    # ==================== YOUR CODE HERE ====================
    coefficients = log_reg.coef_

    # ==================== YOUR CODE HERE ====================
    

    return coefficients


def get_tree_feature_importance(
    gbt: GradientBoostingClassifier,
):
    """
    Collects the feature importances from a GradientBoostingClassifier model object
    and returns them in a list. The order of the coefficients should match the order
    of the features in the model.

    This is a helper function for get_top_features. The coefficients of logistic
    regression and gradient boosted trees are stored differently, so we need to
    have separate functions to access the coefficients of each model.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below in the specified location.
        - You should only need to write one line of code in this function.
            - Hint: Look at the documentation for GradientBoostingClassifier:
                https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html
        - Return the feature importances from the GradientBoostingClassifier model object.
        - Do NOT modify the input dataframes.
    """

    # Overwrite this variable in your implementation
    feature_importances = None


    # ==================== YOUR CODE HERE ====================
    feature_importances = gbt.feature_importances_
    
    # ==================== YOUR CODE HERE ====================
    

    return feature_importances


def get_top_features(
    model_obj,
    features: pd.DataFrame,
    feature_descriptions: pd.DataFrame,
    model_type: str,
    k: int = 10,
):
    """
    Given a sklearn model, return a dataframe containing k features with the largest
    absolute value coefficients. Note that part of this function is provided for you,
    but you will need to complete the implementation.

    TODO: You will need to implement the helper functions get_log_reg_coefficients
    and get_tree_feature_importance.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below in the specified location.
        - Return a dataframe containing the top k features with the largest
            absolute value coefficients.
            - The dataframe should have the following columns:
                - "feature": The name of the feature
                - "feature_type": The type of the feature
                - "description": The description of the feature
                - "coef" or "importance": The coefficient or importance of the feature
                - "abs_coef" or "abs_importance": The absolute value of the coefficient
                    or importance of the feature

    Parameters:
        log_reg: A sklearn model object
        model_type: The type of the model. Either "logistic_regression" or
            "gradient_boosted_tree"
        features: A dataframe containing the features used in training the model
        feature_descriptions: A dataframe containing the descriptions of the features
        k: The number of top features to return

    Returns:
        A dataframe containing the top k features with the largest coefficients.
    """

    # NOTE: The beginning of this function is provided for you, but you will need
    # to complete the implementation.

    # Check that the model type is valid
    if model_type not in ["logistic_regression", "gradient_boosted_tree"]:
        raise ValueError(
            f"Invalid model_type: {model_type}. Must be either 'logistic_regression' or 'gradient_boosted_tree'"
        )

    # If the model is a logistic regression model, get the feature coefficients
    values = []  # This is a list of the coefficients or feature importances
    value_type = ""  # This is either "coef" or "importance"
    if model_type == "logistic_regression":
        values = get_log_reg_coefficients(model_obj)
        value_type = "coef"
    # If the model is a gradient boosted tree model, get the feature importances
    elif model_type == "gradient_boosted_tree":
        values = get_tree_feature_importance(model_obj)
        value_type = "importance"

    # Overwrite this variable in your implementation
    top_k_features = None


    # ==================== YOUR CODE HERE ====================
    abs_values = abs(values.flatten())

    df_features_vals = pd.DataFrame(data={'feature':features.columns.tolist(), 
                                          value_type:values.flatten(), 
                                          f'abs_{value_type}': abs_values})
    df_features = pd.merge(df_features_vals, feature_descriptions[['feature', 'description', 'feature_type']], on='feature', how='left')
    top_k_features = df_features.sort_values(f'abs_{value_type}', ascending=False).head(k)
    # ==================== YOUR CODE HERE ====================
    

    return top_k_features
