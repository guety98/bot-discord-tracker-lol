import requests
import os
import manage_csv
import average_rank
import re

# Initialisation

riot_token = os.environ['RIOT_TOKEN']


# Fonctions

def api_get_summoner_infos(username, server) -> str:
  #username = urllib.parse.quote(username)
  if server == 'EUW':
    summoner_info_url_api = "https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(
      riot_token)
  elif server == 'JP':
    summoner_info_url_api = "https://jp1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(
      riot_token)
  elif server == 'KR':
    summoner_info_url_api = "https://kr.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(
      riot_token)
  elif server == 'EUN':
    summoner_info_url_api = "https://eun1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(
      riot_token)
  elif server == 'LA1':
    summoner_info_url_api = "https://la1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(
      riot_token)
  elif server == 'LA2':
    summoner_info_url_api = "https://la2.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(
      riot_token)
  elif server == 'NA1' or server == 'NA':
    #summoner_info_url_api = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(riot_token)
    summoner_info_url_api = "https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-name/{}?api_key={}".format(username, str(riot_token))
  elif server == 'TR':
    summoner_info_url_api = "https://tr1.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(
      riot_token)
  elif server == 'RU':
    summoner_info_url_api = "https://ru.api.riotgames.com/tft/summoner/v1/summoners/by-name/" + username + "?api_key=" + str(
      riot_token)
  else:
    return None

  response = requests.get(summoner_info_url_api)
  
  if response.status_code != 200:
    print(f"{response.status_code} pour api_get_summoner_infos ({username},{server})\n")
    return None
  else:
    summoner_infos = response.json()
    return summoner_infos


def api_get_current_rank(userId, server) -> str:
  #userId = urllib.parse.quote(userId)
  if server == 'EUW':
    curent_rank_url_api = "https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(
      riot_token)
  elif server == 'JP':
    curent_rank_url_api = "https://jp1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(
      riot_token)
  elif server == 'KR':
    curent_rank_url_api = "https://kr.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(
      riot_token)
  elif server == 'EUN':
    curent_rank_url_api = "https://eun1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(
      riot_token)
  elif server == 'LA1':
    curent_rank_url_api = "https://la1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(
      riot_token)
  elif server == 'LA2':
    curent_rank_url_api = "https://la2.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(
      riot_token)
  elif server == 'NA1' or server == 'NA':
    #curent_rank_url_api = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(riot_token)
    curent_rank_url_api = "https://na1.api.riotgames.com/tft/league/v1/entries/by-summoner/{}?api_key={}".format(userId, str(riot_token))
  elif server == 'TR':
    curent_rank_url_api = "https://tr1.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(
      riot_token)
  elif server == 'RU':
    curent_rank_url_api = "https://ru.api.riotgames.com/tft/league/v1/entries/by-summoner/" + userId + "?api_key=" + str(
      riot_token)
  else:
    return None

  response = requests.get(curent_rank_url_api)
  if response.status_code != 200:
    print(f"{response.status_code} pour api_get_current_rank ({userId},{server})\n")
    return None
  else:
    summoner_rank = response.json()
    return summoner_rank


def api_get_history(puuid, server, number_games) -> str:
  if server == 'EUW' or server == 'EUN' or server == 'TR' or server == 'RU':
    last_games_history_url_api = "https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/" + str(
      puuid) + "/ids?start=0&count=" + str(number_games) + "&api_key=" + str(riot_token)
  elif server == 'JP' or server == 'KR':
    last_games_history_url_api = "https://asia.api.riotgames.com/tft/match/v1/matches/by-puuid/" + str(
      puuid) + "/ids?start=0&count=" + str(number_games) + "&api_key=" + str(riot_token)
  elif server == 'LA1' or server == 'LA2' or server == 'NA1' or server == 'NA':
    last_games_history_url_api = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/" + str(
      puuid) + "/ids?start=0&count=" + str(number_games) + "&api_key=" + str(riot_token)
  else:
    return None

  response = requests.get(last_games_history_url_api)
  if response.status_code != 200:
    print(f"{response.status_code} pour api_get_history ({puuid},{server})\n")
    return None
  else:
    summoner_history = response.json()
    return summoner_history


