"""
BIOMEDIN 215: Assignment 4
utils.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""


import pandas as pd
from typing import Union, List


def preprocess_dates(
    df: pd.DataFrame,
    date_columns: List[str],
    date_formats: List[str],
    inplace: bool = True,
) -> Union[pd.DataFrame, None]:
    """
    Converts the columns in the DataFrame to datetime objects.

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) to convert the columns in the
            DataFrame to datetime objects.
        - As an in-place opperation, the "admittime" and "dischtime" columns should
            be modified in the input DataFrame and nothing should be returned.
        - As a non in-place operation, the input DataFrame should not be modified
            and a new DataFrame should be returned with the appropriate columns
            converted to datetime objects.
        - All converted `datetime` objects should be timezone-aware and in UTC.

    HINT: Review the Pandas documentation to find a function that can be used to
        convert a column to datetime objects.

    Parameters:
        df (pd.DataFrame): The DataFrame
        date_columns (List[str]): The columns to convert to datetime objects
        date_formats (List[str]): The formats of the dates in each date_column column
            NOTE: date_columns and date_formats should be utilized such that the
            columns and formats in each list correspond 1-to-1, in order.
        inplace (bool): Whether or not to perform the operation in-place
    """

    pass

    # ==================== YOUR CODE HERE ====================
    if inplace:
        for i,col in enumerate(date_columns):
            df[col] = pd.to_datetime(df[col], format=date_formats[i], utc=True)
    else: 
        df_converted = df.copy()
        for i,col in enumerate(date_columns):
            df_converted[col] = pd.to_datetime(df_converted[col], format=date_formats[i], utc=True)
        return df_converted
        
    
    
    
    # ==================== YOUR CODE HERE ====================
    


def join_and_clean_data(diagnosis_features, note_concept_features, heart_rate_features):
    """
    Returns a joined dataframe of all features and cleans the data.

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) to `outer` join the three
            feature dataframes and clean the data.
        - The returned dataframe should not contain any NaN values.
            -  Replace all NaN values in the `latest_heart_rate` and `time_wt_avg`
                columns with their respective means.
            - Replace all other NaN values with 0.
        - The returned dataframe should be sorted by `subject_id` in ascending order.

    Parameters:
        diagnosis_features (pd.DataFrame): The patient diagnosis features dataframe.
        note_concept_features (pd.DataFrame): The patient note concept features
            dataframe.
        heart_rate_features (pd.DataFrame): The patient heart rate features dataframe.

    Returns:
        X (pd.DataFrame): The joined and cleaned dataframe of all features.
    """

    # Overwrite this variable with the return value for your implementation
    X = None


    # ==================== YOUR CODE HERE ====================
    X = pd.merge(diagnosis_features, note_concept_features, on='subject_id', how='outer') 
    X = X.fillna(0)    
    X = X.merge(heart_rate_features, on='subject_id', how='outer')
    heart_rate_features_cols = heart_rate_features.columns
    heart_rate_features_cols = [x for x in heart_rate_features_cols if x!='subject_id']
    X[heart_rate_features_cols] = X[heart_rate_features_cols].fillna(X[heart_rate_features_cols].mean())
    other_cols = [x for x in X.columns if x not in heart_rate_features.columns]
    X[other_cols] = X[other_cols].fillna(0)

    X.sort_values('subject_id', inplace=True)
    
    # ==================== YOUR CODE HERE ====================
    

    # Return the dataframe
    return X
