
# %% --------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import requests
import urllib3 
import json
import os
import pandas as pd

from secret_keys import client_id, client_secret, refresh_token

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# %% --------------------------------------------------------------------------
# URLs
# -----------------------------------------------------------------------------
# Define the API endpoint URL
activities_url = 'https://www.strava.com/api/v3/athlete/activities/'
auth_url = "https://www.strava.com/oauth/token"


# %% --------------------------------------------------------------------------
# Refresh Token
# -----------------------------------------------------------------------------
payload = {

    'client_id':client_id,
    'client_secret':client_secret,
    'refresh_token':refresh_token,
    'grant_type':'refresh_token',
    'f':'json'

}

res = requests.post(auth_url, data=payload, verify=False)

access_token = res.json()['access_token']


# %% --------------------------------------------------------------------------
# All activities
# -----------------------------------------------------------------------------
header = {'Authorization': f'Bearer {access_token}'}

# The first loop, request_page_number will be set to one, so it requests the first page. Increment this number after
# each request, so the next time we request the second page, then third, and so on...
request_page_num = 1
all_activities = []

while True:
    param = {'per_page': 200, 'page': request_page_num}
    # initial request, where we request the first page of activities
    my_dataset = requests.get(activities_url, headers=header, params=param).json()

    # check the response to make sure it is not empty. If it is empty, that means there is no more data left. So if you have
    # 1000 activities, on the 6th request, where we request page 6, there would be no more data left, so we will break out of the loop
    if len(my_dataset) == 0:
        print("breaking out of while loop because the response is zero, which means there must be no more activities")
        break

    # if the all_activities list is already populated, that means we want to add additional data to it via extend.
    if all_activities:
        print("all_activities is populated")
        all_activities.extend(my_dataset)

    # if the all_activities is empty, this is the first time adding data so we just set it equal to my_dataset
    else:
        print("all_activities is NOT populated")
        all_activities = my_dataset

    request_page_num += 1

print(len(all_activities))
for count, activity in enumerate(all_activities):
    print(activity["name"])
    print(count)


    
# %% --------------------------------------------------------------------------
# Saving json
# -----------------------------------------------------------------------------
file_path = rf"assets/activities.json"

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, 'w') as json_file:
    json.dump(all_activities, json_file)



# %% --------------------------------------------------------------------------
# New Activities
# -----------------------------------------------------------------------------
rows_list = []

# Loop through the activities
for activity in all_activities:
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

activities_df = pd.DataFrame(rows_list)



# %% --------------------------------------------------------------------------
# Formatting of Dataframe
# -----------------------------------------------------------------------------
activities_df = activities_df.sort_values('start_date', ascending=True)

activities_df['start_date'] = activities_df['start_date'].str[:10] # Reformat Start Dates
activities_df['month'] = activities_df['start_date'].str[5:7] # Reformat Start Dates

activities_df['type'] = activities_df['type'].replace('Soccer', 'Workout') # Change Soccer to Workout

running_df = activities_df[activities_df['type']=='Run'] # Split between Running and Workout
workout_df = activities_df[activities_df['type']=='Workout'] # Split between Running and Workout



# %% --------------------------------------------------------------------------
# Aggregate by Month
# -----------------------------------------------------------------------------
aggregated_running_df = running_df.groupby('month').agg({
    'moving_time': 'sum',
    'distance': 'sum'
}).reset_index()

aggregated_workout_df = workout_df.groupby('month').agg({
    'moving_time': 'sum',
    'distance': 'sum'
}).reset_index()



# %% --------------------------------------------------------------------------
# Plots
# -----------------------------------------------------------------------------
import matplotlib.pyplot as plt

agg_comb = aggregated_workout_df.merge(aggregated_running_df, on='month', how='outer')
agg_comb = agg_comb.fillna(0)
agg_comb = agg_comb.sort_values('month')
agg_comb['moving_time_x'] = agg_comb['moving_time_x']/60
agg_comb['moving_time_y'] = agg_comb['moving_time_y']/60

agg_comb['total_time'] = agg_comb['moving_time_x'] + agg_comb['moving_time_y']


month_dict = {
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September'
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

# %%