def api_get_last_game(last_matchId, server, puuid) -> str:
  last_game_url_api = ""
  if server == 'EUW' or server == 'EUN' or server == 'TR' or server == 'RU':
    last_game_url_api = "https://europe.api.riotgames.com/tft/match/v1/matches/" + last_matchId + "?api_key=" + str(
      riot_token)
  elif server == 'JP' or server == 'KR':
    last_game_url_api = "https://asia.api.riotgames.com/tft/match/v1/matches/" + last_matchId + "?api_key=" + str(
      riot_token)
  elif server == 'LA1' or server == 'LA2' or server == 'NA1' or server == 'NA':
    last_game_url_api = "https://americas.api.riotgames.com/tft/match/v1/matches/" + last_matchId + "?api_key=" + str(
      riot_token)
  response = requests.get(last_game_url_api)
  if response.status_code != 200:
    print(f"{response.status_code} pour api_get_last_game ({last_matchId},{puuid},{server})\n")
    return None
  else:
    summoner_last_game = response.json()
    return summoner_last_game

  response = requests.get(last_game_url_api)
  if response.status_code != 200:
    print(f"{response.status_code} pour api_get_history ({last_matchId},{server},{puuid})\n")
    return None
  else :    
    last_game = response.json()
    participants = last_game.get("metadata").get("participants")
    infos = last_game.get("info").get("participants")
    compo = []
    for i, participant in enumerate(participants):
      if participant == puuid:
        top = infos[i].get("placement")
        units = infos[i].get("units")
        for unit in units:
          character = unit.get("character_id")
          champion = character.split('_')[1]
          tier = unit.get("tier")
          compo += [champion, tier]
    info = [top, compo]
    return info


def run_api(username, server):
  summoner_infos = api_get_summoner_infos(username, server)
  if summoner_infos:
    userId = summoner_infos['id'][0:]
    puuid = summoner_infos['puuid'][0:]
    if userId:
      summoner_rank = api_get_current_rank(userId, server)
      if summoner_rank:
        tier = summoner_rank[0]['tier']
        rank = summoner_rank[0]['rank']
        leaguePoints = summoner_rank[0]['leaguePoints']
        summoner_complete_rank = tier + ' ' + rank + ' ' + str(
          leaguePoints) + ' LP'
        total_games = int(summoner_rank[0]['wins']) + int(summoner_rank[0]['losses'])
        winrate = round((int(summoner_rank[0]['wins']) / total_games) * 100, 1)
        if tier:
          summoner_history = api_get_history(puuid, server, 2)
          if summoner_history:
            last_gameId = summoner_history[0]
            if last_gameId:
              last_game = api_get_last_game(last_gameId, server, puuid)
              if last_game:
                return [
                  "OK",
                  [
                    username, server, userId, puuid, last_gameId,
                    summoner_complete_rank, summoner_complete_rank, total_games, winrate
                  ]
                ]
            else:
              return ["KO dernière game"]
          else:
            return ["KO historique"]
        else:
          return ["KO rang"]
      else:
        return ["KO classé"]
    else:
      return ["KO infos"]
  else:
    return ["KO token"]


def check_last_game(username, server):
  actual = manage_csv.read(username, server)
  response = run_api(username, server)
  response_code = response[0]
  if response_code == "OK":
    check = manage_csv.create_dict(manage_csv.header, response[1])
    if actual['summonerName'] == check['summonerName'] and actual[
        'server'] == check['server']:
      if actual['lastGameId'] != check['lastGameId'] or actual[
          'currentRank'] != check['currentRank']:
        manage_csv.update_summoner_rank(check['summonerName'],
                                        check['currentRank'],
                                        check['lastGameId'],
                                        check['totalGames'],
                                        check['winrate'])
        average_rank.add_game_in_history(check['summonerName'],check['server'],check['id'],check['puuid'],check['lastGameId'])
        return check
  else:
    return None


def calculate_lp_difference(old, new):
  tiers = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER','GRANDMASTER', 'CHALLENGER']
  divisions = ['IV', 'III', 'II', 'I']
  old_tier, old_division, *old_lp = old.split(' ')
  new_tier, new_division, *new_lp = new.split(' ')
  old_index = tiers.index(old_tier) * len(divisions) + divisions.index(
    old_division)
  new_index = tiers.index(new_tier) * len(divisions) + divisions.index(
    new_division)
  old_lp_value = int(old_lp[0])
  new_lp_value = int(new_lp[0])

  lp_difference = (new_index - old_index) * 100 + (new_lp_value - old_lp_value)
  return lp_difference


def check():
  rows = manage_csv.full_read()
  diff_LP = 0
  player_message = ''
  global_message = []
  for row in rows:
    summoner_check = check_last_game(row['summonerName'], row['server'])
    if (summoner_check):
      diff_LP = calculate_lp_difference(row["currentRank"],
                                        summoner_check["currentRank"])
      player_message = f'{summoner_check["summonerName"]} - {row["currentRank"]} -> {summoner_check["currentRank"]} (**{diff_LP} LP**)'
      if diff_LP != 0:
        global_message.append((diff_LP, player_message))
  sorted_global_message = sorted(global_message, key=lambda x: x[0], reverse=True)
  return sorted_global_message
  
def full_check():
  filename = manage_csv.daily_graph('dataset.csv')
  rows = manage_csv.full_read()
  for row in rows:
    row["beginningDayRank"] = row["currentRank"]
  return filename
