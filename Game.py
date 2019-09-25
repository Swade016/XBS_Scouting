import bs4
import re
from Config import log
from Config import Config
from Config import Positions
from Config import Teams
from bs4 import BeautifulSoup
from Stats import TeamGameStat
from datetime import datetime


class Game:

    url_game = 'http://xbox-sports.com/leagues/xbshl/index.php?mode=game&game_id='
    
    
    def __init__(self, game_ID):
        self.GameID = game_ID
        self.URL = Config.GetGameURL(self.GameID)
        self.Goals = []
        self.Penalties = []
        self.Soup = Config.GetHTMLSoup(self.URL)
        self.HTML = self.Soup.find_all('table')
        
#         self.HomeTeam = 
#         self.AwayTeam = 

    def GetBoxScore(self):
        log.info('Under Construction')
        self.GetThreeStars()
        self.GetGameDetails()
        self.GetTeamStats()


        
    def GetGameDetails(self):
        details = self.HTML[25] 
        detail_array = []

        for detail in details:
            if (not isinstance(detail, bs4.element.NavigableString)):
                detail_line = detail.get_text()
                entries = re.split("\n+", detail_line)
                for entry in entries:
                    if not (entry.strip('\t') in ('', 'Boxscore')):
                        #print(repr(entry))
                        detail_array += [entry]
                    else: 
                        continue

        prep_gt = detail_array[0].replace('Scheduled for ', '').replace(' ESTSeason ', ';').replace(' @', '').replace(' - ', ';').split(';')
        gt = prep_gt[0]
        self.GameDateTime = datetime.strptime(gt, '%b %dth, %Y %I:%M %p' )
        self.GameSeason = int(prep_gt[1])
        self.GameType = prep_gt[2]
        self.HomeTeam = '%s %s' % (detail_array[2], detail_array[3])
        self.HomeTeamScore = int(detail_array[4])
        self.AwayTeam = '%s %s' % (detail_array[5], detail_array[6])
        self.AwayTeamScore = int(detail_array[7])                    
                        
        
    def GetThreeStars(self):
        threestars = self.HTML[21]
        player_array = []

        for star in threestars:
            if (not isinstance(star, bs4.element.NavigableString)):
                star_line = star.get_text()
                entries = re.split("\n+", star_line)
                for entry in entries:
                    if not (entry.strip('\t') in ('', 'Rating', 'Three Stars of the Game', 'Game Leaders')):
                        player_array += [entry]
                    else: 
                        continue

#         print(player_array)
        
        offset = 0
#         print('Player 1 metric 1 = ' + player_array[1])
        if ('GAA' in player_array[1]):
            self.FirstStar = {player_array[0]: player_array[3]}
            offset += 1
        else:
            self.FirstStar = {player_array[0]: player_array[4]} 

#         print('Player 2 metric 1 = ' + player_array[6-offset])
        if ('GAA' in player_array[6-offset]):
            self.SecondStar = {player_array[5-offset]: player_array[8-offset]}
            offset += 1
        else:
            self.SecondStar = {player_array[5-offset]: player_array[9-offset]}
        
#         print('Player 3 metric 1 = ' + player_array[11-offset])
        if ('GAA' in player_array[11-offset]):
            self.ThirdStar = {player_array[10-offset]: player_array[13-offset]}
            offset += 1
        else:
            self.ThirdStar = {player_array[10-offset]: player_array[14-offset]}
     
        
        
    
    
    def GetTeamStats(self):
        details = self.HTML[26] 
        
        for index, detail in enumerate(details):
            if (not isinstance(detail, bs4.element.NavigableString)):
#                 print(index)
                detail_line = detail.get_text()
                entries = re.split("\n+", detail_line)
#                 print(entries)
#                 print(len(entries))
                if (index == 5):
                    if(len(entries) == 14):
                        self.HomeTeamStat = TeamGameStat(self.HomeTeam, entries[2], entries[3], entries[4], 0, entries[5], entries[6], entries[7], entries[8], entries[9], entries[10], entries[11], entries[12])
                    elif(len(entries) == 15):
                        self.HomeTeamStat = TeamGameStat(self.HomeTeam, entries[2], entries[3], entries[4], entries[5], entries[6], entries[7], entries[8], entries[9], entries[10], entries[11], entries[12], entries[13])
                elif (index == 7):
                    if(len(entries) == 14):
                        self.AwayTeamStat = TeamGameStat(self.AwayTeam, entries[2], entries[3], entries[4], 0, entries[5], entries[6], entries[7], entries[8], entries[9], entries[10], entries[11], entries[12])
                    elif(len(entries) == 15):
                        self.AwayTeamStat = TeamGameStat(self.AwayTeam, entries[2], entries[3], entries[4], entries[5], entries[6], entries[7], entries[8], entries[9], entries[10], entries[11], entries[12], entries[13])

        
    
    def GetLineupInfo(self):
        details = self.HTML[27] 

        for index, detail in enumerate(details):
            if (not isinstance(detail, bs4.element.NavigableString)):
                detail_line = detail.get_text()
                entries = re.split("\n+", detail_line)

                for entry in entries:
                    if not (entry.strip('\t') in ('', 'Rating', 'Three Stars of the Game', 'Game Leaders')):
                        detail_array += [entry.replace('\xa0', '').strip()]
                    else: 
                        continue

        a1 = {detail_array[10]: detail_array[9]}
        a2 = {detail_array[19]: detail_array[18]}
        a3 = {detail_array[28]: detail_array[27]}
        a4 = {detail_array[37]: detail_array[36]}
        a5 = {detail_array[46]: detail_array[45]}
        a6 = {detail_array[55]: detail_array[54]}
        AwayTeam = [a1, a2, a3, a4, a5, a6]

        h1 = {detail_array[101]: detail_array[100]}
        h2 = {detail_array[110]: detail_array[109]}
        h3 = {detail_array[119]: detail_array[118]}
        h4 = {detail_array[128]: detail_array[127]}
        h5 = {detail_array[137]: detail_array[136]}
        h6 = {detail_array[146]: detail_array[145]}
        HomeTeam = [h1, h2, h3, h4, h5, h6]

        print(AwayTeam)

        self.AwayCenter
        self.AwayLeftWing
        self.AwayRightWing
        self.AwayLeftDefense
        self.AwayRightDefense
        self.AwayGoalie
        self.HomeCenter
        self.HomeLeftWing
        self.HomeRightWing
        self.HomeLeftDefense
        self.HomeRightDefense
        self.HomeGoalie
    
    
    def GetGoalInfo(self):
        log.info('Under Construction')
        
    
    def GetPenaltyInfo(self):
        log.info('Under Construction')
        
    