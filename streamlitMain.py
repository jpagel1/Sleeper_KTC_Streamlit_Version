#JSP 2/25/23

import streamlit as st

import requests
#st.set_page_config(layout="wide")

import pandas as pd

#Import Sleeper Functions
import SleeperFunctions.sleeperfunctions as sleeperData

#Import Keep,Trade,Cut Functions
import KeepTradeCutFunctions.KTCfunctions as KTCdata

#Import sleeper leagure class
from UserLeagueClass.user_sleeperleague_class import sleeper_league

#session states
if 'load_league_button' not in st.session_state:
    st.session_state.datagrab_button = False

#st.write(st.session_state)

@st.cache_data
def load_data(sleeper_league_id):
    #Run Get All NFL Player Info Once A Month
    sleeperData.get_all_nfl_player_data()
    st.session_state.progress = 25

    #Remove Unneeded People from this Json if required that month
    sleeperData.remove_unneeded_nfl_players()
    st.session_state.progress = 50

    #Get KTC Cut Values Once A Day
    sleeper_ktc_include_picks = True
    sleeper_ktc_superflex = False
    KTCdata.initate_ktc_pull(sleeper_ktc_superflex,sleeper_ktc_include_picks)
    #Add the KTC Cut Values to the Player Data
    st.session_state.progress = 75
    
    KTCdata.add_KTC_values_to_player_data()
    userL = sleeper_league(sleeper_league_id)
    st.session_state.progress = 100

    return userL
    
#sleeper_league_id=917535899465388032

st.title("Justin's Fantasy Football App:football:")
sleeper_id_from_user = st.text_input('Sleeper League ID', '917535899465388032')
st.write('The data is typically shown like this: sleeper.app/leagues/123456789098765432')
st.write("")
    
#Load League button function
button_hit = st.button(label='Load In League Data', use_container_width=True, key = 'load_league_button')

if (button_hit):
    st.session_state.datagrab_button = True

st.write("")
st.write("")
st.write("")

