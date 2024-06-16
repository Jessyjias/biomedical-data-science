"""
BIOMEDIN 215: Assignment 4
features.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""

import pandas as pd
import numpy as np
import datetime


def get_diagnoses(
    admissions: pd.DataFrame, diagnoses: pd.DataFrame, shock_labels: pd.DataFrame
):
    """
    Utilizing the admissions, diagnoses, and shock_labels dataframes, return a
    dataframe that only contains the diagnoses that occurred BEFORE the index_time
    for patient's in the shock_labels dataframe.

    IMPLEMENTATION INSTRUCTIONS:
       - Implement the function below to return a dataframe that contains
            the diagnoses that occurred BEFORE the index_time for patient's in the
            shock_labels dataframe with the following columns:
                - `subject_id`: the unique identifier for each patient
                - `hadm_id`: the unique identifier for each patient hospital admission
                - `diagnosis_time`: the time of the diagnosis
                - `icd9_code`: the icd9 code for the diagnosis
                - `index_time`: the time of the shock diagnosis
         - Utilize the appropriate columns in admissions, diagnoses, and shock_labels
            dataframes to pull the information needed.

    Parameters:
        admissions (pd.DataFrame): a dataframe containing the admissions information
        diagnoses (pd.DataFrame): a dataframe containing the diagnoses information
        shock_labels (pd.DataFrame): a dataframe containing the shock labels for
            each patient in the cohort

    Returns:
        dx (pd.DataFrame): a dataframe containing the diagnoses that occurred BEFORE
            the index_time for patient's in the shock_labels dataframe
    """

    # Overwrite this variable with the return value in your implementation
    dx = None


    # ==================== YOUR CODE HERE ====================
    admissions_merge = admissions[['hadm_id', 'subject_id', 'dischtime', 'admittime']]
    diagnosis_merge = diagnoses[['subject_id', 'hadm_id', 'icd9_code']]

    joined_table = admissions_merge.merge(diagnosis_merge, how='inner', on=['subject_id', 'hadm_id'], suffixes=['', '_'])
    joined_table = joined_table[['subject_id', 'hadm_id', 'icd9_code', 'dischtime', 'admittime']]
    shock_labels_merge = shock_labels[['hadm_id', 'subject_id', 'index_time']]
    merged = pd.merge(joined_table, shock_labels_merge, on=['subject_id'], how='inner', suffixes=['', '_'])

    # return merged
    dx = merged[(merged['dischtime'] < merged['index_time']) & (merged['dischtime'] >= merged['admittime'])]
    dx = dx[['subject_id', 'hadm_id', 'icd9_code', 'dischtime', 'index_time']]
    dx.rename(columns={'dischtime': 'diagnosis_time'}, inplace=True)
    
    
    # ==================== YOUR CODE HERE ====================
    

    return dx


def calc_ic(dx_features: pd.DataFrame, all_patients_count: int) -> pd.DataFrame:
    """
    Calculate the IC score for each diagnosis in the dx_features dataframe.

    IMPLEMENTATION INSTRUCTIONS:
         - Implement the function below to return a dataframe that contains
            the IC score for each diagnosis in the dx_features dataframe with
            the following columns:
                - `icd9_code`: the icd9 code for the diagnosis
                - `IC`: the IC score for the diagnosis
            - Utilize the appropriate columns in the dx_features dataframe to pull
                the information needed.
            - Your implementation should utilize the all_patients_count variable to
                calculate the IC score for each diagnosis.

    HINTS:
        - You can use numpy functions to opperate on dataframe columns.
        - Check out the .agg function in pandas to determine the number of unique
            patients with each diagnosis icd9_code. (You may find it helpful
            to use this with the .groupby function.)

    Parameters:
        dx_features (pd.DataFrame): a dataframe containing the valid diagnosis
            features for each patient in the cohort
        all_patients_count (int): the number of patients in the cohort

    Returns:
        icd9_ic (pd.DataFrame): a dataframe containing the IC score for each
            diagnosis icd9 code in the dx_features dataframe
    """

    # Overwrite this variable with the return value in your implementation
    icd9_ic = None


    # ==================== YOUR CODE HERE ====================
    subject_counts = dx_features.groupby(by='icd9_code', as_index=False)['subject_id'].unique()
    subject_counts['unique_patient_id_count'] = [len(x) for x in subject_counts['subject_id']]

    subject_counts['icd9_ic'] = -1*np.log2(subject_counts['unique_patient_id_count']/all_patients_count)

    icd9_ic = pd.merge(dx_features, subject_counts, on='icd9_code', how='inner')
    icd9_ic.drop_duplicates(subset=['icd9_code'], inplace=True)
    icd9_ic = icd9_ic[['icd9_code', 'icd9_ic']]

    # ==================== YOUR CODE HERE ====================
    

    return icd9_ic


def filter_ic(dx_features: pd.DataFrame, icd9_ic: pd.DataFrame) -> pd.DataFrame:
    """
    Filters the dx_features dataframe to only include diagnoses that have an IC
    value between 4 and 9 (inclusive).

    IMPLEMENTATION INSTRUCTIONS:
        - Return a filtered version of the dx_features dataframe (with the same
            columns) that only contains diagnoses that have an IC value between
            4 and 9 (inclusive).

    Parameters:
        dx_features (pd.DataFrame): a dataframe containing the valid diagnosis
            features for each patient in the cohort
        icd9_ic (pd.DataFrame): a dataframe containing the IC score for each
            diagnosis icd9 code in the dx_features dataframe

    Returns:
        dx_filtered (pd.DataFrame): a dataframe containing the filtered diagnosis
            features for each patient in the cohort
    """

    # Overwrite this variable with the return value in your implementation
    dx_filtered = None


    # ==================== YOUR CODE HERE ====================
    dx_filtered = pd.merge(dx_features, icd9_ic, on='icd9_code', how='inner')

    dx_filtered = dx_filtered[(dx_filtered['icd9_ic']>=4) & (dx_filtered['icd9_ic']<=9)]
    
    dx_filtered.drop(columns='icd9_ic', inplace=True)
    # ==================== YOUR CODE HERE ====================
    

    return dx_filtered


def get_diagnosis_features(dx_selected: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a patient-feature matrix that summarizes and organizes diagnoses features.

        Each row represents a patient and each column represents a time-binned
        diagnosis code, where there are two bins (RECENT and PRIOR).
            - RECENT: diagnoses that occurred within 6 months of the index time
            - PRIOR: diagnoses that occurred more than 6 months before the index time

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below to return a dataframe that contains
            the patient-feature matrix with the following columns:
                - `subject_id`: the unique identifier for each patient
                And the following columns for each diagnosis code:
                - `RECENT_<icd9_code>`: the number of times the diagnosis occurred
                    within 6 months of the index time
                - `PRIOR_<icd9_code>`: the number of times the diagnosis occurred
                    more than 6 months before the index time
                - For date calculations, assume that 1 month == 30.44 days

    HINTS:
        - A great way to implement this function is to first create a new column
            called `time_bin` that indicates if each diagnosis should be considered
            RECENT or PRIOR.
        - Then, you can use the pandas groupby function to count the number of times
            each diagnosis occurred for each patient.
        - Your implementation should utilize the pandas_pivot function.
        - You may find it helpful to write helper functions to complete this task.

    Parameters:
        dx_selected (pd.DataFrame): a dataframe containing the filtered diagnosis
            features for each patient in the cohort

    Returns:
        patient_diagnosis_features (pd.DataFrame): a dataframe containing the
            patient-feature matrix for diagnoses

    """

    # Overwrite this variable with the return value in your implementation
    patient_diagnosis_features = None


    # ==================== YOUR CODE HERE ====================
    days_6months = 30.44*6
    dx_selected['RECENT'] = ((dx_selected['index_time'] - dx_selected['diagnosis_time']) <= datetime.timedelta(days=days_6months)).astype(int)
    dx_selected['PRIOR'] = ((dx_selected['index_time'] - dx_selected['diagnosis_time']) > datetime.timedelta(days=days_6months)).astype(int)
    
    dx_selected = dx_selected[['subject_id', 'icd9_code', 'RECENT', 'PRIOR']]
    patient_diagnosis_features = dx_selected.groupby(['subject_id', 'icd9_code'], as_index=False).sum()
    # patient_diagnosis_features = patient_diagnosis_features[['subject_id', 'icd9_code', 'RECENT', 'PRIOR']]
    # patient_diagnosis_features.rename(columns={'RECENT':'count'}, inplace=True)

    patient_diagnosis_features = pd.pivot_table(patient_diagnosis_features, 
                                                index='subject_id', 
                                                values = ['RECENT', 'PRIOR'], 
                                                columns = 'icd9_code', 
                                                aggfunc="count"
                                                )
    
    patient_diagnosis_features.columns = ["_".join(x) for x in patient_diagnosis_features.columns]
    patient_diagnosis_features.reset_index(inplace=True)

    # ==================== YOUR CODE HERE ====================
    

    return patient_diagnosis_features


# NOTE: Feel free to add additional helper functions if you wish!



# NOTE: For any helper functions you choose to implement, please include a docstring 
#       that briefly describes the function and its parameters/returns.
#       This will help us better understand your code for awarding partial credit.

