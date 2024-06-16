"""
survival.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""


import pandas as pd
import numpy as np
from typing import Tuple, List
import matplotlib.pyplot as plt


def calc_survival_time(cohort: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a Dataframe containing the survival time for each patient in the
    cohort dataframe. The survival time is defined as follows:
        - If the patient died during their stay, the survival time is the number
            of days between admission and death.
        - If the patient survived their stay, the survival time is the number of
            days between admission and censorship. Censorship occurs when a patient
            is discharged from the hospital without dying. We use the term censorship
            as it implies that we do not know the exact survival time for that patient,
            only that they survived at least that long.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below where specified.
        - Calculate the survival time for each patient in the cohort dataframe and store
            the results in a column named "survival_time_in_days".
        - In the returned dataframe, only include the columns "subject_id", "death_in_stay",
            "survival_time_days", and "oxy_drop".
        - Do NOT modify the input dataframe.
    """

    # Overwrite this return variable in your implementation
    survival_df = None


    # ==================== YOUR CODE HERE ====================
    survival_df = cohort.copy()

    ## index_time is 12 hours into admission 
    time_cols = ['index_time', 'deathtime', 'exposure_time', 'censor_time']
    for time_col in time_cols: 
        survival_df[time_col] = pd.to_datetime(survival_df[time_col], format="%Y-%m-%d %H:%M:%S", utc=True)

    survival_df.loc[survival_df['death_in_stay']=='died', 'survival_time_days'] = (survival_df['deathtime'] - survival_df['index_time']-pd.Timedelta(hours=12))
    survival_df.loc[survival_df['death_in_stay']=='survived', 'survival_time_days'] = ((survival_df['censor_time'] - survival_df['index_time']-pd.Timedelta(hours=12)))

    survival_df['survival_time_days'] = survival_df['survival_time_days'].apply(lambda x: x.days)

    survival_df = survival_df[["subject_id", "death_in_stay", "survival_time_days", "oxy_drop"]]

    # ==================== YOUR CODE HERE ====================
    

    return survival_df


