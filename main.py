"""
Analysis of Strava Data

This script has all the info needed to access and analyse my Strava Data

"""

__date__ = "2023-10-09"
__author__ = "JamesMcGonigle"



# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from strava_access import DownloadData
from formatting_data import FormatData


# %% --------------------------------------------------------------------------
# Download Data
# -----------------------------------------------------------------------------
data = DownloadData()
data.get_access_token()
data.download_data() 
data.json_save()

# data.all_activities 


# %% --------------------------------------------------------------------------
# Formatting Data
# -----------------------------------------------------------------------------
formatted_data = FormatData(data.all_activities)
formatted_data.json_to_df()

formatted_data.cleaning_up_df()
# formatted_data.running_df
# formatted_data.workout_df

formatted_data.month_agg()
# formatted_data.aggregated_running_df
# formatted_data.aggregated_workout_df






# %%
