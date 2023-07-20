import csv
import riot
import datetime  
import matplotlib.pyplot as plt
import pandas as pd
import os

# Initialisation

synthax_error = "`Erreur : Merci de taper la commande correctement (vous pouvez voir les commandes disponibles avec /tft help)`"
synthax_add_error = "`Erreur : Merci de taper la commande comme suit : /tftadd BotKZ EUW`"
token_error = "`Erreur Récupération Token : La connexion à l'API de Riot`"
infos_error = "`Erreur Récupération Infos : Tu n'as pas tapé correctement un utilisateur ou un serveur`"
ranked_error = "`Erreur Récupération Classé : Cet Invocateur n'a pas joué en classé cette saison`"
rank_error = "`Erreur Récupération Rang Actuel : Impossible de récupérer le rang actuel de l'Invocateur`"
history_error = "`Erreur Récupération Dernières Games : Impossible de récupérer les dernières games de l'Invocateur`"
last_game_error = "`Erreur Récupération Dernière Game : Impossible de récupérer la dernière game de l'Invocateur`"

#a_faire = "Résultat de partie\n"+top+summoner_name+" vient de "+win_or_lose+" + "+ lp_diff+ " point(s) de ligue ! ("+updated_rank+")\nCompo : "+compo+"\n"+timestamp
bot_verify_error = "`Impossible de vérifier le rang de l'utilisateur "
bot_verify_end = "`"
bot_verify_empty = "`Tracker vide`"



header = ['summonerName', 'server', 'id', 'puuid', 'lastGameId', 'beginningDayRank', 'currentRank', 'totalGames', 'winrate']

