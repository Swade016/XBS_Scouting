import bs4
import re
import Stats
import Config
from Config import log
from Config import Config
from Config import Positions
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
        self.Scoring = []
        self.Penalties = []

        
        
    def Get(self):
        self.GetIndex()
        self.GetGameDetails()
        self.GetLineup()
        self.GetThreeStars()
        self.GetTeamStats()
        self.GetBoxScore()

    def GetIndex(self):
        self.IndexTeamStats = 0
        self.IndexLineup = 0
        self.IndexThreeStars = 0
        self.IndexGameDetails = 0
        self.IndexFirstPeriod = 0

        for index, tags in enumerate(self.HTML):
            for detail in tags:
                if (not isinstance(detail ,bs4.element.NavigableString)):
                    dl = detail.get_text().split('\n')
                    if ('1st Period' in dl[1]):
                        self.IndexFirstPeriod = index
                    elif ('Three Stars of the Game' in dl[1]):
                        self.IndexThreeStars = index
                    elif ('Team' == dl[1]):
                        self.IndexTeamStats = index
                        self.IndexLineup = index + 1
                    elif ('Boxscore' == dl[1]):
                        self.IndexGameDetails = index            
                    break

        log.info('Team Stats Index = %d' % (self.IndexTeamStats))
        log.info('Lineup Index = %d' % (self.IndexLineup))
        log.info('Three Stars Index = %d' % (self.IndexThreeStars))
        log.info('Game Details Index = %d' % (self.IndexGameDetails))
        log.info('First Period Index = %d' % (self.IndexFirstPeriod))

        
    def GetGameDetails(self):
        details = self.HTML[self.IndexGameDetails] 
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
        gt_clean = gt[:6]+gt[8:]
        self.GameDateTime = datetime.strptime(gt_clean, '%b %d, %Y %I:%M %p' )
        self.GameSeason = int(prep_gt[1])
        self.GameType = prep_gt[2]
        self.HomeTeam = '%s %s' % (detail_array[2], detail_array[3])
        self.HomeTeamScore = int(detail_array[4])
        self.AwayTeam = '%s %s' % (detail_array[5], detail_array[6])
        self.AwayTeamScore = int(detail_array[7])                    
                        
        
    
    
    def GetThreeStars(self):
        threestars = self.HTML[self.IndexThreeStars]
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
        details = self.HTML[self.IndexTeamStats] 
        
        for index, detail in enumerate(details):
            if (not isinstance(detail, bs4.element.NavigableString)):
#                 print(index)
                detail_line = detail.get_text()
                entries = re.split("\n+", detail_line)
