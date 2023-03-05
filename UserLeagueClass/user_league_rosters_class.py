"""Class for the User League Users
The init is automatically called when creating a sleeper league instance
Function Summarys
    __Init__ - Loaded the Sleeper League Roster Data for the ID and stores it as class attributes
    get_roster_data - This will return a dict of the complete roster data for the user_ID
    get_player_info_raw - Returns player info for entire roster of that user_id
    get_average_weight - Returns average weight for entire roster of that user_id
        - Position - None, QB, WR, RB, TE
    get_average_experience - Returns average experience for entire roster of that user_id
        - Position - None, QB, WR, RB, TE
    get_average_height - Returns average height for entire roster of that user_id
        - Position - None, QB, WR, RB, TE
    get_average_age - Returns average age for entire roster of that user_id
        - Position - None, QB, WR, RB, TE
    get_roster_KTC_sum - Get the entire KTC sum for roster for the User_ID
    get_player_ktc - Get the KTC for the player
        - Player - either player_id or real_name
        - IDFormat = True/False, if true use full_name
    get_player_position - Get the position for the player
        - Player - either player_id or real_name
        - IDFormat = True/False, if true use full_name
    get_roster - Returns list roster position of the user ID
        - Position - None, QB, WR, RB, TE
        - formatID - True/False. If True, return raw play_id, otherwise full_name
    get_total_KTC - Returns total KTC for entire roster of that user_id
        - Position - None, QB, WR, RB, TE
    get_average_KTC - Returns average KTC for entire roster of that user_id
        - Position - None, QB, WR, RB, TE
    load_roster_ktc_sum - Loads the KTC sum into the class attributes
    load_player_data - Loads the player data into the class attributes
    load_roster_data_with_real_names - add attributes for taxi, starter, and all roster names
    
"""

import SleeperFunctions.sleeperfunctions as sleeperData
import json
import pandas as pd
from os import path,remove
from datetime import datetime