# Avoir la taille du csv
def count_csv_rows():
    with open('dataset.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        row_count = len(list(reader))
    return row_count
      
# Lecture du csv complet
def full_read():
    with open('dataset.csv', 'r', encoding='utf-8') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.DictReader(f)
        rows = list(obj)
        return rows

# Lecture d'une seule ligne du csv
def read(invocateur, serveur):
    with open('dataset.csv', 'r', encoding='utf-8') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.DictReader(f)
        rows = list(obj)
        for row in rows:
            if invocateur.strip().lower() == row['summonerName'].strip().lower() and serveur.strip().lower() == row['server'].strip().lower():
                return row
    return None

def create_dict(header, data):
    result = {}
    for i in range(len(header)):
        result[header[i]] = data[i]
    return result
    
        
def write(invocateur, serveur):
    current_time = datetime.datetime.now()
    str_date = current_time.strftime("%d-%m-%Y %H:%M:%S")
    if count_csv_rows() > 50:
      return "Taille"
  
    response = riot.run_api(invocateur, serveur)
    response_code = response[0]
    if response_code == "OK":
        data_dict = create_dict(header, response[1])
        if read(invocateur, serveur) ==  None:
            fichier = open('dataset.csv','a', newline='', encoding='utf-8')
            with fichier:    
                obj = csv.DictWriter(fichier, fieldnames=header)
                obj.writerow(data_dict)
            return "OK"
        else:
            return "Present"
    elif response_code == "KO token":
        print(f'{str_date} {invocateur}: '+token_error)
        return token_error
    elif response_code == "KO infos":
        print(f'{str_date} {invocateur}: '+infos_error)
        return infos_error
    elif response_code == "KO classé":
        print(f'{str_date} {invocateur}: '+ranked_error)
        return ranked_error
    elif response_code == "KO rang":
        print(f'{str_date} {invocateur}: '+rank_error)
        return rank_error
    elif response_code == "KO historique":
        print(f'{str_date} {invocateur}: '+history_error)
        return history_error
    elif response_code == "KO dernière game":
        print(f'{str_date} {invocateur}: '+last_game_error)
        return last_game_error

def delete(invocateur, serveur):
    if read(invocateur, serveur) !=  None:
      # Lire le contenu du fichier CSV dans une liste de dictionnaires
      lignes = []
      with open('dataset.csv','r', encoding='utf-8') as fichier:
          lecteur = csv.DictReader(fichier)
          lignes = list(lecteur)
  
      # Identifier et supprimer la ligne correspondante
      lignes_mises_a_jour = [ligne for ligne in lignes if ligne['summonerName'] != invocateur]
  
      # Réécrire le contenu mis à jour dans le fichier CSV
      with open('dataset.csv', "w", newline='', encoding='utf-8') as fichier:
          writer = csv.DictWriter(fichier, fieldnames=lecteur.fieldnames)
          writer.writeheader()
          writer.writerows(lignes_mises_a_jour)
      return "OK"
    else:
        return "Erreur"

def update_summoner_rank(summoner_name, new_rank, new_gameId, total_games, winrate):
    with open('dataset.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        rows = list(csv_reader)
    
    updated = False
    for row in rows:
        if row['summonerName'] == summoner_name:
            row['currentRank'] = new_rank
            row['lastGameId'] = new_gameId
            row['totalGames'] = total_games
            row['winrate'] = winrate
            updated = True
    
    if updated:
        with open('dataset.csv', mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

def sort_tft_ranks():
    tier_order = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
    rank_order = ['IV', 'III', 'II', 'I']
    sorted_list = []
    list_to_sort = full_read()
    for row in list_to_sort:
        summoner_name, summoner_server = row['summonerName'], row['server']
        summoner_tier, summoner_rank, summoner_lp, lp_suffix = row['currentRank'].split(' ')
        tier_index = tier_order.index(summoner_tier)
        rank_index = rank_order.index(summoner_rank)
        summoner_lp = int(summoner_lp)
        rank_dict = {'summonerName': summoner_name, 'server': summoner_server, 'id': row['id'], 'puuid': row['puuid'], 'lastGameId': row['lastGameId'], 'beginningDayRank': row['beginningDayRank'], 'currentRank': row['currentRank'], 'Tier': tier_index, 'Rank': rank_index, 'LP': summoner_lp, 'totalGames': row['totalGames'], 'winrate':row['winrate']}
        sorted_list.append(rank_dict)

    sorted_list.sort(key=lambda x: (x['Tier'], x['Rank'], x['LP']), reverse=True)
    return sorted_list

def sort_csv():
    with open('dataset.csv', 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = [dict(zip(['summonerName', 'server', 'id', 'puuid', 'lastGameId', 'beginningDayRank', 'currentRank', 'totalGames', 'winrate'], row)) for row in reader]

    sorted_data = sort_tft_ranks()

    with open('dataset.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in sorted_data:
            row.pop('Tier')
            row.pop('Rank')
            row.pop('LP')
            writer.writerow(row)

def daily_graph(file):
    current_time = datetime.datetime.now()
    str_day = current_time.strftime("%d-%m-%Y")

    # Lire le fichier CSV
    df = pd.read_csv(file)

    # Tracer une courbe pour chaque joueur
    #for i in range(len(df)):
    #    summoner_name = df.iloc[i]['summonerName']
    #    beginning_rank = df.iloc[i]['beginningDayRank']
    #    current_rank = df.iloc[i]['currentRank']

        # Extraire la valeur numérique du rang en utilisant une expression régulière
    #    beginning_rank_num = int(re.search(r'\d+', beginning_rank).group())
    #    current_rank_num = int(re.search(r'\d+', current_rank).group())
    #    plt.plot([beginning_rank, current_rank], label=f"{summoner_name}: {beginning_rank} → {current_rank}", marker='o')

    # Supprimer les graduations de l'axe des x
    #plt.xticks([])

    # Configuration du graphique
    #plt.ylabel('Rang')
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), borderaxespad=0.)
    #plt.title(f'Evolution du rang des joueurs - {str_day} (graphe experimental)')


    # Extraire la division du rang
    df['division'] = df['currentRank'].str.split(' ').str[0]

    # Effectuer le décompte des rangs
    rank_counts = df['division'].value_counts()
    
    # Liste des tiers dans l'ordre souhaité
    tiers = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER','GRANDMASTER', 'CHALLENGER']

    # Couleurs pour chaque tier
    colors = ['#372728', '#583D3B', '#717C88', '#D9B682', '#6CD0C5', '#3F598E', '#B44CE5', '#9F2820', '#02739F']

    # Réorganiser les données selon l'ordre des tiers
    rank_counts = rank_counts.reindex(tiers)

    # Vérifier les valeurs NaN
    if rank_counts.isnull().values.any():
        rank_counts = rank_counts.fillna(0)

    # Filtrer les pourcentages non nuls
    non_zero_counts = rank_counts[rank_counts != 0]
    
    # Création du diagramme en camembert
    plt.pie(non_zero_counts, colors=colors, autopct='%1.1f%%', startangle=90)
    
    # Ajout d'un titre
    plt.title('Répartition des joueurs par rang')

    # Sauvegarde du graphique
    script_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(script_dir, str_day + ' - ' + os.path.splitext(file)[0] + '.png') # Générer le nom de fichier pour la sauvegarde
    plt.savefig(filename, bbox_inches='tight')

    # Affichage du graphique
    #plt.show()

    return filename