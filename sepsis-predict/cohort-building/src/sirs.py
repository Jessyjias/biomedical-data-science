"""
BIOMEDIN 215: Assignment 3
sirs.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""

# Imports - Do not modify
import pandas as pd


def summarize_sirs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Utilizing a dataframe containing the labs and vitals for each subject at each
    available timestamp, this function returns a dataframe containing binary indicator
    columns for each of the four SIRS criteria. The binary columns indicate whether
    or not the subject met the criteria at each timestamp with True or False.

    EXAMPLE: The original dataframe contains the following columns:
        `subject_id`, `hadm_id`, `icustay_id`, `charttime`,
            `<followed by all the labs and vitals>`

    The returned dataframe should contain the following columns:
        `subject_id`, `hadm_id`, `icustay_id`, `charttime`,
            `criteria_1`, `criteria_2`, `criteria_3`, `criteria_4`

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) to return a dataframe containing
            binary indicator columns for each of the four SIRS criteria and the current
            sepsis status, as defined by the TREWScore paper.
        - The returned dataframe should ONLY contain the following columns:
            `subject_id`, `hadm_id`, `icustay_id`, `charttime`,
                `criteria_1`, `criteria_2`, `criteria_3`, `criteria_4`
        - Do NOT modify the original DataFrame (for this function)
        - No other error checking is required.

    HINTS:
        - Your implementation of summarize_sirs should call each of the functions
            you implemented below to determine whether or not a subject met each of the
            four SIRS criteria at a given timestamp.


    Parameters:
        df (pd.DataFrame): The DataFrame containing the labs and vitals for each subject
            at each available timestamp.

    Returns:
        sirs_df (pd.DataFrame): A version of the input DataFrame that contains a column
            for each of the four SIRS criteria, which indicate whether or not the subject
            met the criteria at each timestamp with True or False.
    """

    # Overwrite this variable with the return value
    sirs_df = df.copy()
    # ==================== YOUR CODE HERE ====================
    get_criteria_1(sirs_df)
    get_criteria_2(sirs_df)
    get_criteria_3(sirs_df)
    get_criteria_4(sirs_df)

    result_cols =   ['subject_id', 'hadm_id', 'icustay_id', 'charttime', 'criteria_1', 'criteria_2', 'criteria_3', 'criteria_4']
    
    return sirs_df[result_cols]

    
    
    # ==================== YOUR CODE HERE ====================
    

    return sirs_df


def get_criteria_1(sirs_df: pd.DataFrame) -> None:
    """
    Used to determine whether or not a subject met the first SIRS criteria at a given
    timestamp. NOTE: this is an inplace operation on the sirs_df, meaning that
    sirs_df will be modified directly within this function.

    #### Criteria 1: A body temperature of under 36 &deg;C or over 38 &deg;C

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) such that the sirs_df
            dataframe will contain a column titled `criteria_1` that contains True if
            the subject met the first SIRS criteria at the given timestamp, and False
            otherwise. (Boolean values should be utilized)
        - If a subject has a nan value for `TempC` at a given timestamp, they should
            be considered to have not met the first SIRS criteria at that timestamp (
            i.e. the value in the `criteria_1` column should be False)
        - To encorage you to learn about Pandas vectorized operations, this function
            should NOT use any loops. Instead, you should use Pandas vectorized
            operations to perform the operation as efficiently as possible.
        - No other error checking is required.

    HINTS:
        - Pandas DataFrames are designed to perform highly optimized low-level
            vectorized operations on rows and columns. Your implementation should
            utilize this functionality to perform the operation. If you are unfamiliar
            with vectorization, you may find the included pandas practice notebook helpful.
        - Be careful to ensure you are comparing the correct values/ units

    Parameters:
        sirs_df (pd.DataFrame): The DataFrame containing the labs and vitals for each subject
            at each available timestamp. This DataFrame should be directly modified in your
            implementation of this function.
    """


    # ==================== YOUR CODE HERE ====================
    sirs_df["criteria_1"] = (((sirs_df["TempC"] < 36) | (sirs_df["TempC"] > 38)) & (~sirs_df["TempC"].isna()))

    
    # ==================== YOUR CODE HERE ====================
    


