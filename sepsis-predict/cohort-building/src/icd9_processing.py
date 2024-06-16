"""
icd9_processing.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.

"""


# Imports - Do not modify
import pandas as pd
from typing import List, Dict
import re


# ==================== CONSTANTS: DO NOT MODIFY ====================
INFECTION_ICD9_PREFIX = """
                    001,002,003,004,005,008,009,010,011,012,
                    013,014,015,016,017,018,020,021,022,023,
                    024,025,026,027,030,031,032,033,034,035,
                    036,037,038,039,040,041,090,091,092,093,
                    094,095,096,097,098,100,101,102,103,104,
                    110,111,112,114,115,116,117,118,320,322,
                    324,325,420,421,451,461,462,463,464,465,
                    481,482,485,486,494,510,513,540,541,542,
                    566,567,590,597,601,614,615,616,681,682,
                    683,686,730,5695,5720,5721,5750,5990,7110,
                    7907,9966,9985,999349121,56201,56203,56211,
                    56213,56983
                    """

ORGAN_DISFUNCTION_ICD9_PREFIX = """
                    458,293,570,584,7855,3483,3481,2874,2875,
                    2869,2866,5734
                    """

DEBUG_ICD9_PREFIX = """
115, 125
"""


# ==================== HELPER FUNCTION: DO NOT MODIFY ====================
def parse_prefix(icd9_prefix_list: str) -> List[str]:
    """
    NOTE: This function is provided for your convenience. Do not modify.

    Returns a list of ICD-9 code prefixes from the input strings.

    Use this function to parse the ICD-9 code prefixes from the
    INFECTION_3_DIGIT, INFECTION_4_DIGIT, and INFECTION_5_DIGIT
    variables above.

    Parameters:
        icd9_prefix_list (str): A string containing comma-separated ICD-9 code
            prefixes.

    Returns:
        icd9_prefixes (List[str]): A list of ICD-9 code prefixes.
    """

    # Split the string on commas and remove any whitespace
    icd9_prefixes = icd9_prefix_list.split(",")

    # Remove any empty strings
    icd9_prefixes = [re.sub(r"\D", "", prefix) for prefix in icd9_prefixes if prefix]

    return icd9_prefixes


def create_prefix_dict() -> Dict[str, List[str]]:
    """
    NOTE: This function is provided for your convenience. Do not modify.

    Creates a dictionary that maps a word to a list of ICD-9 code prefixes.

    Returns:
        prefix_dict (Dict[str, List[str]]): A dictionary that maps a word to a list
            of ICD-9 code prefixes.
    """

    # Create a dictionary that maps a word to a list of ICD-9 code prefixes
    prefix_dict = {
        "infection": parse_prefix(INFECTION_ICD9_PREFIX),
        "organ_disfunction": parse_prefix(ORGAN_DISFUNCTION_ICD9_PREFIX),
        "debug": parse_prefix(DEBUG_ICD9_PREFIX),
    }

    return prefix_dict


# ==================== DO NOT MODIFY ABOVE THIS LINE ====================