def display_kaplan_meier_curve(
    survival_df: pd.DataFrame, output_path: str = None
) -> None:
    """
    Creates and displays a Kaplan-Meier curve using the survival data in the
    survival_df dataframe. If output_path is specified, saves the plot to that
    file path.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below where specified.
        - Use the survival data to generate a Kaplan-Meier curve for each oxy_drop
            group. Display both curves on the same plot. The x-axis should be labeled
            "Survival Time Days" and the y-axis should be labeled "Survival Probability".
        - If output_path is specified (not None), save your plot to that file path.
        - You may utilize pandas and/or numpy to help you calculate the survival probability
            for each time point for each oxy_drop group. However, you may not use any
            functions that are specifically designed to calculate a Kaplan-Meier curve.
        - Use the function plt.step() to plot the Kaplan-Meier curve.

    HINTS:
    This function can be tricky to implement! There are multiple ways to implement
    this function, but one way is to follow the steps below:
        - Sort the survival_df in ascending order of survival_time_days.
        - Group the data by oxy_drop and survival_time_days. This gives you the
            number of patients who died and survived at each time point for each
            oxy_drop group.
        - Count the number of patients who died at each time point for
            each oxy_drop group.
        - Count the number of patients who were censored at each time point for
            each oxy_drop group.
        - Sort the dataframe again by oxy_drop and survival_time_days, but this time
            in descending order of survival_time_days. This is important for the
            next step.
        - Using the counts of patients who died and were censored at each time point
            for each oxy_drop group, calculate the number of patients at risk at each
            time point for each oxy_drop group. This is the number of patients who
            either died or were censored **at that time point or later**. Since we
            sorted the dataframe in descending order of survival_time_days, we can
            calculate this by cumulatively summing the number of patients who died
            and were censored up to but not including each time point for each oxy_drop
            group.
            - NOTE: There are multiple ways to do this, but one way is to use the
            pandas.DataFrame.cumsum() function
        - Using the number of patients at risk and the number of patients who died
            at each time point for each oxy_drop group, calculate the survival
            probability at each time point for each oxy_drop group.
            - NOTE: There are multiple ways to do this, but one way is to use the
            pandas.DataFrame.cumprod() function
        - Plot the Kaplan-Meier curve for each oxy_drop group on the same plot.

    Parameters:
        survival_df (pd.DataFrame): A dataframe containing the survival data
        output_path (str): The path to save the plot to. If None, do not save.
    """

    # Implement this function where specified

    # ==================== YOUR CODE HERE ====================
    
    # TODO: Implement

    oxy_group_1 = survival_df[survival_df['oxy_drop']=='oxy_drop']
    oxy_group_2 = survival_df[survival_df['oxy_drop']=='stable']

    oxy_group_1 = oxy_group_1.sort_values(by='survival_time_days')
    oxy_group_2 = oxy_group_2.sort_values(by='survival_time_days')
    oxy_group_1['death_in_stay'] = oxy_group_1['death_in_stay'].replace({"died": 1, 'survived': 0})
    oxy_group_2['death_in_stay'] = oxy_group_2['death_in_stay'].replace({"died": 1, 'survived': 0})
    # survival_df_grouped = survival_df_sorted.groupby(by=['oxy_drop', 'survival_time_days'], as_index=False).count()
    oxy_group_1_grouped = pd.pivot_table(oxy_group_1, index=['oxy_drop', 'survival_time_days'], 
                                         values=["subject_id", 'death_in_stay'], aggfunc={"subject_id":len, 'death_in_stay':np.sum}).reset_index()
    oxy_group_2_grouped = pd.pivot_table(oxy_group_2, index=['oxy_drop', 'survival_time_days'], 
                                         values=["subject_id", 'death_in_stay'], aggfunc={"subject_id":len, 'death_in_stay':np.sum}).reset_index()
    oxy_group_1 = oxy_group_1_grouped.rename(columns={'subject_id':'total_ids', 'death_in_stay':'death_count'})
    oxy_group_2 = oxy_group_2_grouped.rename(columns={'subject_id':'total_ids', 'death_in_stay':'death_count'})
    oxy_group_1['censored_count'] = oxy_group_1['total_ids']-oxy_group_1['death_count']
    oxy_group_2['censored_count'] = oxy_group_2['total_ids']-oxy_group_2['death_count']

  
    oxy_group_1 = oxy_group_1.sort_values(by=['oxy_drop', 'survival_time_days'], ascending=[True, False])
    oxy_group_2 = oxy_group_2.sort_values(by=['oxy_drop', 'survival_time_days'], ascending=[True, False])

    oxy_group_1['num_at_risk'] = (oxy_group_1['censored_count']+oxy_group_1['death_count']).cumsum()
    oxy_group_1['num_died'] = (oxy_group_1['death_count']).cumsum()
    oxy_group_1['survive_ratio'] = (oxy_group_1['num_at_risk']-oxy_group_1['death_count']) / oxy_group_1['num_at_risk']
    
    oxy_group_2['num_at_risk'] = (oxy_group_2['censored_count']+oxy_group_2['death_count']).cumsum()
    oxy_group_2['num_died'] = (oxy_group_2['death_count']).cumsum()
    oxy_group_2['survive_ratio'] = (oxy_group_2['num_at_risk']-oxy_group_2['death_count']) / oxy_group_2['num_at_risk']

    oxy_group_1['survival_cumprob'] = (oxy_group_1['survive_ratio'])[::-1].cumprod()[::-1]
    oxy_group_2['survival_cumprob'] = (oxy_group_2['survive_ratio'])[::-1].cumprod()[::-1]
    
    plt.figure(figsize=(10, 6)) 
    plt.step(oxy_group_1['survival_time_days'], oxy_group_1['survival_cumprob'], label='oxy_drop')
    plt.step(oxy_group_2['survival_time_days'], oxy_group_2['survival_cumprob'], label='stable')
    plt.ylim([0, 1])
    plt.ylabel('Survival Probability')
    plt.xlabel('Survival Time Days')
    plt.legend() 
    # plt.show()

    if output_path: 
        plt.savefig(output_path)
    
    # ==================== YOUR CODE HERE ====================


# NOTE: For any helper functions you choose to implement, please include a docstring 
#       that briefly describes the function and its parameters/returns.
#       This will help us better understand your code for awarding partial credit.

