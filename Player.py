import numpy
import pandas as pd
from Config import Config
from Config import Positions
from Config import log
import Stats



class Player:
        
#    def player_url(player_id):
#        url_player_id = "%s;&player_id=%s" % (XBS.GetUrl('player'), str(player_id))
#        return url_player_id
                         
    def __init__(self, player_id, player_name):
        self.PID = player_id
        self.Name = player_name
        self.SeasonStats = Stats.SeasonStats(self.PID, self.Name)
    
    def __repr__(self):
        return '%s - %s' % (self.PID, self.Name)
    
    def __str__(self):
        return '%s - %s' % (self.PID, self.Name)
    
    
    
    # THIS STILL NEEDS BUILT TO GET THEIR LEAGUE PREFERENCES
    def GetPlayerDetails(self):
        log.info("Extracting data for: %s (%s)" % (self.Name, self.PID))
        url_player = Config.GetPlayerURL(self.PID)
        soup = Config.GetHTMLSoup(url_player)
        return soup


    def GetSeasonStats(self):
        self.SeasonStats.GetStats()
