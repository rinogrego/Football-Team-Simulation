"""
    File to collect new data from fbref
    
    There are 3 tables with following purposes:
    1. To scrape new league fixtures data (temporary table)
            Link Example: https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures
    2. To store the latest (scrapped) league fixtures data
            Link Example: https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures
    3. To store raw single match data which includes:
        a. General information regarding the match
            Link Example: https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures
                          https://fbref.com/en/matches/de515487/Liverpool-Bournemouth-August-27-2022-Premier-League
                          https://fbref.com/en/stathead/matchup/teams/822bd0ba/4ba7cbea/Liverpool-vs-Bournemouth-History
        b. Players' statistics from each team before the match started
            Link Example: https://fbref.com/en/squads/822bd0ba/Liverpool-Stats
        c. Link of the post-match informations
            Link Example: https://fbref.com/en/matches/de515487/Liverpool-Bournemouth-August-27-2022-Premier-League
        d. Post-match information
    
    Initialization Steps:
    1. Scrape the latest league fixtures data, save it as Table 1
    2. Find the soon-to-be played matches from Table 1, save/insert them as Table 3
    3. Insert into Table 3 the link of the match
            + The general info of the match from Table 1 & players' pre-match statistics
    
    Update Steps
    1. Scrape the latest league fixtures data
    2. Compare it with Table 2 if exists
    
    3. If the difference between Table 1 and Table 2 exists, 
            then there is a new match data. Go to Step 4. Else Step 7.
    4. Scrape the results of the matches saved in Table 3 and append the data 
            into Table 3
    5. Find the new soon-to-be played matches from Table 1, save/insert them as table 3
    6. Replace the Table 2 with Table 1
    
    7. If the difference between Table 1 and Table 2 is not exist,
            then do nothing
    
"""

import pandas as pd
import bs4
import re
import argparse
import json
import os
import time
from utils import get_html_document, scrape_team, scrape_league, \
            clean_team_stats_table, create_player_columns


DATA_DIR = "data"
# SAVE_DIR = "./raw/Premier League/2022-2023_Matches"
SAVE_DIR = "data/fbref/raw/Premier League/2022-2023_Matches"
TABLE_REF_PATH = "data/fbref/raw/Premier League/table_ref.csv"

LEAGUE_CODE = json.load(open(f"{DATA_DIR}/fbref/dictionaries.json"))["LEAGUE_CODE"]
TEAM_CODE = json.load(open(f"{DATA_DIR}/fbref/dictionaries.json"))["TEAM_CODE"]
TEAM_DISPLAY = json.load(open(f"{DATA_DIR}/fbref/dictionaries.json"))["TEAM_DISPLAY"]


def scrape_new_fixtures(league_fixtures_url: str) -> pd.DataFrame:
    """Get the new league fixtures information
    Parameters
    ----------
    league_fixtures_url : string
        The url of the league fixtures 
    Returns
    ----------
    pd.DataFrame
        pandas DataFrame for Table 1
    """
    # scrape via beautifulsoup4
    html_doc = get_html_document(league_fixtures_url)
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    
    # scrape directly the table via pandas
    pl_fixtures = pd.read_html(league_fixtures_url)
    df_table_1 = pd.DataFrame(pl_fixtures[0])
    df_table_1 = df_table_1.dropna(axis=0, how='all').reset_index().drop(columns=["index"])
    df_table_1 = df_table_1[df_table_1["Notes"] != "Match Postponed"]
    df_table_1["Match Report Link"] = 'empty'
    df_table_1["League"] = "Premier-League"
    
    past_matches = []
    temp_soup = soup.find_all('table')[0]

    for idx, row in df_table_1[df_table_1["Match Report"] == "Match Report"].iterrows():
        home = row["Home"]
        home = TEAM_DISPLAY[home]
        away = row["Away"]
        away = TEAM_DISPLAY[away]

        past_matches.append((home, away))

        for link in temp_soup.find_all('a', attrs={'href': re.compile("^/en/matches/")}):
            # ex: "/en/matches/073227b6/Merseyside-Derby-Everton-Liverpool-September-3-2022-Premier-League"
            last_link = link.get('href').split('/')[-1]

            # ex: "Merseyside-Derby-Everton-Liverpool-September-3-2022-Premier-League"
            if "Premier-League" not in last_link:
                continue

            last_link = last_link.split("-Derby-")[-1]
            # ex: "Everton-Liverpool-September-3-2022-Premier-League"
            
            if last_link.startswith(f"{home}-{away}"):
                df_table_1.loc[idx, "Match Report Link"] = link.get('href')
                break
    
    return df_table_1