#                 print(entries)
#                 print(len(entries))
                if (index == 5):
                    if(len(entries) == 14):
                        self.OT = False
                        self.HomeTeamStat = TeamGameStat(self.HomeTeam, entries[2], entries[3], entries[4], 0, entries[5], entries[6], entries[7], entries[8], entries[9], entries[10], entries[11], entries[12])
                    elif(len(entries) == 15):
                        self.OT = True
                        self.HomeTeamStat = TeamGameStat(self.HomeTeam, entries[2], entries[3], entries[4], entries[5], entries[6], entries[7], entries[8], entries[9], entries[10], entries[11], entries[12], entries[13])
                elif (index == 7):
                    if(len(entries) == 14):
                        self.OT = False
                        self.AwayTeamStat = TeamGameStat(self.AwayTeam, entries[2], entries[3], entries[4], 0, entries[5], entries[6], entries[7], entries[8], entries[9], entries[10], entries[11], entries[12])
                    elif(len(entries) == 15):
                        self.OT = True
                        self.AwayTeamStat = TeamGameStat(self.AwayTeam, entries[2], entries[3], entries[4], entries[5], entries[6], entries[7], entries[8], entries[9], entries[10], entries[11], entries[12], entries[13])

        
    
    def GetLineup(self):
        details = self.HTML[self.IndexLineup] 
        detail_array = []

        for index, detail in enumerate(details):
            if (not isinstance(detail, bs4.element.NavigableString)):
                detail_line = detail.get_text()
                entries = re.split("\n+", detail_line)

                for entry in entries:
                    if not (entry.strip('\t') in ('', 'Rating', 'Three Stars of the Game', 'Game Leaders')):
                        detail_array += [entry.replace('\xa0', '').strip()]
                    else: 
                        continue

        self.AwayTeamLineup = {}
        self.AwayTeamLineup.update({detail_array[10]: detail_array[9]})
        self.AwayTeamLineup.update({detail_array[19]: detail_array[18]})
        self.AwayTeamLineup.update({detail_array[28]: detail_array[27]})
        self.AwayTeamLineup.update({detail_array[37]: detail_array[36]})
        self.AwayTeamLineup.update({detail_array[46]: detail_array[45]})
        self.AwayTeamLineup.update({detail_array[55]: detail_array[54]})

        self.HomeTeamLineup = {}
        self.HomeTeamLineup.update({detail_array[101]: detail_array[100]})
        self.HomeTeamLineup.update({detail_array[110]: detail_array[109]})
        self.HomeTeamLineup.update({detail_array[119]: detail_array[118]})
        self.HomeTeamLineup.update({detail_array[128]: detail_array[127]})
        self.HomeTeamLineup.update({detail_array[137]: detail_array[136]})
        self.HomeTeamLineup.update({detail_array[146]: detail_array[145]})
 
    
    def GetBoxScore(self):
        # Initialize Variables for Looping
        htmlIndex = self.IndexFirstPeriod
        period = 1
        score = '0 - 0'
        stillPlaying = True

        while (stillPlaying):
            details = self.HTML[htmlIndex] 
            detail_array = []

            for index, detail in enumerate(details):
                if (not isinstance(detail, bs4.element.NavigableString)):
                    detail_line = detail.get_text().replace(u'\xa0', u' ').replace('Assists: ','')
                    entries = re.split("\n+", detail_line)
                    for entry in entries:
                        if not (entry.strip('\t') in ('')):
                            detail_array += [entry.strip()]
                        else: 
                            continue

            length = len(detail_array)
            cursor = 2

            # Check to see if there were any goals
            chk_goal = not (detail_array[cursor] == 'No scoring.')
            if (chk_goal):
                log.info('Goals Found')
                while chk_goal:
                    goaltype = 'ES'
                    ts = detail_array[cursor]
                    cursor += 2
                    plr = detail_array[cursor]
                    cursor += 1
                    if (detail_array[cursor] == 'Unassisted'):
                        log.info('Goal was Unassisted')
                        a1 = ''
                        a2 = ''
                        cursor += 1
                    else:
                        assists = detail_array[cursor]
                        if (',' in assists):
                            assistssplt = assists.split(',')
                            a1 = assistssplt[0].strip()
                            a2 = assistssplt[1].strip()
                        else:
                            a1 = assists
                            a2 = ''
                        cursor += 1

                        if (detail_array[cursor] == 'Power Play Goal'):
                            log.info('Power Play Goal found')
                            goaltype = 'PP'
                            cursor += 1
                        elif (detail_array[cursor] == 'Shorthand Goal'):
                            log.info('Shorthanded Goal found')
                            goaltype = 'PK'
                            cursor += 1


                    score = detail_array[cursor]
                    cursor += 1
                    teamname = detail_array[cursor]
                    cursor += 1
                    goal = Stats.Goal(period, ts, plr, a1, a2, goaltype, score)
                    self.Scoring += [goal]

                    chk_goal = not (detail_array[cursor] == 'Penalties')
                
                log.info('Goals complete, move to penalties')
                cursor += 1
            else:
                log.info('No goals, move to penalties')
                cursor = 4

            chk_pen = not (detail_array[cursor] == 'No penalties.')
            if (chk_pen):
                log.info('Penalties Found')
                while chk_pen:
                    ts = detail_array[cursor]
                    cursor += 2
                    plr = detail_array[cursor]
                    cursor += 1
                    infr = detail_array[cursor]
                    fight = (infr == 'Fighting')
                    cursor += 1
                    dur = detail_array[cursor].replace(' minutes', '')
                    maj = (dur == 5)
                    cursor += 1            
                    penalty = Stats.Penalty(period, ts, plr, infr, maj, fight)
                    self.Penalties += [penalty]
                    chk_pen = (cursor < length)
                log.info('Penalties complete, end recursion')
            else:
                log.info('No penalties, move to next period')


            # Check to see if there are more periods
            scorecheck = score.split('-')
            lscr = scorecheck[0].strip()
            rscr = scorecheck[1].strip()
            
            if (period < 3):
                stillPlaying = True
            elif (lscr == rscr):
                stillPlaying = True
            else:
                stillPlaying = False
            period += 1
            htmlIndex += 1



#         print('\n\n BEGIN GOALS! \n\n')
#         for scr in scoring:
#             print('Period = %d' % scr.Period)
#             print('Time = ' + scr.TimeStamp)
#             print('Scorer = ' + scr.Scorer)
#             print('1A = ' + scr.PrimaryAssist)
#             print('2A = ' + scr.SecondaryAssist)
#             print('GoalType = ' + scr.GoalType)
#             print('Score = ' + scr.Score)
#             print('\n')

#         print('\n\n BEGIN PENALTIES! \n\n')
#         for plt in penalties:
#             print('Period = %d' % plt.Period)
#             print('TimeStamp = ' + plt.TimeStamp)
#             print('Player = ' + plt.Player)
#             print('Infraction = ' + plt.Infraction)
#             print('Major = ' + str(plt.IsMajor))
#             print('\n')


        
        
    