class user_league_rosters:
    """This will hold the users league users rosters"""

    def __init__(self,sleeper_league_id):
        """Initialize the user league info users"""

        #load sleeper_data
        leaguedataraw = sleeperData.load_sleeper_league_rosters_into_class(sleeper_league_id)
        #for item in leaguedataraw:
        #    print (item)
        #Load all data into attr under owner_id as top level
        for item in leaguedataraw:
            team = item['owner_id']
            setattr(self,team,item)
        
        #Load In Roster Real Names instead of IDs
        self.load_roster_data_with_real_names()
        #Load In Player Data from Recently Pulled NFL Data with KTC included
        self.load_player_data()
        #Load Roster KTC sum to the class
        #self.load_roster_ktc_sum()

    def get_roster_data(self,user_id):
        """This will return a dict of the complete roster data for the user_ID"""

        temp = {}
        for item,value in self.__dict__.items():
            try:
                if (value['owner_id'] == user_id):
                    temp[value['owner_id']]=value
                    return temp
            except:
                    return temp
    
    def get_player_info_raw(self,user_id):
        """Returns player info for entire roster of that user_id"""

        for item,value in self.__dict__.items():
            try:
                if (value['owner_id'] == user_id):
                    return (value['player_info_raw'])
            except:
                    return None
            
    def get_average_weight(self,user_id,position=None):
        """Returns average experience for entire roster of that user_id"""

        total_players = 0
        total_weight = 0
        for item,value in self.__dict__.items():
            if (value['owner_id'] == user_id):
                for i in (value['player_info_raw']):
                    #print(i)
                    for k,v in i.items():
                        #print(v['age'])
                        checkVal = v['years_exp']
                        if (checkVal and ((position == None) or (v['position'] == position))):
                            total_weight += int(v['weight'])
                            total_players +=1
        try:
            average_weight = total_weight/total_players
        except ZeroDivisionError:
            average_weight = 0
        return round(average_weight,2)
              
    def get_average_experience(self,user_id,position=None):
        """Returns average experience for entire roster of that user_id"""

        total_players = 0
        total_exp = 0
        for item,value in self.__dict__.items():
            if (value['owner_id'] == user_id):
                for i in (value['player_info_raw']):
                    #print(i)
                    for k,v in i.items():
                        #print(v['age'])
                        checkVal = v['years_exp']
                        if (checkVal and ((position == None) or (v['position'] == position))):
                            total_exp += int(v['years_exp'])
                            total_players +=1
        try:
            average_exp = total_exp/total_players
        except ZeroDivisionError:
            average_exp = 0
        return round(average_exp,2)
    
    def get_average_height(self,user_id,position=None):
        """Returns average height for entire roster of that user_id"""
        total_players = 0
        total_height = 0
        for item,value in self.__dict__.items():
            if (value['owner_id'] == user_id):
                for i in (value['player_info_raw']):
                    #print(i)
                    for k,v in i.items():
                        checkVal = v['height']
                        if (checkVal and ((position == None) or (v['position'] == position))):
                            total_height += int(v['height'])
                            total_players +=1

        try:
            average_height = total_height/total_players
        except ZeroDivisionError:
            average_height = 0
        return round(average_height,2)
    
    def get_average_age(self,user_id,position=None):
        """Returns average age for entire roster of that user_id"""
        total_players = 0
        total_age = 0
        for item,value in self.__dict__.items():
            if (value['owner_id'] == user_id):
                for i in (value['player_info_raw']):
                    #print(i)
                    for k,v in i.items():
                        checkVal = v['age']
                        #print(checkVal)
                        if (checkVal and ((position == None) or (v['position'] == position))):
                            total_age += int(v['age'])
                            total_players +=1
        #print(total_age)
        #print(total_players)
        try:
            average_age = total_age/total_players
        except ZeroDivisionError:
            average_age = 0
        return round(average_age,2)

    def get_roster_KTC_sum(self,user_id):
        """Get the entire KTC sum for roster for the User_ID"""

        for key,value in self.__dict__.items():
            #print(f"{value}\n")
            #print(f"{i} - {v}")
            try:
                if (value['owner_id'] == user_id):
                    #print(v['ktc_sum'])
                    return value['ktc_sum']
            except:
                return ("No Match")

    def get_roster(self,user_id,position=None,formatID=False):
        """Returns list roster position of the user ID"""
        #if number format is on then return id, otherwise actual names
        templist = []
        for item,value in self.__dict__.items():
            if (value['owner_id'] == user_id):
                for i in (value['player_info_raw']):
                    #print(i)
                    for k,v in i.items():
                        if ((position == None) or (v['position'] == position)):
                            if (formatID == True):
                                templist.append(v['player_id'])
                            else:
                                templist.append(v['full_name'])
        return templist

    def get_player_ktc(self,player,IDFormat=True):
        """Returns total KTC for entire roster of that user_id"""
        KTCValue=0
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['KTC']
                    else:
                        if (v['player_id'] == player):
                            return v['KTC']
        return KTCValue
    
    def get_player_age(self,player,IDFormat=True):
        """Returns age of the player"""
        playerage = 0
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['age']
                    else:
                        if (v['player_id'] == player):
                            return v['age']
        return playerage

    def get_player_position(self,player,IDFormat=True):
        """Returns position of player"""
        position = None
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['position']
                    else:
                        if (v['player_id'] == player):
                            return v['position']
        return None
    
    def get_player_weight(self,player,IDFormat=True):
        """Returns weight of player"""
        weight = 0
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['weight']
                    else:
                        if (v['player_id'] == player):
                            return v['weight']
        return weight

    def get_player_height(self,player,IDFormat=True):
        """Returns height of player"""
        height = 0
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['height']
                    else:
                        if (v['player_id'] == player):
                            return v['height']
        return height
    
    def get_player_years_exp(self,player,IDFormat=True):
        """Returns years experience of player"""
        yearsExp = 0
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['years_exp']
                    else:
                        if (v['player_id'] == player):
                            return v['years_exp']
        return yearsExp
    
    def get_player_search_rank(self,player,IDFormat=True):
        """Returns search rank of player"""
        rank = 0
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['search_rank']
                    else:
                        if (v['player_id'] == player):
                            return v['search_rank']
        return rank
    
    def get_player_high_school(self,player,IDFormat=True):
        """Returns high school of player"""
        school = None
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['high_school']
                    else:
                        if (v['player_id'] == player):
                            return v['high_school']
        return school

    def get_player_team(self,player,IDFormat=True):
        """Returns team of player"""
        team = None
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['team']
                    else:
                        if (v['player_id'] == player):
                            return v['team']
        return team
    
    def get_player_college(self,player,IDFormat=True):
        """Returns college of player"""
        college = None
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['college']
                    else:
                        if (v['player_id'] == player):
                            return v['college']
        return college
    
    def get_player_depth_chart_order(self,player,IDFormat=True):
        """Returns depth chart order of player"""
        order = None
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['depth_chart_order']
                    else:
                        if (v['player_id'] == player):
                            return v['depth_chart_order']
        return order
    
    def get_player_depth_chart_position(self,player,IDFormat=True):
        """Returns depth chart position of player"""
        pos = None
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['depth_chart_position']
                    else:
                        if (v['player_id'] == player):
                            return v['depth_chart_position']
        return pos

    def get_player_jersey_number(self,player,IDFormat=True):
        """Returns jerseynum of player"""
        num = None
        for item,value in self.__dict__.items():
            for i in (value['player_info_raw']):
                for k,v in i.items():
                    if (IDFormat == True):
                        if (v['full_name'] == player):
                            return v['number']
                    else:
                        if (v['player_id'] == player):
                            return v['number']
        return num

    def get_total_KTC(self,user_id,position=None):
        """Returns total KTC for entire roster of that user_id"""
        total_KTC = 0
        for item,value in self.__dict__.items():
            if (value['owner_id'] == user_id):
                for i in (value['player_info_raw']):
                    for k,v in i.items():
                        if ((position == None) or (v['position'] == position)):
                            total_KTC += int(v['KTC'])
        return round(total_KTC,2)
    
    def get_total_search_rank(self,user_id,position=None):
        """Returns total search rank for entire roster of that user_id"""
        searchrank = 0
        for item,value in self.__dict__.items():
            if (value['owner_id'] == user_id):
                for i in (value['player_info_raw']):
                    for k,v in i.items():
                        if ((position == None) or (v['position'] == position)):
                            if (int(v['search_rank'])==9999999):
                                searchrank=0
                            else:
                                searchrank += int(v['search_rank'])
        return round(searchrank,2)

    def get_average_KTC(self,user_id,position=None):
        """Returns average KTC for entire roster of that user_id"""
        playercount = 0
        total_KTC = 0
        for item,value in self.__dict__.items():
            if (value['owner_id'] == user_id):
                for i in (value['player_info_raw']):
                    for k,v in i.items():
                        if ((position == None) or (v['position'] == position)):
                            total_KTC += int(v['KTC'])
                        playercount+=1
        try:
            ktcAvg = total_KTC/playercount
        except ZeroDivisionError:
            ktcAvg = 0
        return round(ktcAvg,2)     
            
    def load_roster_ktc_sum(self):
        """Loads the Sum of the KTC values of the roster"""

        for item,value in self.__dict__.items():
            ktcSum = 0
            #print("match")
            for i in (value['player_info_raw']):
                for name,value_info in i.items():
                    #Searching through the player_info_raw library
                    try:
                        ktcSum += int(value_info['KTC'])
                    except:
                        ktcSum +=0
            #Also add KTC Sum as a value in dict
            value['ktc_sum']=ktcSum

    
    def load_player_data(self):
        """This will add the player data including KTC to the top level league roster object"""

        #Load in new ktc value player data
        date_str = datetime.now().strftime('%Y%m%d')
        full_path_new = 'SleeperJsonData/NFL_player_info_ktc_'+date_str+'.json'

        if (path.exists(full_path_new)):
            #Only perform this function if that path exists meaning the class was built correctly

            #Load In Player Info
            with open(full_path_new, 'r') as player:
                player_data_raw = json.load(player)

            player_data_team = []
            #Loop Through the roster data
            for key,values in self.__dict__.items():
                #print(f"\n\nRoster for {values['roster_id']}")
                player_data = []
                #Loop through the player real names
                for name in values['players']:
                    #print(name)
                    player_data_dict = {}
                    for id,data in player_data_raw.items():
                        if (str(id).strip() == str(name).strip()):
                            #print(f"{id} - {name}")
                            #Found matching name and id in player_raw_data
                            #Now load that crap in here. might want function to get player real name from ID
                            player_data_dict[data['Name']]=data
                            #player_data_dict[data['full_name']]=data
                    #If dict is empty, dont add it
                    if (player_data_dict):
                        player_data.append(player_data_dict)
                player_data_team.append(player_data)
                values['player_info_raw'] = player_data
            
    def load_roster_data_with_real_names(self):
        """This function will update the roster names's with actual names"""
        date_str = datetime.now().strftime('%Y%m%d')
        full_path_new = 'SleeperJsonData/NFL_player_info_ktc_'+date_str+'.json'
        #print(full_path_new)
        #Check if file exists
        if (path.exists(full_path_new)):
            with open(full_path_new, 'r') as player:
                players = json.load(player)

            #First Combine First and Last name - saw some issues with using full_name
            playerid_list = {}

            for item,values in players.items():
                #print (f"{item} - {values['first_name'].title()} {values['last_name'].title()}\n")
                id = values['player_id']
                combined_name = f" {values['first_name'].title()} {values['last_name'].title()}"
                playerid_list[id]=combined_name

            #Add new dict for player_real_names
            #Add new dict for starters_real_names
            #add new dict for taxi_real_names

            for key,values in self.__dict__.items():
                player_real_names = []
                starters_real_names = []
                taxi_real_names = []

                #print(f"{key} - {values}")
                for k,v in values.items():
                    #print(k)
                    if (k == 'players'):
                        try:
                            for i in v:
                                for ids,playname in playerid_list.items():
                                    #print(playname)
                                    if (ids==i):
                                        player_real_names.append(playname.strip())
                        except:
                            player_real_names = None
                    if (k == 'taxi'):
                        try:
                            for i in v:
                                for ids,playname in playerid_list.items():
                                    #print(playname)
                                    if (ids==i):
                                        taxi_real_names.append(playname.strip())
                        except:
                            taxi_real_names = None
                    if (k == 'starters'):
                        try:
                            for i in v:
                                for ids,playname in playerid_list.items():
                                    #print(playname)
                                    if (ids==i):
                                        starters_real_names.append(playname.strip())
                        except:
                            starters_real_names = None
                values['player_real_names'] = player_real_names
                values['starters_real_names'] = starters_real_names
                values['taxi_real_names'] = taxi_real_names            
