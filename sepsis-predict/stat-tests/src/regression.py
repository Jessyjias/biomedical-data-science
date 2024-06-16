"""
regression.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""


import pandas as pd
import numpy as np
from typing import List, Union
import statsmodels.api as sm
import statsmodels.formula.api as smf


def run_logistic_regression(
    filtered_features: pd.DataFrame,
    labels: pd.DataFrame,
    selected_features: Union[List[str], None] = None,
):
    """
    Runs a logistic regression utilizing the statsmodels package formula api
    and returns the resulting fit model object.

    `statsmodels` is a powerful Python package for statistical modeling. It mimics
    the functionality of R, a popular statistical programming language. The
    `statsmodels.formula.api` (often imported as `smf`) provides a way to
    specify models using formula strings: strings the describe the relationship
    between variables to be used in a model, often in the following form:
        "outcome ~ feature_1 + feature_2 + ... + feature_n"

    To read about the formula api, see the following documentation:
        https://www.statsmodels.org/stable/example_formulas.html

    The formula API is particularly useful when working with Pandas DataFrames because
    it allows for a high-level concise way to define the relationships between variables.

    In this function, use the formula api to create a logistic regression model
    and fit it to the data.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below where specified.
        - Use the smf.glm function to create a logistic regression model. You
            will need to specify the following parameters:
            - `formula`: A string that specifies the relationship between features
                and the outcome using the formula api. Your implementation should
                call the function `create_formula_string` to create this string.
            - `data`: The dataframe containing the features and outcome. You should
                concatenate the labels and filtered_features dataframes into a single
                dataframe and use that as the data parameter.
            - `family`: The appropriate statistical family of the model (Think about
                what type of data we are working with/ what we are trying to predict)
        - Use the .fit() method to fit the model to the data, and return the result
            of the fit function call as the return value.
            - ei. result = glm.fit()
        - If selected_features is None, use all the features in the filtered_features
            dataframe in the formula. Otherwise, use only the features in the
            selected_features list.

    Parameters:
        filtered_features (pd.DataFrame): A dataframe containing the filtered
            features
        labels (pd.DataFrame): A dataframe containing the labels
        selected_features (List[str]): A list of column names to use as features.
            If None, use all the features in the filtered_features dataframe.

    Returns:
        result (statsmodels.genmod.generalized_linear_model.GLMResultsWrapper): The
            result of the fit function call
    """

    # Overwrite this return variable(s) in your implementation
    result = None


    # ==================== YOUR CODE HERE ====================
    
    # TODO: Implement
    if selected_features is None: 
        features = filtered_features
    else: 
        features = filtered_features[selected_features]
    
    formula = create_formula_string(labels.columns[0], features.columns)
    df_data = pd.concat([labels, features], axis=1).reset_index()
    model = smf.glm(formula = formula, data=df_data, family=sm.families.Binomial())
    
    result = model.fit()
    
    # ==================== YOUR CODE HERE ====================
    

    return result


def create_formula_string(outcome_col: str, feature_col_list: List[str]) -> str:
    """
    Creates a (simple) formula string for use in the statsmodels formula api.

    The formula string should be of the form:
        "outcome ~ feature_1 + feature_2 + ... + feature_n"
    where outcome is the name of the outcome column, and feature_1 through
    feature_n are the names of the feature columns. (For the purposes of this
    assignment, we will only be using simple formula strings of this form.)

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below where specified.
        - Create a formula string using the outcome_col and feature_col_list
            parameters.
        - Return the formula string.

    Parameters:
        outcome_col (str): The name of the outcome column
        feature_col_list (List[str]): A list of column names to use as features.

    Returns:
        formula_string (str): A string that specifies the relationship between
            features and the outcome using the formula api.
    """

    # Overwrite this return variable(s) in your implementation
    formula_string = None


    # ==================== YOUR CODE HERE ====================
    
    # TODO: Implement
    formula_string = f"{outcome_col} ~ " + '+'.join(feature_col_list)
    # ==================== YOUR CODE HERE ====================
    

    return formula_string
