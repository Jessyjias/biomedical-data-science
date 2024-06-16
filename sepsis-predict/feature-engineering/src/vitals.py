"""
BIOMEDIN 215: Assignment 4
vitals.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""


import pandas as pd
import numpy as np
from typing import List


def filter_vitals(
    vitals: pd.DataFrame, shock_labels: pd.DataFrame, vitals_to_keep: List[str]
):
    """
    Filters the vitals dataframe to only include the vital measurements that have
    their vital_id include in vitals_to_keep, and only includes the vital measurements
    that were taken before the index_time for each patient. (NOTE: This is strictly
    before, not inclusive of the index_time.)

    IMPLEMENTATION INSTRUCTIONS:
        - Return a filtered version of the vitals dataframe that only includes the
            vital measurements that have their vital_id include in vitals_to_keep, and
            only includes the vital measurements that were taken before the index_time
            for each patient.
        - You will need to select the appropriate merge strategy when merging the
            shock_labels and vitals dataframes.

    Parameters:
        vitals (pd.DataFrame): A dataframe containing the vital measurements for each
            patient.
        shock_labels (pd.DataFrame): A dataframe containing the shock labels for each
            patient, as well as the index_time for each patient.
        vitals_to_keep (List[str]): A list of vital_ids that should be kept in the
            filtered vitals dataframe.

    Returns:
        filtered_vitals (pd.DataFrame): A dataframe containing the filtered vital
            measurements for each patient.
    """

    # Overwrite this variable with the return value in your implementation
    filtered_vitals = None


    # ==================== YOUR CODE HERE ====================
    filtered_vitals = vitals[vitals['vital_id'].isin(vitals_to_keep)]
    filtered_vitals = filtered_vitals.merge(shock_labels, on=['subject_id', 'hadm_id', 'icustay_id'], how='inner')
    filtered_vitals = filtered_vitals[filtered_vitals['charttime'] < filtered_vitals['index_time']]
    
    # ==================== YOUR CODE HERE ====================
    

    return filtered_vitals


def get_latest_hr(heart_rates: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe containing the latest heart rate measurement for each patient
    prior to their index_time. The returned dataframe should contain the columns:
        - `subject_id`: The ID of the patient
        - `charttime`: The time at which the heart rate measurement was taken
        - `latest_heart_rate`: The latest heart rate measurement for the patient
        - `index_time`: The time at which the patient was diagnosed with shock
        - `label`: The shock label for the patient

    IMPLEMENTATION INSTRUCTIONS:
        - Return a dataframe containing the latest heart rate measurement for each
            patient prior to their index_time.

    Parameters:
        heart_rates (pd.DataFrame): A dataframe containing the heart rate measurements
            for each patient.

    Returns:
        latest_hr_df (pd.DataFrame): A dataframe containing the latest heart rate
            measurement for each patient prior to their index_time.
    """

    # Overwrite this variable with the return value in your implementation
    latest_hr_df = None


    # ==================== YOUR CODE HERE ====================
    
    latest_hr_df = heart_rates.copy()
    latest_hr_df = latest_hr_df.sort_values('charttime')
    latest_hr_df = latest_hr_df.groupby('subject_id').tail(1)

    latest_hr_df = latest_hr_df[['subject_id', 'charttime', 'valuenum', 'index_time', 'label']]
    latest_hr_df = latest_hr_df.rename(columns={'valuenum':'latest_heart_rate'})

    # latest_hr_df_2 = latest_hr_df.sort_values(['subject_id', 'charttime'], ascending=[True, False])
    # latest_hr_df_2 = latest_hr_df_2.drop_duplicates('subject_id', keep='first')
    
    # ==================== YOUR CODE HERE ====================
    

    return latest_hr_df


def get_time_weighted_hr(heart_rates: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a dataframe containing the time-weighted average heart rate for each
    patient, using the hr vitals taken prior to their index_time. The returned
    dataframe should contain the columns:
        - `subject_id`: The ID of the patient
        - `time_wt_avg`: The time-weighted average heart rate for the patient


    IMPLEMENTATION INSTRUCTIONS:
        - Return a dataframe containing the time-weighted average heart rate for each
            patient, using the hr vitals taken prior to their index_time.
        - Calculate the weight values for each heart rate measurement using the
            provided formula.
            weight = exp(-|dt| - 1) where dt is the time difference in hours between
            the charttime and the index_time.
        - Calculate the time-weighted average heart rate for each patient as follows:
            time_wt_avg[patient A] = sum(weights[patient A] * heart_rate[patient A]) /
                sum(weights[patient A])
            Notes:
                - The time_wt_avg is a scalar value for each patient.
                - In the formula above, weights[patient A] is a vector of weight values
                    for each heart rate measurement for patient A.
                - heart_rate[patient A] is a vector of heart rate values for each
                    heart rate measurement for patient A.
                - The sum(weights[patient A] * heart_rate[patient A]) is the sum of the
                    element-wise multiplication of the weights and heart_rate vectors.
                    For example, if weights[patient A] = [1, 2, 3] and
                    heart_rate[patient A] = [4, 5, 6], then the sum(weights[patient A] *
                        heart_rate[patient A]) = (1 * 4) + (2 * 5) + (3 * 6) = 32
                - The sum(weight) is the sum of the weight values for all rows in the
                    dataframe that correspond to the same patient.

                - HINT: Whenever you see opperations being performed on a "group"
                    of rows, you should think about using the groupby function.

        - After calculating the time-weighted average heart rate for each patient,
            filter OUT any patients that have a time-weighted average heart rate of
            NaN.
        - The final dataframe should have the following columns:
            - subject_id
            - time_wt_avg
        - Do not modify the input dataframe.

    Parameters:
        heart_rates (pd.DataFrame): A dataframe containing the heart rate measurements
            for each patient.

    Returns:
        time_wt_avg_df (pd.DataFrame): A dataframe containing the time-weighted
            average heart rate for each patient.
    """

    # Overwrite this variable with the return value in your implementation
    result = None


    # ==================== YOUR CODE HERE ====================
    result = heart_rates.copy()
    result['dt'] = (result['charttime'] - result['index_time'])/ pd.Timedelta(hours=1)
    result['weight'] = np.exp(-1*abs(result['dt']) - 1)
    result['weighted_hr'] = result['weight']*result['valuenum']
    result = result[['subject_id', 'dt', 'weight', 'weighted_hr', 'valuenum']]
    subject_group = result.groupby('subject_id', as_index=False).sum()
    subject_group['time_wt_avg'] = subject_group['weighted_hr'] / subject_group['weight']
    subject_group = subject_group[['subject_id', 'time_wt_avg']]

    subject_group = subject_group.dropna()
    # ==================== YOUR CODE HERE ====================
    

    return subject_group
