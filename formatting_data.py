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

from strava_access import DownloadData

# %% --------------------------------------------------------------------------
# Download Data
# -----------------------------------------------------------------------------
data = DownloadData()
data.get_access_token()
data.download_data() 
data.json_save()

# data.all_activities


# %%