if st.session_state.datagrab_button:

    userLObj = load_data(sleeper_id_from_user)
    if (userLObj.validLeagueID == False):
        st.write("Invalid League ID")
    else:
        #sst.progress(100, text="Loaded Sleeper Data")
        #Display User league name
        st.header(f"League Name: {userLObj.league_info.get_league_name()}")
        #print(userLObj.league_info.get_league_name())
        option = st.selectbox(
        'What league data do you want to explore today?',
        ('Teams Total KTC Value', 'Teams Average KTC Value', 
        'Teams Average Age',"Teams Search Rank","Teams Average Weight","Teams Average Height","Teams Position Count",
        "Teams Average Experience","Display League Rosters","Display Team College Map"))
        #df = pd.read_csv(csv_path)
        #print(df)
        df = pd.DataFrame(userLObj.league_data_calculated)
        #print(dftest)
        if (option == "Teams Total KTC Value"):
            st.write("Total KTC(Keep,Trade,Cut) Points")
            #Graph - ID Name - KTC By Position
            item = ["Total KTC","QB Total KTC","RB Total KTC","WR Total KTC","TE Total KTC"]
            for i in item:
                st.write(i)
                columns = ["Actual ID Name", i]
                df2 = df[columns].copy()
                chart_data = df2
                st.bar_chart(chart_data,x="Actual ID Name",y=i) 
                
        elif (option == "Teams Average KTC Value"):
            st.write("Age Information")
            #Graph - ID Name - KTC By Position
            item = ["Overall KTC Average","QB Ave KTC","RB Ave KTC","WR Ave KTC","TE Ave KTC"]
            for i in item:
                st.write(i)
                columns = ["Actual ID Name", i]
                df2 = df[columns].copy()
                chart_data = df2
                st.bar_chart(chart_data,x="Actual ID Name",y=i)

        elif (option == "Teams Search Rank"):
            st.write("Teams Search Rank")
            item = ["Total Search Rank","QB Search Rank","RB Search Rank","WR Search Rank","TE Search Rank"]
            for i in item:
                st.write(i)
                columns = ["Actual ID Name", i]
                df2 = df[columns].copy()
                chart_data = df2
                st.bar_chart(chart_data,x="Actual ID Name",y=i)
                
        elif (option == "Teams Average Weight"):
            st.write("Weight Information")
            #Graph - ID Name - KTC By Position
            item = ["Overall Average Weight","QB Average Weight","RB Average Weight","WR Average Weight","TE Average Weight"]
            for i in item:
                st.write(i)
                columns = ["Actual ID Name", i]
                df2 = df[columns].copy()
                chart_data = df2
                st.bar_chart(chart_data,x="Actual ID Name",y=i)
                
        elif (option == "Teams Average Height"):
            st.write("Height Information")
            #Graph - ID Name - KTC By Position
            item = ["Overall Average Height","QB Average Height","RB Average Height","WR Average Height","TE Average Height"]
            for i in item:
                st.write(i)
                columns = ["Actual ID Name", i]
                df2 = df[columns].copy()
                chart_data = df2
                st.bar_chart(chart_data,x="Actual ID Name",y=i)
                
        elif (option == "Teams Average Experience"):
            st.write("Average Experience Infomation")
            #Graph - ID Name - KTC By Position
            item = ["Overall Experience Average","QB Experience","RB Experience","WR Experience","TE Experience"]
            for i in item:
                st.write(i)
                columns = ["Actual ID Name", i]
                df2 = df[columns].copy()
                chart_data = df2
                st.bar_chart(chart_data,x="Actual ID Name",y=i)
            
        elif (option == "Teams Position Count"):
            st.write("Position Information")
            #Graph - ID Name - KTC By Position
            item = ["QB Count","RB Count","WR Count","TE Count"]
            for i in item:
                st.write(i)
                columns = ["Actual ID Name", i]
                df2 = df[columns].copy()
                chart_data = df2
                st.bar_chart(chart_data,x="Actual ID Name",y=i)

        elif (option == "Teams Average Age"):
            st.write("Age Information")
            #Graph - ID Name - KTC By Position
            item = ["Overall Average Age","QB Average Age","RB Average Age","WR Average Age","TE Average Age"]
            for i in item:
                st.write(i)
                columns = ["Actual ID Name", i]
                df2 = df[columns].copy()
                chart_data = df2
                st.bar_chart(chart_data,x="Actual ID Name",y=i)

        elif (option == "Display League Rosters"):
            #st.write("Display League Rosters")
            
            teamnames = userLObj.league_users.get_all_user_names()
            teamPD = pd.DataFrame(teamnames)
            #Get name of rosters
            #roster = userLObj.get_formatted_roster_with_data()
            option1 = st.selectbox(
            'What team do you want to explore today?',
            (teamPD))
            
            team_id = userLObj.league_users.get_user_ID_from_team_name(option1)
            #display roster data for QB
            roster_data = userLObj.get_formatted_roster_with_data(team_id,'QB')
            st.header("QB Roster")
            data = pd.DataFrame(roster_data).sort_values(by=['KTC'],ascending=False)
            st.table(data[['Name','Age','College','KTC']])
            roster_data = userLObj.get_formatted_roster_with_data(team_id,'RB')
            st.write("RB Roster")
            data = pd.DataFrame(roster_data).sort_values(by=['KTC'],ascending=False)
            st.table(data[['Name','Age','College','KTC']])
            roster_data = userLObj.get_formatted_roster_with_data(team_id,'WR')
            st.write("WR Roster")
            data = pd.DataFrame(roster_data).sort_values(by=['KTC'],ascending=False)
            st.table(data[['Name','Age','College','KTC']])
            roster_data = userLObj.get_formatted_roster_with_data(team_id,'TE')
            st.write("TE Roster")
            data = pd.DataFrame(roster_data).sort_values(by=['KTC'],ascending=False)
            st.table(data[['Name','Age','College','KTC']])
            
        
        elif (option == "Display Team College Map"):
            st.write("Work In Progress...")
            """
            teamnames = userLObj.league_users.get_all_user_names()
            teamPD = pd.DataFrame(teamnames)
            #Get name of rosters
            #roster = userLObj.get_formatted_roster_with_data()
            option1 = st.selectbox(
            'What team do you want to explore today?',
            (teamPD))
            
            team_id = userLObj.league_users.get_user_ID_from_team_name(option1)
            roster_data = userLObj.get_formatted_roster_with_data(team_id,'QB')
            #st.write(roster_data)
            st.header("QB Roster Colleges")
            dataF = pd.DataFrame(roster_data, columns=['Name','College','lat','lon'])
            st.table(dataF)
            st.map(dataF)
            
            roster_data = userLObj.get_formatted_roster_with_data(team_id,'RB')
            #st.write(roster_data)
            st.header("RB Roster Colleges")
            dataF = pd.DataFrame(roster_data, columns=['Name','College','lat','lon'])
            st.table(dataF)
            st.map(dataF)
            """
        
        
        else:
            None
            
