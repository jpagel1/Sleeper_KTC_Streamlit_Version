"""Use this to get all the players in the NFL through sleeper API. Going to Use Once a Month"""

# Importing
import requests
import json
from datetime import datetime
from os import path
import streamlit as st

def remove_unneeded_nfl_players():
    """Function to get remove unneeded NFL Player data from sleeper and save as a json object. Use once a month"""
    date_str = datetime.now().strftime('%Y%m')
    full_path = 'SleeperJsonData/NFL_player_info_limited_'+date_str+'.json'
    full_path_existing = 'SleeperJsonData/NFL_player_info_'+date_str+'.json'

    #check if values already downloaded this month
    if not path.exists(full_path):
        #Load In Player Info
        with open(full_path_existing, 'r') as player:
            players = json.load(player)

        initialcount=0
        for item1 in players:
            initialcount=initialcount+1

        active_players = {}
        for key,value in players.items():

            #Take Player if Position is QB,RB,TE,WR and Player is Active
            #check if player is active
            validPosition = False
            poslist = ['QB','WR','TE','RB']
            if (value['position'] in poslist):
                validPosition = True

            if (value['active'] and validPosition):
                active_players[key] = value

        finalcount=0
        for item in active_players:
            finalcount=finalcount+1

        removedcount = finalcount - initialcount
        print(f"Successfully Removed {removedcount} players from database")

        # Serializing json object
        json_object = json.dumps(active_players, indent=4)

        with open(full_path, 'w') as player:
                player.write(json_object)

    else:
        print("Players Already Removed")


def get_all_nfl_player_data():
    """Function to get all NFL Player data from sleeper and save as a json object. Use once a month"""
    date_str = datetime.now().strftime('%Y%m')
    full_path = 'SleeperJsonData/NFL_player_info_'+date_str+'.json'
    #print(full_path)
    #print(path.exists(full_path))
    
    #check if values already downloaded this month
    if not path.exists(full_path):
        print("Pulling NFL Player Data")
        st.write("Pulling NFL Player Data")

        # Get all the players/player IDS
        response = requests.get(f'https://api.sleeper.app/v1/players/nfl')
        player_info = response.json() 

        # Serializing json object
        json_object = json.dumps(player_info, indent=4)
        # Writing to a file to be used with other scripts

        with open(full_path, 'w') as player:
            player.write(json_object)
    else:
        print("NFL Database Up To Date")
        st.write("NFL Database Up To Date")
    st.write("")
    

def load_sleeper_data_into_class(sleeper_league_id):
    """Get League Info from Sleeper to create the class"""
    print("Pulling Sleeper League Info Data to create the class")
    # Get league info using the league ID above
    response = requests.get(f'https://api.sleeper.app/v1/league/{sleeper_league_id}')
    league_info = response.json()
    return league_info

def load_sleeper_league_users_into_class(sleeper_league_id):
    print("Pulling Sleeper League Users Data to create the class")
    # Get all of the users in the league
    response = requests.get(f'https://api.sleeper.app/v1/league/{sleeper_league_id}/users')
    league_users = response.json()
    #for item in league_users:
    #    print(f"{item}\n")
    return league_users

def load_sleeper_league_rosters_into_class(sleeper_league_id):
    print("Pulling Sleeper League Users Rosters to create the class")

    # Get all of the users rosters in the league
    response = requests.get(f'https://api.sleeper.app/v1/league/{sleeper_league_id}/rosters')
    league_rosters = response.json()
    #for item in league_rosters:
    #    print(f"{item}\n")
    return league_rosters



###These Functions Might Be Obsolute now loading into classes for each

def get_sleeper_league_info(sleeper_league_id):
    print("Pulling Sleeper League Info Data")

    """Get League Info from Sleeper and Write to a Json File for Active Session"""
    # Get league info using the league ID above
    response = requests.get(f'https://api.sleeper.app/v1/league/{sleeper_league_id}')
    league_info = response.json()

    json_object = json.dumps(league_info, indent=4)

    # Writing to a file to be used with other scripts
    with open('SleeperJsonData/league_info.json', 'w') as player:
        player.write(json_object)

def get_sleeper_league_users(sleeper_league_id):
    print("Pulling Sleeper League Users Data")

    """Get League Users from Sleeper and Write to a Json file for Active Session"""
    # Get all of the users in the league
    response = requests.get(f'https://api.sleeper.app/v1/league/{sleeper_league_id}/users')
    league_users = response.json()

    json_object = json.dumps(league_users, indent=4)

    # Writing to a file to be used with other scripts
    with open('SleeperJsonData/league_users.json', 'w') as player:
        player.write(json_object)

def get_sleeper_league_rosters(sleeper_league_id):
    print("Pulling Sleeper League Roster Data")

    """Get League Rosters from Sleeper and Write to a Json file for Active Session"""
    # Get all rosters in the league, this is where max points for is stored (seems like it gets rid of the max points for value when the season is restarted)
    response = requests.get(f'https://api.sleeper.app/v1/league/{sleeper_league_id}/rosters')
    league_rosters = response.json()

    # Serializing json object
    json_object = json.dumps(league_rosters, indent=4)

    # Writing to a file to be used with other scripts
    with open('SleeperJsonData/league_rosters.json', 'w') as player:
        player.write(json_object)