def get_next_matches(df_next_matches: pd.DataFrame) -> pd.DataFrame:
    """Get new matches from newly scrapped league fixtures to be recorded/watched
    Parameters
    ----------
    df_next_matches : pd.DataFrame
        Pandas dataframe containing next fixtures to-be-played until the end
    Returns
    ----------
    pd.DataFrame
        Pandas DataFrame for next matches to be recorded not containing
        similar clubs in two different fixtures
    """
    clubs_recorded = []
    df_ = []

    for idx, row in df_next_matches.iterrows():
        club1 = row["Home"]
        club2 = row["Away"]
        
        if club1 in clubs_recorded or club2 in clubs_recorded:
            break

        df_.append(row)
        clubs_recorded.append(club1)
        clubs_recorded.append(club2)

    df_next_matches = pd.DataFrame(df_)
    
    return df_next_matches


def get_pre_match_info(df_next_matches: pd.DataFrame, save_dir=SAVE_DIR):
    """Get pre-match information regarding a match and then save it
    as .csv file. The information includes: the match's general information
    and the player's pre-match statistics.
    Parameters
    ----------
    match_url : string
        The head-to-head url of the match
    df_next_matches : pd.DataFrame
        Pandas DataFrame for next matches to be recorded not containing
        similar clubs in two different fixtures
    Returns
    ----------
    None
    """
    df_nm = df_next_matches.copy()

    for idx, row in df_nm.iterrows():
        home = TEAM_DISPLAY[row["Home"]]
        away = TEAM_DISPLAY[row["Away"]]
        date = row["Date"]
        filename = f"{SAVE_DIR}/{date}_{home}-vs-{away}.csv"
        
        # check if the .csv is already exists then don't scrap
        if os.path.exists(filename) == True:
            continue

        df_home, home_players = create_player_columns(TEAM_CODE[home], home)
        # sleep for 3 seconds to delay scraping just not too spam the requests to fbref
        time.sleep(3)
        df_away, away_players = create_player_columns(TEAM_CODE[away], away)

        # to prevent concat giving 2 rows instead of 1
        row_ = row.to_frame().T.reset_index().drop(columns=["index"])
        # increase the number of levels of the columns
        row_.columns = pd.MultiIndex.from_product([[""], [""], row_])
        row_.columns.names = ["Club", "Player", "Statistic"]

        df_ = pd.concat(
            [home_players, away_players], 
            axis=1,
        )
        df_.to_csv(filename)
        print(f"{home} vs {away} pre-match information. DataFrame shape: {df_.shape}")
        print(f"Saved to: {filename}")