def get_criteria_2(sirs_df: pd.DataFrame) -> None:
    """
    Used to determine whether or not a subject met the second SIRS criteria at a given
    timestamp.

    #### Criteria 2: Heart rate measured at over 90 beats per minute

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) such that the sirs_df
            dataframe will contain a column titled `criteria_2` that contains True if
            the subject met the second SIRS criteria at the given timestamp, and False
            otherwise.
        - If a subject has a nan value for `HeartRate` at a given timestamp, they should
            be considered to have not met the second SIRS criteria at that timestamp (
            i.e. the value in the `criteria_2` column should be False)
        - To encorage you to learn about Pandas vectorized operations, this function
            should NOT use any loops. Instead, you should use Pandas vectorized
            operations to perform the operation as efficiently as possible.
        - No other error checking is required.

    HINTS:
        - Pandas DataFrames are designed to perform highly optimized low-level
            vectorized operations on rows and columns. Your implementation should
            utilize this functionality to perform the operation. If you are unfamiliar
            with vectorization, you may find the pandas_practice notebook helpful.
        - Be careful to ensure you are comparing the correct values/ units

    Parameters:
        sirs_df (pd.DataFrame): The DataFrame containing the labs and vitals for each subject
            at each available timestamp. This DataFrame should be directly modified in your
            implementation of this function.
    """


    # ==================== YOUR CODE HERE ====================
    
    sirs_df["criteria_2"] = ((sirs_df["HeartRate"] > 90) & (~sirs_df["HeartRate"].isna()))
    
    # ==================== YOUR CODE HERE ====================
    


def get_criteria_3(sirs_df: pd.DataFrame) -> None:
    """
    Used to determine whether or not a subject met the third SIRS criteria at a given
    timestamp.

    #### Criteria 3: Respiratory rate measured at over 20 breaths per minute `OR` a PaCO2 level of under 32 mmHg

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) such that the sirs_df
            dataframe will contain a column titled `criteria_3` that contains True if
            the subject met the third SIRS criteria at the given timestamp, and False
            otherwise. (Boolean values should be utilized)
        - If a subject has a nan value for `RespRate` OR `PaCO2` at a given timestamp,
            they should be considered to have not met the third SIRS criteria at that
            timestamp (i.e. the value in the `criteria_3` column should be False)
        - To encorage you to learn about Pandas vectorized operations, this function
            should NOT use any loops. Instead, you should use Pandas vectorized
            operations to perform the operation as efficiently as possible.
        - No other error checking is required.

    HINTS:
        - Pandas DataFrames are designed to perform highly optimized low-level
            vectorized operations on rows and columns. Your implementation should
            utilize this functionality to perform the operation. If you are unfamiliar
            with vectorization, you may find the pandas_practice notebook helpful.
        - Be careful to ensure you are comparing the correct values/ units

    Parameters:
        sirs_df (pd.DataFrame): The DataFrame containing the labs and vitals for each subject
            at each available timestamp. This DataFrame should be directly modified in your
            implementation of this function.
    """


    # ==================== YOUR CODE HERE ====================
    
    sirs_df["criteria_3"] = (((sirs_df["RespRate"] > 20) | (sirs_df["PaCO2"] < 32)) & (~sirs_df["PaCO2"].isna()) & (~sirs_df["RespRate"].isna()))
    # sirs_df["criteria_3"] = ((sirs_df["RespRate"] > 20) | (sirs_df["PaCO2"] < 32))
    
    # ==================== YOUR CODE HERE ====================
    


def get_criteria_4(sirs_df: pd.DataFrame) -> None:
    """
    Used to determine whether or not a subject met the fourth SIRS criteria at a given
    timestamp.

    #### Criteria 4: A white blood cell count that meets *at least one* of the following criteria:
        - over 12,000 cells/mm  (WBC > 12)
        - under 4,000 cells/mm  (WBC < 4)
        - greater than 10% immature forms (BANDS > 10)

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) such that the sirs_df
            dataframe will contain a column titled `criteria_4` that contains True if
            the subject met the fourth SIRS criteria at the given timestamp, and False
            otherwise. (Boolean values should be utilized)
        - If a subject has a nan value for `WBC` or `BANDS` at a given timestamp,
            they should be considered to have not met the fourth SIRS criteria at that
            timestamp (i.e. the value in the `criteria_4` column should be False)
        - To encorage you to learn about Pandas vectorized operations, this function
            should NOT use any loops. Instead, you should use Pandas vectorized
            operations to perform the operation as efficiently as possible.
        - No other error checking is required.

    HINTS:
        - Pandas DataFrames are designed to perform highly optimized low-level
            vectorized operations on rows and columns. Your implementation should
            utilize this functionality to perform the operation. If you are unfamiliar
            with vectorization, you may find the pandas_practice notebook helpful.
        - Be careful to ensure you are comparing the correct values/ units

    Parameters:
        sirs_df (pd.DataFrame): The DataFrame containing the labs and vitals for each subject
            at each available timestamp. This DataFrame should be directly modified in your
            implementation of this function.
    """


    # ==================== YOUR CODE HERE ====================
    
    sirs_df["criteria_4"] = ((((sirs_df["WBC"] > 12) | (sirs_df["WBC"] < 4)) | (sirs_df["BANDS"] > 10)) & (~sirs_df["BANDS"].isna()) & (~sirs_df["WBC"].isna()))
    
    # ==================== YOUR CODE HERE ====================
    
