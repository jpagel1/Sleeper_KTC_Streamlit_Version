"""KeepTradeCut Functions
These functions are used to scrape Keep Trade Cut values add load them
    getKTCValues - Grabs Info and Player Data from KTC, return to caller
    initiate_KTC_pull = Initiates KTC pull, saves updated values once a day
    add_KTC_values_to_player_data - Adds KTC data to all NFL player data once a day  
"""

import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from os import path,remove


def getKTCValues(superFlex = False,includePicks = True):
    
    """Grabs Info and Player Data from KTC and returns a dictionary with the following info:
    Player Name
    Player Position
    Player Team
    Player Value
    """

    url = 'https://keeptradecut.com/dynasty-rankings?filters=QB|WR|RB|TE'
    if includePicks:
        url = url + '|RDP'
    if not superFlex:
        url = url + '&format=1'
    raw_html = requests.get(url)
    soupdata = BeautifulSoup(raw_html.content, "html.parser")

    #Prettify
    #print(soupdata.prettify())

    #The ID I need for the location I want is div[id=rankings-page-rankings]
    table = soupdata.find('div', attrs = {'id':"rankings-page-rankings"}) 

    #print(table.prettify())

    #Make List for Players
    player_list = []
    test = table.findAll('div', attrs = {"player-name"})

    player_data = table.find_all('div', attrs = {'onePlayer'})

    #print(player_data)

    for player in player_data:
        #Make Dict for player to put in player_list later on
        player_dict = {}

        #Get Player Name
        player_name = player.find('div', attrs = {'player-name'})
        #Get Data back as a list of one element?
        temp = player_name.select('a') 
        tempRemovePeriods= str.replace(temp[0].text,'.',"")
        tempRemoveSpaces = str.replace(tempRemovePeriods,' ','')
        tempRemoveapos = str.replace(tempRemoveSpaces,"'",'')
        tempRemovehyphen = str.replace(tempRemoveapos,"-",'')
        player_dict['Player Name'] = tempRemovehyphen.lower()

        #Get Player Team
        player_team = player.find('span', attrs = {'player-team'})
        player_dict['Player Team'] = player_team.text

        #Get Player Value On KTC
        player_value = player.find('div', attrs = {'value'})
        temp = player_value.select('p')
        player_dict['Player Value'] = temp[0].text

        #Get Player Position
        player_pos = player.find('div', attrs = {'position-team'})
        temp = player_pos.select('p')
        temp = (temp[0].text)[:2]
        player_dict['Player Position'] = temp

        #Get Player Age - In order to get draft pick ages I would have to pull from elsewhere
        temp = player_pos.select('p')
        try:
            age = (temp[1].text)[:2]
        except:
            age = None
        player_dict['Player Age'] = age

        player_list.append(player_dict)
        
    return player_list

def initate_ktc_pull(superFlex = False,includePicks = True):

    base_path = 'KTC Values/'
    date_str = datetime.now().strftime('%Y%m%d')
    csv_path = base_path + 'ktc_' + date_str + '.csv'

    #check if values already downloaded today
    if not path.exists(csv_path):

        print("Updating KTC Values")
        #Get Data
        player_db = getKTCValues(superFlex, includePicks)
        player_pandas = pd.DataFrame.from_dict(player_db)
        player_pandas.to_csv(csv_path, index=False)

        #Delete Yesterdays Values
        #Unless I want to do historical KTC values, then I could save them elsewhere (possibly database?)
        
        #for now delete yesterdays values
        
    else:
        print("KTC Values Up To Date")

def add_KTC_values_to_player_data():
    #Look at path
    #base_path = 'C:/Users/jpage/Documents/Python Work/Fantasy Football/KTC Sleeper App/KTC Values/'
    base_path = 'KTC Values/'
    date_str_ktc = datetime.now().strftime('%Y%m%d')
    csv_path = base_path + 'ktc_' + date_str_ktc + '.csv'

    """Function to add KTC values to the NFL Player data. Use once a day"""
    date_str = datetime.now().strftime('%Y%m%d')
    date_str_m = datetime.now().strftime('%Y%m')
    full_path_existing = 'SleeperJsonData/NFL_player_info_limited_'+date_str_m+'.json'
    full_path_new = 'SleeperJsonData/NFL_player_info_ktc_'+date_str+'.json'

    #Check if KTC_Player_Data is Created Already
    if not path.exists(full_path_new):

        #Load In Player Info
        with open(full_path_existing, 'r') as player:
            players = json.load(player)

        df = pd.read_csv (csv_path, usecols=['Player Name','Player Value'])
        new = df['Player Name'].str.strip()

        for item,values in players.items():

            #Only update players who are Active
            if (values['active']):
                #For Some Reason Some Players Names Are not combined so first add a 'name' key in the dictonary
                combined_name = f" {values['first_name'].title()} {values['last_name'].title()}"
                values['Name']=values['search_full_name']
                #combined_name.strip().lower()

                #Search for name in df and if found, update ktc
                i = df[df['Player Name'].str.contains(values['Name'])]
                #print(i)
                if (not i.empty):
                    for player_n in i.values:
                        values['KTC'] = player_n[1]
                else: 
                    #Update all other players that don't have a KTC with a KTC of 0
                    values['KTC']=0

        # Serializing json object
        json_object = json.dumps(players, indent=4)

        # Writing to a file to be used with other scripts
        with open(full_path_new, 'w') as player:
            player.write(json_object)

        #Remove the Limited NFL Player Database
        remove(full_path_existing)
        #Remove yesterdays KTC database if it exists
        datetoday = datetime.now()
        dattemp = datetoday- timedelta(days=1)
        dateyesterday = dattemp.strftime('%Y%m%d')
        full_path_old_ktc = 'SleeperJsonData/NFL_player_info_ktc_'+dateyesterday+'.json'

        if path.exists(full_path_old_ktc):
            #full_path_old_ktc = 'SleeperJsonData/NFL_player_info_ktc_'+dateyesterday+'.json'
            remove(full_path_old_ktc)


