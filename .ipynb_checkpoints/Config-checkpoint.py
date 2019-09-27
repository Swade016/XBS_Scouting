import logging
import requests
import os
import yaml
import pandas as pd
from lxml import html
import urllib.request
import time
import datetime
from bs4 import BeautifulSoup
from enum import Enum
import inspect




log = logging.getLogger()
fhandler = logging.FileHandler(filename='mylog.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
log.addHandler(fhandler)
log.setLevel(logging.DEBUG)



class Config:
    
    URL = 'http://xbox-sports.com/leagues/xbshl/index.php'
    URL_game = 'http://xbox-sports.com/leagues/xbshl/index.php?mode=game'
    URL_roster = 'http://xbox-sports.com/leagues/xbshl/index.php?mode=league_rosters'
    URL_player = 'http://xbox-sports.com/leagues/xbshl/index.php?mode=player'
    URL_team = 'http://xbox-sports.com/leagues/xbshl/index.php?mode=team'
    
    Teams = {
        'Anaheim Ducks': 1,
        'Boston Bruins': 3,
        'Buffalo Sabres': 4,
        'Calgary Flames': 5,
        'Carolina Hurricanes': 6,
        'Chicago Blackhawks': 7,
        'Colorado Avalanche': 8,
        'Columbus Blue Jackets': 9,
        'Dallas Stars': 10,
        'Detroit Red Wings': 11,
        'Edmonton Oilers': 12,
        'Florida Panthers': 13,
        'Los Angeles Kings': 14, 
        'Minnesota Wild': 15,
        'Montreal Canadiens': 16,
        'Nashville Predators': 17,
        'New Jersey Devils': 18,
        'New York Islanders': 19,
        'New York Rangers': 20,
        'Ottawa Senators': 21,
        'Philadelphia Flyers': 22,
        'Arizona Coyotes': 23,
        'Pittsburgh Penguins': 24, 
        'San Jose Sharks': 25,
        'St Louis Blues': 26,
        'Tampa Bay Lightning': 27,
        'Toronto Maple Leafs': 28,
        'Vancouver Canucks': 29,
        'Washington Capitals': 30,
        'Winnepeg Jets': 34,
        'Vegas Golden Knights': 39}



    @staticmethod
    def GetHTMLSoup(url):
        log.info('Querying ' + url)
        response = requests.get(url)
        if (response.status_code == 200):
            log.info('Success!')
            response.headers['Content-Type']
            content = html.fromstring(response.content)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            log.warning('Failed to get soup for %s!' % (url))
            return ""


    @staticmethod
    def GetPlayerURL(player_id):
        try:
            pid = str(player_id)
            return '%s&player_id=%s' % (Config.URL_player, pid)
        except:
            log.warning('Could not find ' + str(player_id))

    @staticmethod
    def GetGameURL(game_id):
        try:
            gid = str(game_id)
            return '%s&game_id=%s' % (Config.URL_game, gid)
        except:
            log.warning('Could not find game ' + str(gid))
            
    @staticmethod
    def PrintObjectAttributes(obj):
        for i in inspect.getmembers(obj):
            # Ignores anything starting with underscore 
            # (that is, private and protected attributes)
            if not i[0].startswith('_'):
                # Ignores methods
                if not inspect.ismethod(i[1]):
                    print(i)
            


class Positions(Enum):
    Skater = 1
    Center = 2
    Wing = 3
    Defense = 4
    Goalie = 5
    
    
   