"""
Downloading the Data from Strava

This module uses the Strava API to download the training data

"""

__date__ = "2023-10-09"
__author__ = "JamesMcGonigle"

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
# Downloading Data
# -----------------------------------------------------------------------------
class DownloadData():

    def __init__(self):

        # Define the API endpoint URL
        self.auth_url = "https://www.strava.com/oauth/token"

        # Refresh Token
        self.payload = {

            'client_id':client_id,
            'client_secret':client_secret,
            'refresh_token':refresh_token,
            'grant_type':'refresh_token',
            'f':'json'
            }
        
        self.request_page_num = 1
        self.all_activities = []
        self.header = {}
        self.activities_url = 'https://www.strava.com/api/v3/athlete/activities/' 


    def get_access_token(self):

        res = requests.post(self.auth_url, data=self.payload, verify=False)
        self.access_token = res.json()['access_token']
        self.header = {'Authorization': f'Bearer {self.access_token}'}

    def download_data(self):

        while True:
            param = {'per_page': 200, 'page': self.request_page_num}
            # initial request, where we request the first page of activities
            self.my_dataset = requests.get(self.activities_url, headers=self.header, params=param).json()

            # check the response to make sure it is not empty. If it is empty, that means there is no more data left. So if you have
            # 1000 activities, on the 6th request, where we request page 6, there would be no more data left, so we will break out of the loop

            if len(self.my_dataset) == 0:
                # print("breaking out of while loop because the response is zero, which means there must be no more activities")
                break

            # if the all_activities list is already populated, that means we want to add additional data to it via extend.
            if self.all_activities:
                # print("all_activities is populated")
                self.all_activities.extend(self.my_dataset)

            # if the all_activities is empty, this is the first time adding data so we just set it equal to my_dataset
            else:
                # print("all_activities is NOT populated")
                self.all_activities = self.my_dataset

            self.request_page_num += 1

    def json_save(self):

        file_path = rf"assets/total_activities.json"

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as self.json_file:
            json.dump(self.all_activities, self.json_file)