def summarize_icd9(
    diagnoses: pd.DataFrame,
    subject_ids: List[int],
    indicator_column_name: str,
    icd9_prefix_list: str,
) -> pd.DataFrame:
    """
    Returns a DataFrame containing only the columns `subject_id`, `hadm_id`, and
    `<indicator_column_name>` where each row is a unique (`subject_id`, `hadm_id`)
    pair and <indicator_column_name> is 1 if the patient has an ICD-9 code that
    starts with ANY of the ICD-9 code prefixes provided, and 0 otherwise.

    The diagnoses DataFrame contains ICD-9 codes for ALL admissions for
    ALL patients in the MIMIC-III database. Use the `subject_ids` parameter
    to restrict the diagnoses DataFrame to only the subject_ids that appear
    in the `subject_ids` parameter. (This will reduce the size of the DataFrame
    and speed up your code.)

    Each unique (`subject_id`, `hadm_id`) pair will correspond to one or more
    rows in the diagnoses DataFrame, where each row contains a ICD-9 code for that
    (`subject_id`, `hadm_id`) pair.

    For each (`subject_id`, `hadm_id`) pair, determine whether or not the patient
    has any ICD-9 codes that start with ANY of the ICD-9 code prefixes provided
    above. If the patient has an ICD-9 code that starts with ANY of the ICD-9 code
    prefixes provided above, then the <indicator_column_name> should be 1 for that
    (`subject_id`, `hadm_id`) pair. If the patient does NOT have an ICD-9 code that
    starts with ANY of the ICD-9 code prefixes provided above, then the
    <indicator_column_name> should be 0 for that (`subject_id`, `hadm_id`) pair.

    EXAMPLE: If one of the ICD-9 codes in the `icd9_code` column for a given
    (`subject_id`, `hadm_id`) pair is "11511", then the patient has an infection
    because "11511" starts with "115" which is one of the ICD-9 code prefixes
    provided above.

    For all subject_id's in the `subject_id_list` parameter, the final output
    DataFrame should contain a single row for each unique (`subject_id`, `hadm_id`)
    pair, and a column `<indicator_column_name>` which is 1 if the patient has an
    an ICD-9 code with a prefix from the sets above and 0 otherwise.

    IMPLEMENTATION INSTRUCTIONS:
        - Complete the function below (where indicated) to return a new DataFrame
            that contains ONLY the columns `subject_id`, `hadm_id`, and
            `<indicator_column_name>`, such that each row is a unique
            (`subject_id`, `hadm_id`) pair has an `<indicator_column_name>` that
            is 1 if the patient has a relevant ICD-9 code and 0 otherwise.
        - First, use the `subject_ids` parameter to restrict the diagnoses DataFrame
            to only the subject_ids that appear in the `subject_ids` list.
        - A patient should be considered to have an infection if any of the corresponding
            ICD-9 codes in the `icd9_code` column start with ANY of the relevant ICD-9 code
            prefixes.
        - Consider any row of the original DataFrame to NOT indicate an the presence of
            a relevant ICD-9 code if the `icd9_code` column is null. Examples:
                - if a patient has code that starts with one of the ICD-9 code prefixes
                provided above AND also has null code for a particular (`subject_id`, `hadm_id`)
                pair, then the `<indicator_column_name>` for that (`subject_id`, `hadm_id`)
                should be considered to correspond to an infection.
                - If a patient only has null codes for a particular (`subject_id`, `hadm_id`)
                pair, then that (`subject_id`, `hadm_id`) should NOT correspond
                to an infection.
        - Do NOT modify the input DataFrame.
        - No other error checking is required.

    HINTS:
        - Your implementation should utilize the pandas groupby function.
        - You may find the pandas.Series.str.startswith function useful.
        - You may find the pandas.Series.fillna function useful.

    Parameters:
        diagnoses (pd.DataFrame): A DataFrame containing the columns
            `subject_id`, `hadm_id`, and `icd9_code`.
        subject_ids (List[int]): A list of subject_ids to restrict the diagnoses
            DataFrame to.
        indicator_column_name (str): The name of the column that indicates whether
            or not the patient has an infection. (TODO: Your implementation should
            use the value of this parameter to name the column that indicates whether
            or not the patient has a relevant ICD9.)
        icd9_prefix_list (str): A string name of the ICD-9 code prefixes to use
            when determining whether or not a patient has an infection. (This is
            only for selecting the appropriate ICD-9 code prefixes, which is
            taken care of for you. You should not use the parameter directly.)

    Returns:
        icd9_df (pd.DataFrame): A DataFrame containing the columns
            `subject_id`, `hadm_id`, and `has_infection`, such that each row
            is a unique (`subject_id`, `hadm_id`) pair and `has_infection` is 1
            if the patient has an infection and 0 otherwise.
    """

    # Overwrite this variable with the return value
    icd9_df = None

    # This gets a string list of ICD-9 code prefixes from the constants above
    # You should use icd9_prefixes in your implementation below
    icd9_prefixes = create_prefix_dict()[icd9_prefix_list]


    # ==================== YOUR CODE HERE ====================
    diagnoses_target = diagnoses[diagnoses['subject_id'].isin(subject_ids)]
    # diagnoses_target.fillna('nan', inplace=True)
    diagnoses_target[indicator_column_name] = (diagnoses_target['icd9_code'].apply(lambda x: str(x).startswith(tuple(icd9_prefixes))))
    diagnoses_target[indicator_column_name] = diagnoses_target.groupby(['subject_id', 'hadm_id'], as_index=False)[indicator_column_name].transform('max')
    icd9_df = diagnoses_target[['subject_id', 'hadm_id', indicator_column_name]].drop_duplicates(subset=['subject_id', 'hadm_id'])
    icd9_df[indicator_column_name] = icd9_df[indicator_column_name].astype(int)
    # ==================== YOUR CODE HERE ====================
    

    return icd9_df
