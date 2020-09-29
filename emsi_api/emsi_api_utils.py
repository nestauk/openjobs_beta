import requests
import pandas as pd
import pickle
#from ast import literal_eval
"""
29/09/2020
author: Stef Garasto

This script downloads the list of skills from EMSI using their API.

See https://skills.emsidata.com/ and  https://api.emsidata.com/apis/skills

To use, replace the path to the credentials file. This file needs to be a csv
file with three columns: client_id, secret and scope:

client_id	the client id that you received during API account setup
client_secret	the client secret that you received during API account setup
scope	use the string 'emsi_open' to access the skills ('emsiauth' might be a more general one)

"""
credentials_file = '/Users/stefgarasto/Local-Data/sensitive-data/emsi_api_credentials.csv'

credentials = pd.read_csv(credentials_file).T.to_dict()[0]

def obtain_oauth2():
    url = "https://auth.emsicloud.com/connect/token"

    payload = "client_id={}&client_secret={}&grant_type=client_credentials&scope={}".format(
    credentials['client_id'],
    credentials['secret'],
    credentials['scope']
    )
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json()

#oauth2 = obtain_oauth2()

def obtain_skills_list(oauth2=None):
    if not oauth2:
        oauth2 = obtain_oauth2()
    url = "https://emsiservices.com/skills/versions/latest/skills"
    #v1 "https://skills.emsicloud.com/versions/latest/skills"
    headers = {'authorization': 'Bearer {}'.format(oauth2['access_token'])}
    response = requests.request("GET", url, headers=headers)
    return response.json()


def get_and_save_skills_list(emsi_path=None,oauth2=None):
    if not emsi_path:
        # change path to whereever you want it to be
        emsi_path = '/Users/stefgarasto/Google Drive/Documents/data/ESCO/Emsi_skills_library_201912.pkl'

    emsi_skills = obtain_skills_list(oauth2)
    with open(emsi_path, 'wb') as f:
        pickle.dump(emsi_skills,f)
    return emsi_skills

def load_skills_list(emsi_path=None):
    if not emsi_path:
        # change path to whereever you want it to be
        emsi_path = '/Users/stefgarasto/Google Drive/Documents/data/ESCO/Emsi_skills_library_201912.pkl'

    with open(emsi_path, 'rb') as f:
        emsi_skills = pickle.load(f)

    return emsi_skills
#if __name__ == '__main__':
#    obtain_oauth2()
