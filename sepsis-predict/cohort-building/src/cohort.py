"""
BIOMEDIN 215: Assignment 3
cohort.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""

# Imports - Do not modify
import numpy as np
import pandas as pd
from typing import List, Any


def filter_df(df: pd.DataFrame, filter_col: str, value_list: List[Any]) -> pd.DataFrame:
    """
    Returns a filtered version of the input DataFrame where only rows that have
    a value in the <filter_col> column that is in <value_list> are retained.

    EXAMPLE: If <filter_col> is "subject_id" and <value_list> is [39, 1888],
    then the returned DataFrame should only contain rows where the "subject_id" column
    is either 39 or 1888.

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) to return a filtered version
            of the input DataFrame where only rows that have a value in the <filter_col>
            column that is in <value_list> are retained.
        - If <value_list> is empty, return an empty DataFrame with the same columns
            as the input DataFrame.
        - If <filter_col> is not in the DataFrame, raise a ValueError.
        - Do NOT modify the original DataFrame.
        - No other error checking is required.

    HINTS:
        - You may find the following functions useful:
            - Pandas: isin()

    Parameters:
        df (pd.DataFrame): The DataFrame to be filtered
        filter_col (str): The column to filter on
        value_list (List[Any]): The list of values to filter on

    Returns:
        filtered_df (pd.DataFrame): A filtered version of the input DataFrame
            where only rows that have a value in the <filter_col> column that is
            in <value_list> are retained.
    """

    # Overwrite this variable with the return value
    filtered_df = None

    # ==================== YOUR CODE HERE ====================
    if not value_list: 
        df_empty = df.iloc[:0,:].copy()
        return df_empty
    elif filter_col not in df.columns: 
        raise ValueError(f'{filter_col} is not in df columns.')
    else: 
        filtered_df = df[df[filter_col].isin(value_list)]
    
    return filtered_df

    
    # ==================== YOUR CODE HERE ====================


def get_dev_cohort_list(df: pd.DataFrame, num_subject_ids: int = 1000):
    """
    Returns a list of the smallest <num_subject_ids> subject_ids in the DataFrame.
    You may assume that the inputs are valid.

    EXAMPLE: If <num_subject_ids> is 1000, then the returned list should
    contain the smallest 1000 subject_ids (determined by sorting the subject_ids
     in ascending order).

        - NOTE: In practice, you should always randomly sample for a development
        set, as there could be some underlying systematic difference between the
        first 1000 patient records and the rest of the patient records. For the
        purposes of this assignment, we will use this method to simplify
        reproducibility.

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) to return a list that
            contains the smallest <num_subject_ids> subject_ids in the DataFrame.
        - If <num_subject_ids> is less than or equal to 0, return an empty list.
        - If <num_subject_ids> is greater than the number of unique subject_ids,
            return a list containing all of the unique subject_ids in the DataFrame.


    HINTS:
        - You may assume all `subject_id` values can be cast to integers.
        - You may find the following functions useful:
            - Pandas: unique()
            - Numpy: sort()

    Parameters:
        df (pd.DataFrame): The DataFrame to be filtered
        num_subject_ids (int): The number of subject_ids to include in the
            restricted DataFrame

    Returns:
        subject_ids (List[int]): A list of the smallest <num_subject_ids>
            subject_ids in the DataFrame.
    """

    # Overwrite this variable with the return value
    subject_ids = []


    # ==================== YOUR CODE HERE ====================
    
    all_subjectids = df['subject_id'].unique()
    all_subjectids_sorted = np.sort(all_subjectids)
    if num_subject_ids <= 0: 
        return subject_ids
    elif num_subject_ids > all_subjectids_sorted.shape[0]: 
        return list(all_subjectids_sorted)
    else:
        subject_ids = list(all_subjectids_sorted[:num_subject_ids])
        return subject_ids
    
    
    # ==================== YOUR CODE HERE ====================


def join_infections(df_1: pd.DataFrame, df_2: pd.DataFrame):
    """
    Joins the two infection DataFrames on admission events (`subject_id` and `hadm_id`).

    The resulting dataframe should contain one instance of each column in the two dataframes,
    and should contain one row for every unique (`subject_id` and `hadm_id`) pair
    that appears in either of the two DataFrames.

    EXAMPLE: If df_1 contains the following columns:
        subject_id | hadm_id | has_icd9_infection
    and df_2 contains the following columns:
        subject_id | hadm_id | has_note_infection
    then the returned DataFrame should contain the following columns:
        subject_id | hadm_id | has_icd9_infection | has_note_infection


    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) to return a merged version
            of the two input DataFrames using the appropriate join strategy for
            this task.
        - Replace any missing values in the resulting merged DataFrame with 0.
        - Do NOT modify the original DataFrames.

    HINTS:
        - You may find the following functions useful:
            - Pandas: merge()

    Parameters:
        df_1 (pd.DataFrame): The first DataFrame to be joined
        df_2 (pd.DataFrame): The second DataFrame to be joined

    Returns:
        joined_df (pd.DataFrame): A merged version of the two input DataFrames
            using the appropriate join strategy for this task.
    """

    # Overwrite this variable with the return value
    joined_df = None


    # ==================== YOUR CODE HERE ====================
    
    joined_df = pd.merge(df_1, df_2, how='outer', on=['subject_id','hadm_id'])
    joined_df.fillna(0, inplace=True)
    
    # ==================== YOUR CODE HERE ====================
    

    # Return the merged DataFrame
    return joined_df
