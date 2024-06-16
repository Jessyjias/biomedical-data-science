"""
note_processing.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""

# Imports - Do not modify
import pandas as pd
from typing import List
import re

# ==================== CONSTANTS: DO NOT MODIFY ====================
SEARCH_STRINGS = ["sepsis", "septic"]


def summarize_notes(notes: pd.DataFrame, indicator_column_name: str) -> pd.DataFrame:
    """
    Determines whether or not a patient has an infection utilizing the
    SEARCH_STRINGS provided above. For each unique (`subject_id`, `hadm_id`)
    pair, determine whether or not the patient has an infection by checking
    to see if any of the notes in the `note_text` column of the input DataFrame
    contain ANY of the SEARCH_STRINGS provided above (case insensitive).

    EXAMPLE: If one of the notes in the `note_text` column for a given
    (`subject_id`, `hadm_id`) pair is "Patient has Sepsis", then the patient
    has an infection because "sepsis" is one of the SEARCH_STRINGS provided
    above. (Notice that this is case insensitive, so "sepsis" and "Sepsis"
    would both be considered to be a match.)

    The final output DataFrame should contain a single row for each unique
    (`subject_id`, `hadm_id`) pair, and a column <indicator_column_name> which
    is True if the patient has an infection and False otherwise.

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) return a new DataFrame
            that contains ONLY the columns `subject_id`, `hadm_id`, and <indicator_column_name>,
            such that each row is a unique (`subject_id`, `hadm_id`) pair and
            <indicator_column_name> is True if the patient has an infection and False otherwise.
        - A patient should be considered to have an infection if any of the
            corresponding notes in the `note_text` column contain ANY of the
            SEARCH_STRINGS provided above (case insensitive).
        - Consider any row of the original DataFrame to NOT indicate an infection
            if the `note_text` column is null. Examples:
                - if a patient has a note that contains one of the SEARCH_STRINGS
                provided above AND also has null note for a particular (`subject_id`, `hadm_id`)
                pair, then that (`subject_id`, `hadm_id`) should be considered to
                correspond to an infection.
                - If a patient only has null notes for a particular (`subject_id`, `hadm_id`)
                pair, then that (`subject_id`, `hadm_id`) should NOT correspond
                to an infection.
        - Do NOT modify the input DataFrame.
        - No other error checking is required.

    Parameters:
        notes (pd.DataFrame): A DataFrame containing the columns `subject_id`,
            `hadm_id`, and `note_text`.

    Returns:
        infection_df (pd.DataFrame): A DataFrame containing ONLY the columns
            `subject_id`, `hadm_id`, and <indicator_column_name> (True if the patient
            has an infection and False otherwise).
    """

    # Overwrite this variable with the return value
    infection_df = None


    # ==================== YOUR CODE HERE ====================
    
    infection_df = notes[['subject_id', 'hadm_id', 'note_text']]
    # infection_df[indicator_column_name] = (infection_df['note_text'].apply(lambda x: any(substring in x for substring in SEARCH_STRINGS)))
    pattern = '|'.join(SEARCH_STRINGS)
    infection_df[indicator_column_name]  = infection_df['note_text'].str.contains(pattern, case=False, na=False).astype(int)

    infection_df[indicator_column_name] = infection_df.groupby(['subject_id', 'hadm_id'], as_index=False)[indicator_column_name].transform('max')
    infection_df = infection_df[['subject_id', 'hadm_id', indicator_column_name]].drop_duplicates(subset=['subject_id', 'hadm_id'])
    infection_df[indicator_column_name] = infection_df[indicator_column_name].astype(int)
    
    # ==================== YOUR CODE HERE ====================
    

    return infection_df
