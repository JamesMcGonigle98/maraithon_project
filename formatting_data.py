"""
Formatting Data from Strava API

Changing the data into a nicer format
"""

__date__ = "2023-10-09"
__author__ = "JamesMcGonigle"



# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# %% --------------------------------------------------------------------------
# Format Data Class
# -----------------------------------------------------------------------------
class FormatData():

    def __init__(self, all_activities):

        self.all_activities = all_activities

    def json_to_df(self):

        rows_list = []

        # Loop through the activities
        for activity in self.all_activities:
            try:
                new_row = {
                    'name': activity['name'],
                    'distance': activity['distance'],
                    'moving_time': activity['moving_time'],
                    'total_elevation_gain': activity['total_elevation_gain'],
                    'type': activity['sport_type'],
                    'start_date': activity['start_date']
                }
                rows_list.append(new_row)
            except KeyError:
                # Handle missing keys or continue
                continue

        self.activities_df = pd.DataFrame(rows_list)        

    def cleaning_up_df(self):

        self.activities_df = self.activities_df.sort_values('start_date', ascending=True)

        self.activities_df['start_date'] = self.activities_df['start_date'].str[:10] # Reformat Start Dates
        self.activities_df['month'] = self.activities_df['start_date'].str[5:7] # Reformat Start Dates

        self.activities_df['type'] = self.activities_df['type'].replace('Soccer', 'Workout') # Change Soccer to Workout

        self.running_df = self.activities_df[self.activities_df['type']=='Run'] # Split between Running and Workout
        self.workout_df = self.activities_df[self.activities_df['type']=='Workout'] # Split between Running and Workout

    def month_agg(self):
        
        self.aggregated_running_df = self.running_df.groupby('month').agg({
            'moving_time': 'sum',
            'distance': 'sum'
            }).reset_index()

        self.aggregated_workout_df = self.workout_df.groupby('month').agg({
            'moving_time': 'sum',
            'distance': 'sum'
            }).reset_index()
