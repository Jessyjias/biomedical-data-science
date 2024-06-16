"""
BIOMEDIN 215: Assignment 4
preprocessing.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict


def split_labels_and_features(
    patient_feature_matrix: pd.DataFrame,
    column_value_map: Dict[str, Dict[str, int]],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Converts non-numeric features to numeric and splits the patient_feature_matrix
    into two dataFrames: one containing the numerical features and one
    containing the labels.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below where specified.
        - Convert the non-numeric values in the patient_feature_matrix to numeric
            values using the column_value_map. HINT: Look at pandas documentation
            to find a function that can map values in columns to new values.
        - Split the patient_feature_matrix into two dataframes: one containing
            the numerical features and one containing the labels.
            - The features matrix should contain all values from all columns in the
                patient_feature_matrix except for "death_in_stay". Additionally,
                the "subject_id" column should be set as the index of the features.
            - The labels matrix should contain only the "death_in_stay" column values.
                Additionally, the "subject_id" column should be set as the index of
                the labels.
        - Do NOT modify the input dataframe.

    Parameters:
        patient_feature_matrix (pd.DataFrame): A dataframe containing the patient
            feature matrix
        column_value_map (Dict[str, Dict[str, int]]): A dictionary mapping column
            names to a dictionary mapping column values to their corresponding
            numeric values.
                Example Structure:
                    {
                        "column_name_1": {
                            "A": 0,
                            "B": 1,
                            }
                    }
                With this mapping, the value "A" in "column_name_1" would be
                converted to 0, and the value "B" in "column_name_1" would be
                converted to 1.

    Returns:
        features (pd.DataFrame): A pd.DataFrame containing the numerical features
            with the subject_id as the index
        labels (pd.DataFrame): A pd.DataFrame containing the labels with the
            subject_id as the index
    """

    # Overwrite these return variables in your implementation
    features = patient_feature_matrix.copy()
    labels = None


    # ==================== YOUR CODE HERE ====================
    features.replace(column_value_map, inplace=True)
    labels = features[['subject_id', 'death_in_stay']]
    labels.set_index('subject_id', inplace=True)
    features_cols = [col for col in features.columns if col != 'death_in_stay']
    features = features[features_cols]
    features.set_index('subject_id', inplace=True)
    
    # ==================== YOUR CODE HERE ====================
    

    return features, labels


def feature_variance_threshold(
    features: pd.DataFrame, freq_cut: float = 95 / 5, unique_cut: float = 0.1
) -> pd.DataFrame:
    """
    Removes features from the features dataframe that have low variance utilizing
    the following behavior:
        - If the feature has only one unique value, then the feature should always
            be REMOVED
        - If the ratio of the most common value to the second most common value
            for a particular feature column is LESS THAN freq_cut, then the feature
            should be KEPT
        - If the (number of unique values) / (total number of rows) is GREATER
            than unique_cut for a particular feature column, then the feature
            should be KEPT
        - Otherwise, the feature should be REMOVED

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below where specified.
        - Remove features from the features dataframe that have low variance
            utilizing the behavior described above.
        - Return a version of the features dataframe with the low variance features
            removed.
        - Do NOT modify the input dataframe.


    Parameters:
        features (pd.DataFrame): A dataframe containing the numerical features
        freq_cut (float): The frequency cut-off value to use for removing features
            based on frequency of most common value to second most common value
        unique_cut (int): The unique cut-off value to use for removing features
            based on the ratio of unique values to total number of rows

    Returns:
        filtered_features (pd.DataFrame): A pd.DataFrame containing the filtered
            features
    """

    # Overwrite this return variable in your implementation
    filtered_features = features.copy()

    # ==================== YOUR CODE HERE ====================

    ## returns name of the feature if it meets the to-be-kept criteria, else return None
    def get_kept_feature_name(df, col_name): 
        if len(df[col_name].unique())==1: 
            return None 
        top_1_count, top_2_count = df[col_name].value_counts().nlargest(2).values.tolist()[0], df[col_name].value_counts().nlargest(2).values.tolist()[1]
        num_unique = len(df[col_name].unique()) 
        total_df_rows = df[col_name].shape[0]
        if top_1_count/top_2_count < 95/5: 
            return col_name
        elif num_unique/total_df_rows > 0.1: 
            return col_name
        else: 
            return None
    
    filtered_cols = [col for col in filtered_features.columns if get_kept_feature_name(filtered_features, col) != None]
    filtered_features = filtered_features[filtered_cols]
    
    # ==================== YOUR CODE HERE ====================
    

    return filtered_features
