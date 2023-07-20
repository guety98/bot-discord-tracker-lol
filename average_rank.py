# -*- coding: utf-8 -*-

import riot
import manage_csv
import csv
import random

header_history = ['summonerName', 'server', 'userId', 'puuid', 'matchId', 'top']

def get_infos_summoner(summonerName):
    with open('dataset.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['summonerName'] == summonerName:
                return row
    return None

def count_lines_with_summoner(summonerName):
    count = 0
    with open('history.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['summonerName'] == summonerName:
                count += 1
    return count

# Verification presence d'un id de match avec un invocateur désigné dans le history.csv
def presence_history(invocateur, serveur, matchId):
    with open('history.csv', 'r', encoding='utf-8') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.DictReader(f)
        rows = list(obj)
        for row in rows:
            if invocateur.strip().lower() == row['summonerName'].strip().lower() and serveur.strip().lower() == row['server'].strip().lower() and matchId == row['matchId']:
              return True
    return False


def history_player(invocateur, serveur, debut, fin):
  player_history = []
  print(f'debut {debut}')
  print(f'fin {fin}')

  infos = get_infos_summoner(invocateur)
  if infos is not None:
    riot.check_last_game(invocateur, serveur)

    summoner_name = infos['summonerName']
    serveur = infos['server']
    userId = infos['id']
    puuid = infos['puuid']
    total_games = infos['totalGames']
    summoner_history_games = count_lines_with_summoner(invocateur)
    
    print(f'summonerName {summoner_name}')
    print(f'total_games {int(total_games)}')
    print(f'nb de games dans le history.csv {int(summoner_history_games)}')

    if invocateur == summoner_name and int(total_games) != int(summoner_history_games):
            summoner_history = riot.api_get_history(puuid, serveur, total_games)
            if summoner_history:
                #random.shuffle(summoner_history)
                print(summoner_history[debut:fin])
                if count_lines_with_summoner(invocateur) != total_games:
                  for matchId in summoner_history[debut:fin]:
                      game = riot.api_get_last_game(matchId, serveur, puuid)            
                      if game:
                        lastGame = riot.api_get_last_game(matchId, serveur, puuid)
                        if lastGame:
                          info = lastGame["info"]
                          participants = info["participants"]
                          for participant in participants:
                            if participant["puuid"] == puuid:
                              lastTop = participant["placement"]   
                              
                              player_history = [invocateur,serveur,userId,puuid,matchId,lastTop]                    
                              data_dict = manage_csv.create_dict(header_history, player_history)
                              if presence_history(invocateur, serveur, matchId) ==  False:
                                  print(f'matchId {matchId}')
                                  fichier = open('history.csv','a', newline='', encoding='utf-8')
                                  with fichier:    
                                      obj = csv.DictWriter(fichier, fieldnames=header_history)
                                      obj.writerow(data_dict)
            else:
                return ["KO historique"]
  else:
    return ["KO dataset"]

def calculate_average_top(summonerName):
  summ_top = 0
  average_top = 0
  with open('history.csv', 'r', newline='', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
          if row['summonerName'] == summonerName:
              summ_top += int(row['top'])
  total_games = count_lines_with_summoner(summonerName)
  if total_games != 0:
      average_top = round(summ_top/int(total_games), 2)
  else:
      average_top = "?"
  return average_top

def add_game_in_history(summonerName,server,userId,puuid,lastGameId):
  lastGame = riot.api_get_last_game(lastGameId, server, puuid)
  info = lastGame["info"]
  participants = info["participants"]
  for participant in participants:
    if participant["puuid"] == puuid:
      lastTop = participant["placement"]
      data = [summonerName, server, userId, puuid, lastGameId, lastTop]
      with open('history.csv', 'a', newline='') as file:
          writer = csv.writer(file)
          writer.writerow(data)

# Lecture du csv complet
def full_read():
    with open('history.csv', 'r', encoding='utf-8') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.DictReader(f)
        rows = list(obj)
        return rows