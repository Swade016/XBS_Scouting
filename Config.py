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
            
            
            
class Teams(Enum):
    Anaheim = 1
    Boston = 3
    Buffalo = 4
    Calgary = 5
    Carolina = 6
    Chicago = 7
    Colorado = 8
    Columbus = 9
    Dallas = 10
    Detroit = 11
    Edmonton = 12
    Florida = 13
    LosAngeles =14 
    Minnesota = 15
    Montreal = 16
    Nashville = 17
    NewJersey = 18
    NewYorkI = 19
    NewYorkR = 20
    Ottowa = 21
    Philadelphia = 22
    Arizona = 23
    Pittsburgh = 24 
    SanJose = 25
    StLouis = 26
    TampaBay = 27
    Toronto = 28
    Vancouver = 29
    Washington = 30
    Winnepeg = 34
    Vegas = 39

class Positions(Enum):
    Skater = 1
    Center = 2
    Wing = 3
    Defense = 4
    Goalie = 5
    
    
   