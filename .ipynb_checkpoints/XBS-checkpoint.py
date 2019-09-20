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
from Config import Config
from Roster import Roster
from Season import Season


class XBS:    

    def __init__(self):
        self.Config = Config()
        self.Roster = Roster()
        self.Season = Season()
        
    def GetTeams(self):
        self.League.GetAllTeams(self.URL_team)        

    def GetSeason(self):
        self.Season.GetAllGames(self.URL_game)
        

    
