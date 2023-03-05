"""Class for the User League Users
The init is automatically called when creating a sleeper league instance
Function Summarys
    __Init__ - Loaded the Sleeper League User Data for the ID and stores it as class attributes
    get_user_id_and_name - This will return a list of dictonaries matching the user ID and displayname
    get_user_data_from_user_id - Get all of the User Data for the User_ID
    get_all_user_ids - Return list of all user IDs
    get_all_user_names - Return list of all user names
    get_user_name_from_user_id - Get the User Name for the User_ID
    get_team_name_from_user_id - Get the Team Name from user ID
"""
import SleeperFunctions.sleeperfunctions as sleeperData

class user_league_users:
    """This will hold the users league users info"""

    def __init__(self,sleeper_league_id):
        """Initialize the user league info users"""
        
        #load sleeper_data
        leaguedataraw = sleeperData.load_sleeper_league_users_into_class(sleeper_league_id)

        #Load all data into attr
        for item in leaguedataraw:
            team = item['user_id']
            setattr(self,team,item)
    
    def get_user_id_and_name(self):
        """This will return a list of dictonaries matching the user ID and displayname"""

        user_id_and_name = []
        for key,value in self.__dict__.items():
            temp_dict = {}
            temp_dict['user_id']= value['user_id']
            temp_dict['display_name']= value['display_name']
            user_id_and_name.append(temp_dict)
        return user_id_and_name
    
    def get_user_data_from_user_id(self,user_id):
        """Get all of the User Data for the User_ID"""

        for key,value in self.__dict__.items():
            try:
                if (value['user_id'] == user_id):
                    return value
            except:
                return ("No Match")
                
    def get_all_user_ids(self):
        """Return list of all user IDs"""

        temp = []
        for key,value in self.__dict__.items():
            temp.append(value['user_id'])
        return temp

    def get_all_user_names(self):
        """Return list of all user names"""

        temp = []
        for key,value in self.__dict__.items():
            temp.append(value['display_name'])
        return temp
    
    def get_user_name_from_user_id(self,user_id):
        """Get the User Name for the User_ID"""

        for key,value in self.__dict__.items():
            try:
                if (value['user_id'] == user_id):
                    return value['display_name']
            except:
                return ("No Match")

    def get_team_name_from_user_id(self,user_id):
        """Get the Team Name from user ID"""

        for key,value in self.__dict__.items():
            #print(f"{key} - {value}")
            if (value['user_id'] == user_id):
                for i,vs in (value['metadata']).items():
                    #print(f"{i}-{vs}")
                    if (i=='team_name'):
                        return vs
        return "No Team Name"

    def get_user_ID_from_team_name(self,teamname):
        """Get the user id from team name"""

        for key,value in self.__dict__.items():
            #print(f"{key} - {value}")
            if (value['display_name'] == teamname):
                return(key)
                """
                for i,vs in (value['metadata']).items():
                    #print(f"{i}-{vs}")
                    if (i=='user_id'):
                        return vs
                """
        return "No Team Name"
        