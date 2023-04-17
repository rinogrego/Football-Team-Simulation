"""
    File to collect new data from fbref
    
    There are 3 kinds of .csv (say, Table) files with following purposes:
    1. To scrape new league fixtures data (temporary table)
            Link Example: https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures
    2. To store the latest (scrapped) league fixtures data
    3. To store raw single match data (as one .csv row) which includes players' pre-match statistics from each team before the match started
            Link Example: https://fbref.com/en/squads/822bd0ba/Liverpool-Stats
                          https://fbref.com/en/squads/4ba7cbea/Bournemouth-Stats
            
    Post-match information is saved as .json file with the same name as its Table 3 counterparts (that saves the match' players' pre-match info).
        Link Example: https://fbref.com/en/matches/de515487/Liverpool-Bournemouth-August-27-2022-Premier-League
    
    Initialization Steps:
    1. Scrape the latest league fixtures data, this is Table 1. The retrieved data including:
        - url of the match for detailed information
        - general information of the match
    2. Find the soon-to-be played matches from Table 1, then retrieve players' pre-match statistics right before the match. Save it into Table 3, a one row .csv.
    3. Save Table 1 for future scrape reference. For future scraping this becomes Table 2.
    
    Update Steps
    1. Scrape the latest league fixtures data. New (temporary) Table 1
    2. Get stored league fixtures reference table (Table 2) then compare it
    
    3. If the difference between Table 1 and Table 2 exists, 
            then there is a new match data. Go to Step 4. Else Step 7.
    4. Scrape the post-match information of the matches saved in Table 3 and then save the data as .json with similar filename
    5. Find the new soon-to-be played matches from Table 1, then retrieve players' pre-match statistics right before the match. Save it into Table 3, a one row .csv.
    6. Update table reference by saving Table 1 for future scrape reference. For future scraping this becomes Table 2.
    
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
# SAVE_DIR = "data/fbref/raw/Premier-League/2022-2023_Matches"
# TABLE_REF_DIR = "data/fbref/raw"

LEAGUE_CODE = json.load(open(f"{DATA_DIR}/fbref/dictionaries.json"))["LEAGUE_CODE"]
LEAGUE_LINK = json.load(open(f"{DATA_DIR}/fbref/dictionaries.json", mode='rb'))["LEAGUE_LINK"]
TEAM_CODE = json.load(open(f"{DATA_DIR}/fbref/dictionaries.json", mode='rb'))["TEAM_CODE"]
TEAM_DISPLAY = json.load(open(f"{DATA_DIR}/fbref/dictionaries.json", mode='rb'))["TEAM_DISPLAY"]
# print(list(TEAM_DISPLAY.keys()))

parser = argparse.ArgumentParser(description='Script to automatically scrape pre-and-post-match information')
parser.add_argument('--league', type=str, help='Specify the league to scrape.')
args = parser.parse_args()
if args.league is not None:
    LEAGUE = args.league
else:
    LEAGUE = "All"

def scrape_new_fixtures(league: str = "Premier-League") -> pd.DataFrame:
    """Get the new league fixtures information
    Parameters
    ----------
    league : string
        The league whose fixtures info gonna be scraped
    Returns
    ----------
    pd.DataFrame
        pandas DataFrame for league fixtures reference table
    """
    league_fixtures_url = LEAGUE_LINK[league]
    
    # scrape via beautifulsoup4
    html_doc = get_html_document(league_fixtures_url)
    soup = bs4.BeautifulSoup(html_doc, 'html.parser')
    
    # scrape directly the table via pandas
    pl_fixtures = pd.read_html(league_fixtures_url)
    df_table_1 = pd.DataFrame(pl_fixtures[0])
    df_table_1 = df_table_1.dropna(axis=0, how='all').reset_index().drop(columns=["index"])
    df_table_1 = df_table_1[df_table_1["Notes"] != "Match Postponed"]
    df_table_1["Match Report Link"] = 'empty'
    df_table_1["League"] = league
    
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
            if league not in last_link:
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


def get_pre_match_info(df_next_matches: pd.DataFrame, save_dir: str, league_code: int, re_scrape=False):
    """Get pre-match information regarding a match and then save it
    as .csv file. The information includes: the match's general information
    and the player's pre-match statistics.
    Parameters
    ----------
    df_next_matches : pd.DataFrame
        Pandas DataFrame for next matches to be recorded not containing
        similar clubs in two different fixtures
    save_dir : string
        Directory to save the scrapped pre-match info
    league_code : int
        Code of the league whose fixtures info gonna be scraped
    re_scrape : bool
        Indicates whether doing a re-scraping for the already-scrapped match or not
    Returns
    ----------
    None
    """
    df_nm = df_next_matches.copy()

    for idx, row in df_nm.iterrows():
        home = TEAM_DISPLAY[row["Home"]]
        away = TEAM_DISPLAY[row["Away"]]
        date = row["Date"]
        filename = f"{save_dir}/{date}_{home}-vs-{away}.csv"
        
        if re_scrape:
            # check if the .csv is already exists then don't scrape
            if os.path.exists(filename) == True:
                continue

        df_home, home_players = create_player_columns(TEAM_CODE[home], home, league_code=league_code)
        # sleep for 3 seconds to delay scraping just not too spam the requests to fbref
        time.sleep(3)
        df_away, away_players = create_player_columns(TEAM_CODE[away], away, league_code=league_code)
        # sleep for 3 seconds to delay scraping just not too spam the requests to fbref
        time.sleep(3)

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
) -> dict:
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
    dict
        Python dictionary data about post-match info consisted of players that played on the match 
        with their minutes and positions played
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


def collect(league="Serie-A"):
    """Collect the new raw data and then update the database
    Parameters
    ----------
    league: str
        Indicates the league to scrape
    Returns
    ----------
    str
        to determine whether the collection process succeed or not
    """
    SAVE_DIR = f"{DATA_DIR}/fbref/raw/{league}/2022-2023_Matches"
    TABLE_REF_PATH = f"{DATA_DIR}/fbref/raw/{league}/table_ref.csv"
    league_code = LEAGUE_CODE[league]
    
    try:
        # get reference/past fixtures table
        table_2 = pd.read_csv(
            TABLE_REF_PATH,
            # header=[0, 1, 2],
            index_col=0
        )
        
    except:
        # if no table found then initialize table
        table_1 = scrape_new_fixtures(league=league)
        table_1.to_csv(TABLE_REF_PATH)
        
        print("============================================================")
        print("Scraping future matches' information")
        print("------------------------------------------------------------")
        df_next_matches = table_1[table_1["Match Report"] != "Match Report"]
        df_next_matches = get_next_matches(df_next_matches)
        get_pre_match_info(df_next_matches=df_next_matches, save_dir=SAVE_DIR, league_code=league_code)
        print("============================================================")
        status = "New Table Fixture Initialized"
        return status

    table_1 = scrape_new_fixtures(league=league)
    # import numpy as np
    # for idx, (row_t1, row_t2) in enumerate(zip(table_1.to_numpy(), table_2.to_numpy())):
    #     print(np.array_equal(row_t1, row_t2))
    #     break
    #     if np.array_equal(row_t1, row_t2):
    #         print()
    #         print("INDEX", idx)
    #         print(row_t1)
    #         print(row_t2)
    #         print()
    
    ### Testing purpose
    # table_1 = pd.read_csv("table_1_test.csv")
    
    if (table_1["Match Report Link"] == table_2["Match Report Link"]).all() == False:
        # new table and old table is not the same
        # which means new result (probably) exists
        print("New match result exists!\nStart Processing...")
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
        get_pre_match_info(df_next_matches=df_next_matches, save_dir=SAVE_DIR, league_code=league_code)
        print("------------------------------------------------------------")
        
        # save newly scrapped table as new reference for the future
        table_2.to_csv(TABLE_REF_PATH)
        print("Fixture reference updated")
        print("============================================================")
        status = "Collection Success"
    else:
        status = "No New Data Found"
        
    return status


if __name__ == "__main__":
    LEAGUE_LIST = ["Premier-League", "Serie-A", "La-Liga", "Ligue-1", "Bundesliga"]
    print("Start Scraping for New Data...")
    if LEAGUE == "All":
        for league in LEAGUE_LIST:
            print("")
            print("        LEAGUE:", league.upper())
            print("")
            status = collect(league=league)
            print(f"{league}: {status}")
        status = "\nCollecting All League Data Success"
    else:
        assert LEAGUE in LEAGUE_LIST
        print("")
        print("        LEAGUE:", LEAGUE.upper())
        print("")
        status = collect(league=LEAGUE)
        status = f"{LEAGUE.upper()}: {status}"
    print(status)