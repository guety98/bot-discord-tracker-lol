import interactions
from interactions import autodefer
import os
import asyncio
import requests
import schedule
import manage_csv
import riot
import pandas as pd
import matplotlib.pyplot as plt
import average_rank
import re

# Initialisation

discord_token = os.environ['DISCORD_TOKEN']

guild_id = os.environ['guild_id']
channel_id = os.environ['channel_id']
green_color = 0x00FF00
red_color = 0xFF0000

# Reset beginningDayRank avec currentRank

# Fonctions


def run_discord_bot():
  bot = interactions.Client(token=discord_token)

  async def send_message(channel_id, message, color):
    payload = {
      "content": " ",
      "embeds": [{
        "description": message,
        "color": f"{color}"
      }]
    }
    header = {"authorization": f"Bot {discord_token}"}
    response = requests.post(
      f"https://discord.com/api/v9/channels/{channel_id}/messages",
      json=payload,
      headers=header)

  async def send_file(channel_id, message, color, filename):
    header = {"authorization": f"Bot {discord_token}"}
    payload = {
      "content": " ",
      "embeds": [{
        "description": message,
        "color": f"{color}"
      }]
    }
    # File
    file = {
      "file":
      (filename, open(filename,
                      'rb'))  # The picture that we want to send in binary
    }
    response = requests.post(
      f"https://discord.com/api/v9/channels/{channel_id}/messages",
      json=payload,
      headers=header,
      files=file)

  async def daily_check():
    filename = riot.full_check()
    message = "Voici le récapitulatif de la journée"
    await send_file(channel_id, message, green_color, filename)

  async def game_check():
    global_message = riot.check()
    if global_message:
      await send_message(channel_id, "***Récapitulatif de cette dernière heure***", 0x000000)
      for player_message in global_message:
        diff_LP = player_message[0]
        format_message = player_message[1]
        print(f"{format_message}")
        if diff_LP > 0:
          await send_message(channel_id, format_message, green_color)
        elif diff_LP < 0:
          await send_message(channel_id, format_message, red_color)

  
  @bot.command(scope=guild_id)
  async def tft(ctx: interactions.CommandContext):
    """Tracker TFT"""
    pass

  @tft.subcommand()
  @autodefer()  # configurable
  async def wake(ctx):
    """Wake up the bot"""
    await asyncio.sleep(5)
    await ctx.send("I'm awake now!")

  @tft.subcommand()
  @autodefer()  # configurable
  async def help(ctx):
    """Savoir comment utiliser le bot"""
    await asyncio.sleep(1)
    await ctx.send(
      f"Voici comment utiliser le tracker TFT. Vous pouvez :\n- Regarder le rang de tout le serveur (/tft discord_rank)\n- Ajouter un invocateur dans le tracker (/tft add) __**Finissez vos placements avant d'ajouter votre compte**__\n- Retirer un invocateur du tracker (/tft remove)"
    )

  # Synchronisez les commandes slash
  @tft.subcommand()
  @autodefer()  # configurable
  async def sync(ctx):
    """Re-sync slash commands (owner only)"""
    if ctx.user.id == os.environ['owner_id'] or ctx.user.id == os.environ['akerman_id']:
      await asyncio.sleep(1)
      await bot._Client__sync()
      await ctx.send(f"Command tft synced.")
    else:
      await ctx.send(f"You must be the owner to use this command!")

  #@tft.subcommand()
  #@interactions.option(description="Invocateur")
  #@interactions.option(description="Serveur associé à l'invocateur recherché")
  #@interactions.option(description="Debut history")
  #@interactions.option(description="Fin history")

  async def rank(ctx,
                 invocateur: str = None,
                 serveur: str = None,
                 debut: str = None,
                 fin: str = None):
    """Connaître le rang d'un invocateur"""
    if invocateur == None or serveur == None:
      await asyncio.sleep(1)
      await ctx.send(
        f"Tu as mal tapé la commande, renseigne bien l'invocateur et son serveur associé"
      )

    else:
      # ALIMENTATION A GRANDE ECHELLE DE HISTORY.CSV     
      average_rank.history_player(invocateur,serveur,int(debut),int(fin))    
      average_top = average_rank.calculate_average_top(invocateur)
      player_data = manage_csv.read(invocateur, serveur)
      if invocateur == player_data['summonerName'] and serveur == player_data[
          'server']:
        await asyncio.sleep(1)            
        await ctx.send(f"{player_data['summonerName']} ({player_data['server']}) - {player_data['currentRank']} ({average_top} de moyenne)")
        #await ctx.send(f"Voici le rang de {invocateur} pour le serveur {serveur}")

  
  @tft.subcommand()
  @autodefer()  # configurable
  async def discord_rank(ctx):
    """Connaître le rang de tout le discord"""
    await asyncio.sleep(3)
    #message = ""
    manage_csv.sort_csv()
    discord_data = manage_csv.full_read()

    # Créer un dictionnaire contenant les données
    table_data = {
        'Classement': [],
        'Invocateur': [],
        'Rang actuel': [],
        'Games': [],
        'Top moyen': [],
        'Winrate': [],
    }

    for index, player_data in enumerate(discord_data):
      summoner_name = player_data['summonerName']
      current_rank = player_data['currentRank']
      total_games = player_data['totalGames']
      winrate = player_data['winrate']
      averageTop = average_rank.calculate_average_top(player_data['summonerName'])

      # Définir les valeurs de remplacement correspondantes
      remplacements = {
          "IV": "4",
          "III": "3",
          "II": "2",
          "I": "1"
      }

      # Rechercher les motifs "IV", "III", "II" ou "I" dans la chaîne et les remplacer
      for motif, remplacement in remplacements.items():
          current_rank = re.sub(r"\b" + motif + r"\b", remplacement, current_rank)

      if "MASTER 1" in current_rank:
        current_rank = current_rank.replace("MASTER 1", "MASTER")

      # Définir le dictionnaire de correspondance des rangs et abréviations
      correspondance_rangs = {
          "DIAMOND ": "D",
          "PLATINUM ": "P",
          "GOLD ": "G",
          "SILVER ": "S",
          "BRONZE ": "B",
          "IRON ": "I",
      }

      # Parcourir le dictionnaire de correspondance et effectuer le remplacement
      for rang, abreviation in correspondance_rangs.items():
          if rang in current_rank:
              current_rank = current_rank.replace(rang, abreviation)
              break  # Sortir de la boucle après le premier remplacement

      # Retrait de l'espace " LP" dans le rang
      current_rank = re.sub(r'\sLP', 'LP', current_rank)

      table_data['Classement'].append(index+1)
      table_data['Invocateur'].append(summoner_name)
      table_data['Rang actuel'].append(current_rank)
      table_data['Games'].append(total_games)
      table_data['Top moyen'].append(averageTop)
      table_data['Winrate'].append(winrate+"%")


      #if total_games and winrate:
      #  message += f"{index+1}) {summoner_name} | {current_rank} | {total_games} games / {winrate}% WR\n"
      #else:
      #  message += f"{index+1}) {summoner_name} | {current_rank}\n"
    
    # Supprimer le dernier séparateur s'il existe
    #if message.endswith("\n"):
    #  message = message[:-1]


    #if len(message) <= 2000:
    #    await ctx.send(message)
    #else:
    #    while message:
    #        await ctx.send(message[:2000])
    #        message = message[2000:]

 
    # Créer le DataFrame à partir du dictionnaire
    df = pd.DataFrame(table_data)

    # Créer le graphique à partir du DataFrame
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')  # Supprimer les axes du graphique   

    # Créer le graphique à partir du DataFrame
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')  # Supprimer les axes du graphique
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    
    # Appliquer le style au graphique
    table = ax.tables[0]
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)  # Ajuster la taille de la table
  
    # Appliquer le fond de couleur et la couleur de police d'écriture
    for key, cell in table.get_celld().items():
      cell.set_facecolor('#161821')
      cell.set_text_props(color='white')
        
    # Enregistrer le tableau en tant qu'image
    output_image_path = 'discord_rank.png'
    plt.savefig(output_image_path, bbox_inches='tight', pad_inches=0)

    # Envoi de l'image
    await ctx.send(f"**Voici le tableau des rangs des joueurs.**")
    #await send_message(channel_id, f"**Voici le tableau des rangs des joueurs.**", 0x161821)
    await send_file(channel_id, "Voici le tableau des rangs des joueurs", green_color, output_image_path)

    # Fermer la figure pour libérer la mémoire
    plt.close(fig)


  @tft.subcommand()
  @interactions.option(description="Nom de l'invocateur")
  @interactions.option(description="Serveur associé")
  @autodefer()  # configurable
  async def add(ctx, invocateur: str, serveur: str):
    "Ajouter un invocateur dans le tracker"
    await asyncio.sleep(3)
    retour = manage_csv.write(invocateur, serveur.upper())
    if "Erreur Récupération Token" in retour:
      await ctx.send(f"*La connexion au service Riot est KO.*")
    elif "Erreur Récupération Infos" in retour:
      await ctx.send(
        f"*L'invocateur {invocateur} pour le serveur {serveur} n'est pas reconnu par le service Riot, vérifie que tu as bien tapé tes infos.*"
      )
    elif "Erreur Récupération Classé" in retour:
      await ctx.send(
        f"*{invocateur}, tu n'es pas classé actuellement. Finis bien tes placements.*"
      )
    elif "Erreur Récupération Rang Actuel" in retour:
      await ctx.send(f"*Impossible de récupérer ton rang actuel {invocateur}.*"
                     )
    elif "Erreur Récupération Dernière Game" in retour:
      await ctx.send(
        f"*Impossible de récupérer ta dernière game {invocateur}.*")
    elif "Present" in retour:
      await ctx.send(
        f"*L'utilisateur {invocateur} est déjà dans le tracker pour le serveur {serveur}.*"
      )
    elif "Taille" in retour:
      await ctx.send(f"*Trop d'invocateurs dans le tracker.*")
    elif "OK" in retour:
      manage_csv.sort_csv()
      await ctx.send(f"*Vous avez bien ajouté l'invocateur {invocateur} pour le serveur {serveur}.*")

  @tft.subcommand()
  @interactions.option(description="Nom de l'invocateur")
  @interactions.option(description="Serveur associé")
  @autodefer()  # configurable
  async def remove(ctx, invocateur: str, serveur: str):
    "Retirer un invocateur dans le tracker"
    retour = manage_csv.delete(invocateur, serveur)
    await asyncio.sleep(1)
    if "Erreur" in retour:
      await ctx.send(
        f"Impossible de retirer l'invocateur {invocateur} pour le serveur {serveur}"
      )
    elif "OK" in retour:
      manage_csv.sort_csv()
      await ctx.send(
        f"*Vous avez bien retiré l'invocateur {invocateur} pour le serveur {serveur}.*"
      )

  async def run_check():
    while True:
      await asyncio.sleep(1)
      schedule.run_pending()

  loop = asyncio.get_event_loop()
  # Il y a un décalage de -2h entre l'heure indiquée et l'heure réelle en France
  #schedule.every().friday.at("20:00").do(loop.create_task, daily_check())
  #schedule.every(15).minutes.do(lambda: loop.create_task(game_check()))
  schedule.every().hour.at(':59').do(lambda: loop.create_task(game_check()))
  loop.create_task(run_check())
  loop.create_task(bot.start())
  loop.run_forever(
  )  # Boucle d'événements pour gérer les événements Discord et les tâches planifiées avec schedule
