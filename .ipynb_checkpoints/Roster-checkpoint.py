from Config import log
import time
import datetime
from Config import Config
from Player import Player


class Roster:
    
    def __init__(self):
        self.Size = 0
        self.LastUpdateDateTime = time.gmtime(0)
        self.Players = []
    

    def GetAllPlayers(self):
        self.Players = []
        url = Config.URL_player
        soup = Config.GetHTMLSoup(url)
        playerHTML = soup.find_all('option')
        for index, x in enumerate(playerHTML):
            if (index <3):
                continue
            id_str = x.get('value')
            player_name = x.get_text()
            try:
                player_id = int(id_str)
                if(player_name != ''):
                    newPlayer = Player(player_id, player_name)
                    self.Players.append(newPlayer)
            except:
                log.warning('Failed to convert')
                continue
        self.LastUpdateDateTime = datetime.datetime.now()
        self.Size = len(self.Players)
        log.info('Found %d players' % (self.Size))
        
    
    def Print(self):
        print('Found %s players' % (self.Size))
        for player in self.Players:
            print('%s - %s' % (str(player.ID), player.Name))
    
    
    def GetActivePlayers(self, season):
        
        # If the player list is empty, go retrieve the lastest list
        if (self.LastUpdateDateTime == time.gmtime(0)):
            log.info('Reloading Players')
            self.GetAllPlayers()
        
        # Get the latest list of eligible players
        url = COnfig.URL_roster
        soup = Config.GetHTMLSoup(url)
        x = soup.find_all(class_ = "table_1a")
        
        # STILL NEED TO DO STUFF HERE

    
    def GetOwners(self, season):
        # DO STUFF HERE
        log.info('GetOwners is being built')
        
        
        
        
    def GetRoster(self):
        self.Roster.GetAllPlayers(self.URL_player)


    