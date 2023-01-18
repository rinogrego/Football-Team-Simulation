import numpy as np
import pandas as pd
import bs4
import requests
import re
import matplotlib.pyplot as plt


def get_html_document(url):
  # request for HTML document of given url
  response = requests.get(url)
  # response will be provided in JSON format
  return response.text


def scrape_team(team_id, team_name):
  team_url = f'https://fbref.com/en/squads/{team_id}/{team_name}-Stats'
  html_doc = get_html_document(team_url)
  soup = bs4.BeautifulSoup(html_doc, 'html.parser')
  return soup


def scrape_league(league_id, league_name):
  league_url = f'https://fbref.com/en/comps/{league_id}/{league_name}-Stats'
  html_doc = get_html_document(league_url)
  soup = bs4.BeautifulSoup(html_doc, 'html.parser')

  lg_table_soup = soup.find_all('table')[0]

  return lg_table_soup


def clean_team_stats_table(raw_table):
  # remove the multi-index
  # ex: column name ('Playing Time', 'MP') becomes ('Playing Time - MP')
  for col in raw_table.columns:
    if 'unnamed' in col[0].lower():
      continue
    new_colname = col[0] + ' - ' + col[1]

    # column reassignment is used instead of rename because rename changes 
    # all the columns with the desired name
    raw_table[('', new_colname)] = raw_table[col]
    raw_table.drop(columns=[col], inplace=True, axis=1)

  # change the column structure to make it just 1 level
  raw_table = raw_table.droplevel(level=0, axis=1)

  # drop unneeded columns & rows
  raw_table = raw_table.drop(["Matches"], axis=1)
  raw_table = raw_table[
      (raw_table["Player"] != "Squad Total") &
      (raw_table["Player"] != "Opponent Total")
  ]

  # Change NaN values to 0
  raw_table = raw_table.fillna(0)
  
  # Convert string values to numeric
  for col in raw_table.columns:
    raw_table[col] = pd.to_numeric(
        raw_table[col], 
        errors='ignore',
    )
  
  return raw_table


def create_player_columns(team_id="822bd0ba", team_name="Liverpool"):
  # get html doc of the team
  team_soup = scrape_team(team_id, team_name)

  # get html table of playing time
  stats_list = [
    "standard",
    "keeper",
    "keeper_adv",
    "shooting",
    "passing",
    "passing_types",
    "gca",
    "defense",
    "possession",
    "playing_time",
    "misc",
  ]
  stats_table_list = []

  for stats in stats_list:
    # get individual table of each statistic category
    table_soup = team_soup.find('table', attrs={'id': f"stats_{stats}_9"})
    table_raw = pd.read_html(str(table_soup))[0]
    table_clean = clean_team_stats_table(table_raw)

    # rename the columns to mark from where the columns was obtained
    table_clean = table_clean.set_index("Player")
    for col in table_clean.columns:
      table_clean.rename(columns={col: f"{stats} - {col}"}, inplace=True)
    table_clean = table_clean.reset_index("Player")

    stats_table_list.append(table_clean)

  # join/merge all the tables
  df_players = stats_table_list[0]
  for stats_table in stats_table_list[1:]:
    # merge
    df_players = df_players.merge(stats_table.set_index("Player"), on="Player", how="outer",)

  # # convert into 1 row
  # df_players_one_row = df_players.set_index("Player").unstack().to_frame().T
  # # swap axis level of the columns
  # df_players_one_row = df_players_one_row.swaplevel(0, axis=1)
  # # sort the columns based on the player's name
  # df_players_one_row = df_players_one_row.sort_values("Player", axis=1)

  # # add new column name to determine the club the players belong to
  # # the club information is placed as new column level
  # df_players_one_row.columns = pd.MultiIndex.from_product([[team_name], df_players_one_row])


  #### Convert into 1 row
  # df_players_one_row = df_players.unstack().to_frame().T
  # df_players_one_row = df_players_one_row.swaplevel(1, axis=1)
  # df_players_one_row = df_players_one_row.sort_values("Player", axis=1)
  # df_players_one_row.columns.names = ["Club", "Player", "Statistic"]

  df_players_one_row = df_players.set_index("Player")
  df_players_one_row.columns = pd.MultiIndex.from_product([["Fulham"], df_players_one_row.columns])
  # pakai column name Club -- Player - Statistics
  df_players_one_row = df_players_one_row.unstack().to_frame().T
  df_players_one_row = df_players_one_row.swaplevel(1, axis=1).sort_values("Player", axis=1)
  df_players_one_row.columns.names = ["Club", "Player", "Statistic"]
  ###


  #### reduce the column levels further
  ## this thing makes the process from ~2 secs to ~2 mins 30 secs
  ## so i commented this because that's too long
  # for col in df_players.columns:
  #   if 'unnamed' in col[0].lower():
  #     continue
  #   new_colname = col[0] + ' - ' + col[1]

  #   # column reassignment is used instead of rename because rename changes 
  #   # df_players.rename(columns={col[1]: new_colname}, inplace=True)

  #   # all the columns with the desired name
  #   df_players[('', new_colname)] = df_players[col]
  #   df_players.drop(columns=[col], inplace=True, axis=1)

  # # change the column structure to make it just 1 level
  # df_players = df_players.droplevel(level=0, axis=1)
  ####

  return df_players, df_players_one_row