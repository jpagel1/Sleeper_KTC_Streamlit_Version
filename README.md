<pre>
# Sleeper_KTC_Streamlit_Version
Streamlit App to display sleeper fantasy football stats and KTC values based on League ID

Background

1. The User Enters in a valid Sleeper League ID into the form on the streamlit webapp.
</pre>
![image](https://user-images.githubusercontent.com/31528908/222980977-f04af900-497e-40b2-a219-83afd8f47899.png)
<pre>
2. Once the User hits "Load In League Data" the following happens in the background. 

  a. A SleeperData function call is done once a month (to limit api calls since it is a large file) 
  and saves the raw data as a json in the SleeperJsonData folder.
  
  b. A SleeperData function call is then done once a month to the data gathered above to filter out 
  all non active players, invalid positions, etc.. to limit the file size for later use.
  
  c. A KeepTradeCut function call is then done to scrape the KTC website and get up to date values for 
  players. This is performed once daily and the values are saved into a csv inside of the KTCValues folder. 
  
  d. A KeepTradeCut function call is then done that sorts through the filtered nfl player data and adds 
  in the KTC values into the player info. This is done once a day.

3. Now that all of the background data should be available, the following occurs automatically. 

  a. A SleeperLeague object is created. The following is added to the object. 
      
      1. A user_league_info object which automaticaly performed sleeper api call to get league info 
      and loads the data into attributes. 
      
      2. A user_league_rosters object which does the same as above but for league rosters.
          
          a. The rosters come with just ID identifiers that match with the large raw nfl player json 
          grabbed earlier. The following is added to the league roster info:
                - player_real_names, starters_real_names, taxi_real_names
                - For each individual roster, we load in all nfl data for that player info the roster 
                object. This lets it be easily accessible later on.
      
      3. A user_league_users object which does the same as above but for league users. 
  
  b. Now that all of the league data is loaded into our object.
      
      1. We call the SleeperLeague method to load league stats. and store it into self.league_data_calculated.
      
4. Now we have all of league information easily accessible in our SleeperLeague object.

  userLeague = SleeperLeague(*users sleeper league ID*)
  
  a. Examples:
      1. userLeague.user_league_info.get_league_name() - gets league name
      2. userLeague.user_league_rosters.get_player_info_raw(user_ID) -  gets all nfl player info for 
      entire roster of that user_ID
      3. userLeague.user_league_users.get_all_user_ids() - returns a list of all user ids in the league
      
  b. There are many many functions that I have created that I am not using in the streamlit version of the app. 
  Hoping to implement more later on with historical stats. 
  
5. The Streamlit Main dropdowns are using data calculated from the SleeperLeagues objects attribute self.league_data_calculated. 
Examples of a Few Options
</pre>
![image](https://user-images.githubusercontent.com/31528908/222982213-da3810f5-49c6-4315-992f-c66ad57442e0.png)
![image](https://user-images.githubusercontent.com/31528908/222982228-0383a05d-e27e-4361-a658-e58a966519e2.png)
![image](https://user-images.githubusercontent.com/31528908/222982347-2ec53d77-9042-4dbd-b8af-6dbc55c21192.png)

<pre>

Enjoy!
</pre>
