"""
Plotting Strava Data

Different plots of my Strava Data
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
# Download Data and Formatting
# -----------------------------------------------------------------------------
data = DownloadData()
data.get_access_token()
data.download_data() 
data.json_save()

formatted_data = FormatData(data.all_activities)
formatted_data.json_to_df()
formatted_data.cleaning_up_df()
formatted_data.month_agg()

# formatted_data.running_df
# formatted_data.workout_df
# formatted_data.aggregated_running_df
# formatted_data.aggregated_workout_df


# %% --------------------------------------------------------------------------
# Plotting Running vs Non Running Activities
# -----------------------------------------------------------------------------
agg_comb = formatted_data.aggregated_workout_df.merge(formatted_data.aggregated_running_df, on='month', how='outer')
agg_comb = agg_comb.fillna(0)
agg_comb = agg_comb.sort_values('month')
agg_comb['moving_time_x'] = agg_comb['moving_time_x']/60
agg_comb['moving_time_y'] = agg_comb['moving_time_y']/60

agg_comb['total_time'] = agg_comb['moving_time_x'] + agg_comb['moving_time_y']


month_dict = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
    }

# Replace numeric month values with string representation
agg_comb['month'] = agg_comb['month'].replace(month_dict)

x = agg_comb["month"]
y1 = agg_comb["moving_time_x"]
y2 = agg_comb["moving_time_y"]
y3 = agg_comb["total_time"]

plt.plot(x, y1, label = "Time Spend Doing Non-Running Training")
plt.plot(x, y2, label = "Time Spent Running")
plt.plot(x, y3, linestyle=':', label = "Total Time Training")
plt.legend()
plt.title('Comparison of Running to Non-Running Training')
plt.xlabel('Month')
plt.ylabel('Time Spend Exercising (Minutes)')
plt.legend(fontsize='small')
plt.ylim(0, 700)