def get_post_match_data_as_dict(
    match_url: str="/en/matches/de515487/Liverpool-Bournemouth-August-27-2022-Premier-League",
    home: str="Liverpool",
    away: str="Bournemouth"
) -> json:
    """For each newly appended matches in Table 3, append the 
    post-match information into it
    Parameters
    ----------
    match_url : str
        The url of the league fixtures 
    home : str
        The string indicating the home team
    away : str
        The string indicating the away team
    Returns
    ----------
    json
        JSON data consisted of players that played on the match with their minutes 
        and positions played
    """
    df_ = pd.read_html("https://fbref.com" + match_url)
    desired_column = ["Player", "Pos", "Age", "Min"]
    
    # initiating directories
    post_match_dict = {}
    post_match_dict[home] = {}
    post_match_dict[away] = {}

    # processing home team players
    home_players = df_[3].copy()
    home_players.columns = [col[1] for col in home_players.columns.to_flat_index()]
    
    next_is_sub = False
    for idx, row in home_players[desired_column].iloc[:-1].iterrows():
        if next_is_sub:
            post_match_dict[home][row["Player"] + " (Sub)"] = {}
            post_match_dict[home][row["Player"] + " (Sub)"]["Pos"] = row["Pos"]
            post_match_dict[home][row["Player"] + " (Sub)"]["Age"] = row["Age"]
            post_match_dict[home][row["Player"] + " (Sub)"]["Min"] = row["Min"]
            next_is_sub = False
            continue
            
        post_match_dict[home][row["Player"]] = {}
        post_match_dict[home][row["Player"]]["Pos"] = row["Pos"]
        post_match_dict[home][row["Player"]]["Age"] = row["Age"]
        post_match_dict[home][row["Player"]]["Min"] = row["Min"]
        if row["Min"] < 90:
            # fbref indicates substituted players either by string or minutes played
            # even though the player came on at 90+ min, the player being sent off
            # has minutes played displayed as 89 and not 90
            # so players that played the entire match were given 90 minutes otherwise
            # at max they are given 89
            next_is_sub = True

    # processing away team players
    away_players = df_[10].copy()
    away_players.columns = [col[1] for col in away_players.columns.to_flat_index()]
    
    next_is_sub = False
    for idx, row in away_players[desired_column].iloc[:-1].iterrows():
        if next_is_sub:
            post_match_dict[away][row["Player"] + " (Sub)"] = {}
            post_match_dict[away][row["Player"] + " (Sub)"]["Pos"] = row["Pos"]
            post_match_dict[away][row["Player"] + " (Sub)"]["Age"] = row["Age"]
            post_match_dict[away][row["Player"] + " (Sub)"]["Min"] = row["Min"]
            next_is_sub = False
            continue
        
        post_match_dict[away][row["Player"]] = {}
        post_match_dict[away][row["Player"]]["Pos"] = row["Pos"]
        post_match_dict[away][row["Player"]]["Age"] = row["Age"]
        post_match_dict[away][row["Player"]]["Min"] = row["Min"]
        if row["Min"] < 90:
            next_is_sub = True

    return post_match_dict


def collect():
    """Collect the new raw data and then update the database
    Parameters
    ----------
    None
    Returns
    ----------
    str
        to determine whether the collection process succeed or not
    """
    league_fixtures_url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
    TABLE_2_FILENAME = TABLE_REF_PATH
    
    try:
        # get reference/past fixtures table
        table_2 = pd.read_csv(
            TABLE_2_FILENAME,
            # header=[0, 1, 2],
            index_col=0
        )
        
    except:
        # if no table found then initialize table
        table_1 = scrape_new_fixtures(league_fixtures_url=league_fixtures_url)
        table_1.to_csv(TABLE_2_FILENAME)
        status = "New Table Fixture Initialized\nPlease run the script again to obtain pre-match information"
        return status

    table_1 = scrape_new_fixtures(league_fixtures_url=league_fixtures_url)
    
    ### Testing purpose
    # table_1 = pd.read_csv("table_1_test.csv")
    
    if (table_1["Match Report Link"] == table_2["Match Report Link"]).all() == False:
        # new table and old table is not the same
        # which means new result (probably) exists
        print("New match result exists\nStart Processing...")
        print("============================================================")
        cond = table_1["Match Report Link"] != table_2["Match Report Link"]
        df_new_finished_matches = table_1.loc[cond, :]
        
        print("Processing post-match information of previous matches")
        for idx, row in df_new_finished_matches.iterrows():
            match_report_link = row["Match Report Link"]
            home = TEAM_DISPLAY[row["Home"]]
            away = TEAM_DISPLAY[row["Away"]]
            date = row["Date"]

            post_match_dict = get_post_match_data_as_dict(match_report_link, home, away)

            with open(f"{SAVE_DIR}/{date}_{home}-vs-{away}.json", 'w') as fp:
                json.dump(post_match_dict, fp, indent=4)
            print(f"Saved to: {SAVE_DIR}/{date}_{home}-vs-{away}.json")
        
        # get next matches
        print("============================================================")
        print("Scraping future matches' information")
        print("------------------------------------------------------------")
        table_2 = table_1.copy()
        df_next_matches = table_2[table_2["Match Report"] != "Match Report"]
        df_next_matches = get_next_matches(df_next_matches)
        get_pre_match_info(df_next_matches=df_next_matches, save_dir=SAVE_DIR)
        print("------------------------------------------------------------")
        
        # save newly scrapped table as new reference for the future
        table_2.to_csv(TABLE_2_FILENAME)
        print("Fixture reference updated")
        print("============================================================")
        status = "Collection Success"
    else:
        status = "No New Data Found"
        
    return status


if __name__ == "__main__":
    print("Start Scraping for New Data...")
    status = collect()
    print(status)