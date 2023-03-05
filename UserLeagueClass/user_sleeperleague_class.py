#Import Sleeper Functions
import SleeperFunctions.sleeperfunctions as sleeperData

#Import Keep,Trade,Cut Functions
import KeepTradeCutFunctions.KTCfunctions as KTCdata
import pandas as pd
from UserLeagueClass.user_league_info_class import user_league_info
from UserLeagueClass.user_league_users_class import user_league_users
from UserLeagueClass.user_league_rosters_class import user_league_rosters

#location lat/long
import LocationFunctions.LocationFunctions as Locate 

from os import path,remove
from datetime import datetime,timedelta  

#Build Master Class for Entire League
class sleeper_league():
    """This class combines the league info, league users, and league rosters object data"""

    def __init__(self,sleeper_league_id = None):
        self.dataready = False
        if (sleeper_league_id != None):
            """Initiates league info, league rosters, league users objects"""
            self.league_info = user_league_info(sleeper_league_id)
            if (self.league_info.validLeagueID == True):
                self.league_rosters = user_league_rosters(sleeper_league_id)
                self.league_users = user_league_users(sleeper_league_id)
                """
                for i,v in self.league_rosters.__dict__.items():
                    print (f"{i}-{v}")
                """
                #Calculate data we want for the league
                self.league_data_calculated = self.load_league_stats()
                #self.save_league_stats_to_csv()
                self.validLeagueID = True
            else:
                self.validLeagueID = False
                       
    def get_league_stats(self):
        return self.league_data_calculated

    def load_league_stats(self):
        """This loads the league stats into the instance of the object"""
        
        #league_id = self.league_info.get_league_id()
        #Build dataframe to save to csv
        dataforleague = []
        
        #Get league IDs
        league_ids = self.league_users.get_all_user_ids()
        for item in league_ids:
            team_id = str(item)
            #Get real name of user to display
            actual_id_name = self.league_users.get_user_name_from_user_id(team_id)
            actual_team_name = self.league_users.get_team_name_from_user_id(team_id)
            #print(team_id)
            #Show Average Age Functions
            avgAgeTotal = self.league_rosters.get_average_age(team_id)
            dataforteam = {}
            
            avgAgeQB = self.league_rosters.get_average_age(team_id,'QB')
            avgAgeRB = self.league_rosters.get_average_age(team_id,'RB')
            avgAgeWR = self.league_rosters.get_average_age(team_id,'WR')
            avgAgeTE = self.league_rosters.get_average_age(team_id,'TE')

            #Average Experience Functions
            avgExpTotal = self.league_rosters.get_average_experience(team_id)
            avgExpQB = self.league_rosters.get_average_experience(team_id,'QB')
            avgExpRB = self.league_rosters.get_average_experience(team_id,'RB') 
            avgExpWR = self.league_rosters.get_average_experience(team_id,'WR')
            avgExpTE = self.league_rosters.get_average_experience(team_id,'TE')

            #Average Weight Functions
            avgWeightTotal = self.league_rosters.get_average_weight(team_id)
            avgWeightQB = self.league_rosters.get_average_weight(team_id,'QB')
            avgWeightRB = self.league_rosters.get_average_weight(team_id,'RB')
            avgWeightWR = self.league_rosters.get_average_weight(team_id,'WR')
            avgWeightTE = self.league_rosters.get_average_weight(team_id,'TE')

            #Average Height Functions
            avgHeightTotal = self.league_rosters.get_average_height(team_id)
            avgHeightQB = self.league_rosters.get_average_height(team_id,'QB')
            avgHeightRB = self.league_rosters.get_average_height(team_id,'RB')
            avgHeightWR = self.league_rosters.get_average_height(team_id,'WR')
            avgHeightTE = self.league_rosters.get_average_height(team_id,'TE')

            #Total KTC Functions
            KTCTotal = self.league_rosters.get_total_KTC(team_id)
            ktcTotalQB = self.league_rosters.get_total_KTC(team_id,'QB')
            ktcTotalRB = self.league_rosters.get_total_KTC(team_id,'RB')
            ktcTotalWR = self.league_rosters.get_total_KTC(team_id,'WR')
            ktcTotalTE = self.league_rosters.get_total_KTC(team_id,'TE')

            #Ave KTC Functions
            KTCTotalAve = self.league_rosters.get_average_KTC(team_id)
            ktcAveQB = self.league_rosters.get_average_KTC(team_id,'QB')
            ktcAveRB = self.league_rosters.get_average_KTC(team_id,'RB')
            ktcAveWR = self.league_rosters.get_average_KTC(team_id,'WR')
            ktcAveTE = self.league_rosters.get_average_KTC(team_id,'TE')

            #Roster Functions
            #full_roster = self.league_rosters.get_roster(team_id,None,False)
            QB_roster = self.league_rosters.get_roster(team_id,'QB',False)
            RB_roster = self.league_rosters.get_roster(team_id,'RB',False)
            WR_roster = self.league_rosters.get_roster(team_id,'WR',False)
            TE_roster = self.league_rosters.get_roster(team_id,'TE',False)
            
            #Total Search Rank
            TotalSearchRank = self.league_rosters.get_total_search_rank(team_id)
            SearchRankQB = self.league_rosters.get_total_search_rank(team_id,'QB')
            SearchRankRB = self.league_rosters.get_total_search_rank(team_id,'RB')
            SearchRankWR = self.league_rosters.get_total_search_rank(team_id,'WR')
            SearchRankTE = self.league_rosters.get_total_search_rank(team_id,'TE')
            
            #Get counts of roster
            QBCount = len(QB_roster)
            RBCount = len(RB_roster)
            WRCount = len(WR_roster)
            TECount = len(TE_roster)
            
            #Load Data into Dict, then append it into data list to save to csv later on
            dataforteam = {}
            dataforteam['Team ID'] = team_id
            dataforteam['Actual ID Name'] = actual_id_name
            dataforteam['Actual Team Name'] = actual_team_name
        
            #Load Rosters Data into class
            dataforteam['Total Search Rank'] = TotalSearchRank
            dataforteam['QB Search Rank'] = SearchRankQB
            dataforteam['RB Search Rank'] = SearchRankRB
            dataforteam['WR Search Rank'] = SearchRankWR
            dataforteam['TE Search Rank'] = SearchRankTE

            #Load search rank into class
            dataforteam['QB Count'] = QBCount
            dataforteam['RB Count'] = RBCount
            dataforteam['WR Count'] = WRCount
            dataforteam['TE Count'] = TECount

            #Age Data
            dataforteam['Overall Average Age'] = avgAgeTotal
            dataforteam['QB Average Age'] = avgAgeQB
            dataforteam['RB Average Age'] = avgAgeRB
            dataforteam['WR Average Age'] = avgAgeWR
            dataforteam['TE Average Age'] = avgAgeTE

            #Exp Data
            dataforteam['Overall Experience Average'] = avgExpTotal
            dataforteam['QB Experience'] = avgExpQB
            dataforteam['RB Experience'] = avgExpRB
            dataforteam['WR Experience'] = avgExpWR
            dataforteam['TE Experience'] = avgExpTE

            #Weight Data
            dataforteam['Overall Average Weight'] = avgWeightTotal
            dataforteam['QB Average Weight'] = avgWeightQB
            dataforteam['RB Average Weight'] = avgWeightRB
            dataforteam['WR Average Weight'] = avgWeightWR
            dataforteam['TE Average Weight'] = avgWeightTE

            #Height Data
            dataforteam['Overall Average Height'] = avgHeightTotal
            dataforteam['QB Average Height'] = avgHeightQB
            dataforteam['RB Average Height'] = avgHeightRB
            dataforteam['WR Average Height'] = avgHeightWR
            dataforteam['TE Average Height'] = avgHeightTE
            
            #Total KTC Data
            dataforteam['Total KTC'] = KTCTotal
            dataforteam['QB Total KTC'] = ktcTotalQB
            dataforteam['RB Total KTC'] = ktcTotalRB
            dataforteam['WR Total KTC'] = ktcTotalWR
            dataforteam['TE Total KTC'] = ktcTotalTE

            #Total KTC Data
            dataforteam['Overall KTC Average'] = KTCTotalAve
            dataforteam['QB Ave KTC'] = ktcAveQB
            dataforteam['RB Ave KTC'] = ktcAveRB
            dataforteam['WR Ave KTC'] = ktcAveWR
            dataforteam['TE Ave KTC'] = ktcAveTE

            dataforleague.append(dataforteam)
            
        return dataforleague


    def save_league_stats_to_csv(self):
        """This just saves all league stats to a csv"""
        dataforleague = self.league_data_calculated
        #Save to CSV for League
        #Look at path
        base_path = 'FinalData/'
        date_str = datetime.now().strftime('%Y%m%d')
        sleeperlID = str(self.league_info.get_league_id())
        csv_path = base_path + date_str +'_' + sleeperlID + '.csv'

        #Get Data
        #check if values already downloaded today
        if not path.exists(csv_path):
            print("Saving League Values")
            player_pandas = pd.DataFrame.from_dict(dataforleague)
            player_pandas.to_csv(csv_path, index=False)

        else:
            print("File Already Created")
            
    
    def get_formatted_roster_with_data(self,user_id = None,position=None):
        """Gets the roster formatted with QB,RB,WR,and TE in order. Include Position, Age, and KTC value"""
        dataforleague = []
        
        #Get league IDs
        league_ids = self.league_users.get_all_user_ids()
        for item in league_ids:
            team_id = str(item)
            if (user_id == team_id):
                """Found Matching Team ID/User ID"""
                #print(self.league_rosters.get_player_info_raw('866361936198135808'))
                
                #Roster Functions
                #full_roster = self.league_rosters.get_roster(team_id,None,False)
                QB_roster = self.league_rosters.get_roster(team_id,'QB',False)
                RB_roster = self.league_rosters.get_roster(team_id,'RB',False)
                WR_roster = self.league_rosters.get_roster(team_id,'WR',False)
                TE_roster = self.league_rosters.get_roster(team_id,'TE',False)
                
                #Now Build Dictonary for player_data_formatted
                player_data_formatted_list = []
                if (position == 'QB') or (position == None):
                    for qb in QB_roster:
                        player_data = {}
                        player_data['Name'] = qb
                        player_data['Age'] = self.league_rosters.get_player_age(qb)
                        player_data['Position'] = self.league_rosters.get_player_position(qb)
                        college = self.league_rosters.get_player_college(qb)
                        player_data['College'] = college
                        """
                        college_find = college +' university'
                        #Get lat of college
                        tempList = Locate.getlatlong(college_find)
                        player_data['lat'] = tempList[0]
                        player_data['lon'] = tempList[1]
                        """
                        player_data['KTC'] = self.league_rosters.get_player_ktc(qb)
                        player_data_formatted_list.append(player_data)
                if (position == 'RB') or (position == None):
                    for rb in RB_roster:
                        player_data = {}
                        player_data['Name'] = rb
                        player_data['Age'] = self.league_rosters.get_player_age(rb)
                        player_data['Position'] = self.league_rosters.get_player_position(rb)
                        college = self.league_rosters.get_player_college(rb)
                        player_data['College'] = college
                        """
                        college_find = college +" university"
                        #Get lat of college
                        tempList = Locate.getlatlong(college_find)
                        player_data['lat'] = tempList[0]
                        player_data['lon'] = tempList[1]
                        """
                        player_data['KTC'] = self.league_rosters.get_player_ktc(rb)
                        player_data_formatted_list.append(player_data)
                if (position == 'WR') or (position == None):
                    for wr in WR_roster:
                        player_data = {}
                        player_data['Name'] = wr
                        player_data['Age'] = self.league_rosters.get_player_age(wr)
                        player_data['Position'] = self.league_rosters.get_player_position(wr)
                        college = self.league_rosters.get_player_college(wr)
                        player_data['College'] = college
                        """
                        college_find = college +" university"
                        #Get lat of college
                        tempList = Locate.getlatlong(college_find)
                        player_data['lat'] = tempList[0]
                        player_data['lon'] = tempList[1]
                        """
                        player_data['KTC'] = self.league_rosters.get_player_ktc(wr)
                        player_data_formatted_list.append(player_data)
                if (position == 'TE') or (position == None):
                    for te in TE_roster:
                        player_data = {}
                        player_data['Name'] = te
                        player_data['Age'] = self.league_rosters.get_player_age(te)
                        player_data['Position'] = self.league_rosters.get_player_position(te)
                        college = self.league_rosters.get_player_college(te)
                        player_data['College'] = college
                        """
                        print(college)
                        college_find = college +" university"
                        #Get lat of college
                        tempList = Locate.getlatlong(college_find)
                        player_data['lat'] = tempList[0]
                        player_data['lon'] = tempList[1]
                        """
                        player_data['KTC'] = self.league_rosters.get_player_ktc(te)
                        player_data_formatted_list.append(player_data)
                
                return(player_data_formatted_list)

#Testing
"""
#Run Get All NFL Player Info Once A Month
sleeperData.get_all_nfl_player_data()


#Remove Unneeded People from this Json if required that month
sleeperData.remove_unneeded_nfl_players()


#Get KTC Cut Values Once A Day
sleeper_ktc_include_picks = True
sleeper_ktc_superflex = False
KTCdata.initate_ktc_pull(sleeper_ktc_superflex,sleeper_ktc_include_picks)
#Add the KTC Cut Values to the Player Data

KTCdata.add_KTC_values_to_player_data()
leaguetest = sleeper_league('917535899465388032')

league_stats = leaguetest.get_league_stats()
leaguetest.save_league_stats_to_csv()

roster = leaguetest.get_formatted_roster_with_data('866361936198135808')
rt = pd.DataFrame(roster)
print(rt)    
es = pd.DataFrame(league_stats)
#print(es)
"""