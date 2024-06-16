"""
BIOMEDIN 215: Assignment 6
preprocessing.py

This file contains provided functions similar to those you implemented in A5.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict


def split_labels_and_features(
    patient_feature_matrix: pd.DataFrame,
    column_value_map: Dict[str, Dict[str, int]],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    NOTE: This function is provided for you. You do NOT need to modify it.
    This is a slightly modified version of the function you implemented in A5.

    Converts non-numeric features to numeric and splits the patient_feature_matrix
    into two dataFrames: one containing the numerical features and one
    containing the labels.

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
    features = None
    labels = None

    patient_feature_matrix = patient_feature_matrix.copy()

    # For each column in the patient_feature_matrix, convert the non-numeric
    # values to numeric values using the column_value_map
    for column in column_value_map:
        patient_feature_matrix[column] = patient_feature_matrix[column].map(
            column_value_map[column]
        )

    # Create features dataframe
    features = patient_feature_matrix.drop(columns=["death_in_stay"])
    features = features.set_index("subject_id")

    # Create labels dataframe
    labels = patient_feature_matrix[["death_in_stay", "subject_id"]]
    labels = labels.set_index("subject_id")

    return features, labels


def feature_variance_threshold(
    features: pd.DataFrame, freq_cut: float = 95 / 5, unique_cut: float = 0.1
) -> pd.DataFrame:
    """
    NOTE: This function is provided for you. You do NOT need to modify it.
    This is a slightly modified version of the function you implemented in A5.

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
    filtered_features = None

    # A list of columns to keep
    kept_columns = []

    for column_name in features.columns:
        # Get the current column
        col = features[column_name]

        # Get the value counts of unique values
        value_freqs = col.value_counts()

        # If the column has only one unique value, skip appending this feature
        if len(value_freqs) == 1:
            continue

        # Determine most frequent value and second most frequent value
        most_freq_value = value_freqs.iloc[0]
        second_most_freq_value = value_freqs.iloc[1]

        # Determine the frequency ratio
        freq_ratio = most_freq_value / second_most_freq_value

        # Calculate the percentage of unique values
        n_unique = len(value_freqs)
        n_total = len(col)
        unique_ratio = n_unique / n_total

        # If the frequency ratio is less than the frequency cut and the
        # unique ratio is greater than the unique cut, keep the column
        if freq_ratio < freq_cut or unique_ratio > unique_cut:
            kept_columns.append(column_name)

    # Create filtered features dataframe
    filtered_features = features[kept_columns].copy()

    return filtered_features
