"""Class for the User League Info
The init is automatically called when creating a sleeper league instance
Function Summarys
    __Init__ - Loaded the Sleeper Data for the ID and stores it as class attributes
    get_league_name - Returns the League Name
    get_league_total_rosters - Returns the League Total Roster #
    get_league_settings - Returns the League Settings
    get_league_scoring_settings - Returns the League Settings
    get_league_roster_positions - Returns the League Roster Positions
    get_league_past_winner - Returns the Leagues latest winner ID number
    get_league_id - Returns the League ID
"""

import SleeperFunctions.sleeperfunctions as sleeperData

class user_league_info:
    """This will hold the users league info"""

    def __init__(self,sleeper_league_id):
        """Initialize the user league info"""
        #load sleeper_data
        leaguedataraw = sleeperData.load_sleeper_data_into_class(sleeper_league_id)
        if leaguedataraw is not None:
            self.__dict__ = leaguedataraw
            self.validLeagueID = True
        else:
            self.validLeagueID = False
    
    def get_league_name(self):
        """Returns the League Name"""
        return self.__dict__['name']

    def get_league_total_rosters(self):
        """Returns the League Total Roster #"""
        return self.__dict__['total_rosters']
    
    def get_league_settings(self):
        """Returns the League Settings"""
        return self.__dict__['settings']
    
    def get_league_scoring_settings(self):
        """Returns the League Scoring Settings"""
        return self.__dict__['scoring_settings']
    
    def get_league_roster_positions(self):
        """Returns the League Roster Positions"""
        return self.__dict__['roster_positions']
    
    def get_league_past_winner(self):
        """Returns the Leagues latest winner ID number"""
        temp = self.__dict__['metadata']
        return temp['latest_league_winner_roster_id']
    
    def get_league_id(self):
        """Returns the League ID"""
        return self.__dict__['league_id']