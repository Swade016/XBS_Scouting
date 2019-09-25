import numpy
import pandas as pd
from Config import Config
from Config import Positions
from Config import log
from datetime import datetime

class Goal:
    def __init__(self, period, ts, scorer, A1, A2, goaltype):
        raise ValueError('Period can only be 1, 2, 3, or OT.') if (period not in ['1', '2', '3', 'OT']) else False
        self.Period = period
        self.TimeStamp = ts
        
        raise ValueError('You must supply a Goal scorer.') if (scorer == '' or scorer is None) else False
        self.Scorer = scorer
        self.PrimaryAssist = A1
        self.SecondaryAssist = A2
        
        if (goaltype not in ('ES', 'PP', 'SH')): raise ValueError('Can only accept ES, PP, or SH.')
        self.GoalType = goaltype
        
        
class Penalty:
    def __init__(self, period, ts, player, infraction, IsMajor, IsFighting, FightWon):
        raise ValueError('Period can only be 1, 2, 3, or OT.') if (period not in ['1', '2', '3', 'OT']) else False
        self.Period = period
        self.TimeStamp = ts
        
        raise ValueError('You must supply a Player.') if (player == '' or player is None) else False
        self.Infraction = infraction
        self.IsFighting = IsFighting
        self.FightWon = FightWon


class TeamGameStat:
    def __init__(self, team_name, p1, p2, p3, ot, final, shots, hits, toa, pim, pp, pk, fow):
        self.Name = team_name
        self.FirstPeriod = int(p1)
        self.SecondPeriod = int(p2)
        self.ThirdPeriod = int(p3)
        self.OT = int(ot)
        self.Final = int(final)
        self.Shots = int(shots)
        self.Hits = int(hits)
        self.TOA = datetime.strptime(toa, '%I:%M' )
        self.PIM = int(pim)
        self.PowerPlay = float(pp.strip('%'))/100
        self.PenaltyKill = float(pk.strip('%'))/100
        self.FaceOffsWon = float(fow.strip('%'))/100
        
        
    
class SeasonStats:
    
    
    def __init__(self, player_ID, player_name):
        self.PID = player_ID
        self.Name = player_name
        self.URL = Config.GetPlayerURL(self.PID)
        
        self.Columns = ['PlayerID', 'PlayerName', 'Season', 'SeasonType', 'Position', 'GamesPlayed', 'Goals', 'Assists', 'Points', 'PIM', 'Hits', 'Shots', 'GameWinningGoals', 'FaceOffPercent', 'PlusMinus', 'Corsi', 'Wins', 'Losses', 'OvertimeLosses', 'WinPercentage', 'Salary']

        self.DataTypes = {'PlayerID' : 'int64', 'PlayerName' : 'str', 'Season' : 'str', 'SeasonType' : 'bool', 'Position' : 'str', 'GamesPlayed' : 'int64', 'Goals' : 'int64', 'Assists' : 'int64', 'Points' : 'int64', 'PIM' : 'int64', 'Hits' : 'int64', 'Shots' : 'int64', 'GameWinningGoals' : 'int64', 'FaceOffPercent' : 'float', 'PlusMinus' : 'int64', 'Corsi' : 'float', 'Wins' : 'int64', 'Losses' : 'int64', 'OvertimeLosses' : 'int64', 'WinPercentage' : 'float', 'Salary' : 'int64'}

        self.Stats = pd.DataFrame(columns = self.Columns)
        self.Stats = self.Stats.astype(dtype = self.DataTypes)

        # Figure out how to get the MultiIndex to work
#        self.Stats.index = pd.MultiIndex(levels=[[],[],[],[]], codes=[[],[],[],[]], names=[u'PlayerID', u'Season', u'SeasonType', u'Position'])
#        self.Stats.set_index(['PlayerID', 'Season', 'SeasonType', 'Position'], inplace=True, drop=True)



    def GetStats(self):
        for k in Positions:
            if (k == Positions.Skater):
                continue
            #self.GetStatsByPosition(k)
            self.GetStuffTest(k)

    def GetStuffTest(self, position):
        print(position)
        print(type(position))

        
    def GetStatsForCenter(self):
        log.info('Under Construction')
    
    def GetStatsForWing(self):
        log.info('Under Construction')
        
    def GetStatsForDefense(self):
        log.info('Under Construction')
        
    def GetStatsForGoalie(self):
        log.info('Under Construction')
        
        
        
        
    def GetStatsByPosition(self, position):
        if (position == Positions.Center):
            url = self.URL + '&filter_pos=center'
        elif (position == Positions.Wing):
            url = self.URL + '&filter_pos=wing'
        elif (position == Positions.Defense):
            url = self.URL + '&filter_pos=defense'
        elif (position == Positions.Goalie):
            url = self.URL + '&filter_pos=goalie'
        else:
            log.warning('Position entered that is not in the Config.Positions ENUM')
        
        soup = Config.GetHTMLSoup(url)
        tags = soup.find_all(class_ = "table_1")[0]
        
        #loop through all tags
        for index, tag in enumerate(tags):

            #clean all variables
            eligible = False
            
            #skip all empty tags
            if(tag != '\n'):

                log.info('Tag #%s - Length = %s' % (index, len(tag)))

                #only grab the first detailed contents and size
                row = tag.contents[1].get_text().splitlines()
                rowlen = len(row)

                log.info('Row Length = %s' % (len(row)))
                log.info(row)


                #find their position
                if (rowlen == 1 and 'Statistics' in row[0]):

                    #Get their position
                    pos = row[0].replace(' Statistics', '')

                elif (rowlen >= 20 and 'Season' in row[2]):
                    log.info('Season Eligible')
                    eligible = True
                    season = row[2][7:]
                    SeasonType = 'Regular'
                    gp = row[5]
                    g = row[6]
                    a = row[7]
                    pim = row[9]
                    hits = row[10]
                    shots = row[11]
                    gwg = row[12]
                    fop = row[13]
                    pm = row[14]
                    corsi = row[15]
                    w = row[16]
                    l = row[17]
                    otl = row[18]
                    sal = row[20].replace('$', '').replace(',', '')

                elif(rowlen >= 17 and 'Playoffs' in row[2]):
                    log.info('Playoff Eligible')
                    eligible = True
                    SeasonType = 'Playoff'
                    gp = row[4]
                    g = row[5]
                    a = row[6]
                    pim = row[7]
                    hits = row[8]
                    shots = row[9]
                    gwg = row[10]
                    fop = row[11]
                    pm = row[12]
                    corsi = row[13]
                    w = row[14]
                    l = row[15]
                    otl = row[16]
                    sal = sal
                
                elif(rowlen >= 19 and 'International' in row[2]):
                    log.info('International Eligible')
                    eligible = True
                    SeasonType = 'International'
                    gp = row[4]
                    g = row[5]
                    a = row[6]
                    pim = row[7]
                    hits = row[8]
                    shots = row[9]
                    gwg = row[10]
                    fop = row[11]
                    pm = row[12]
                    corsi = row[13]
                    w = row[14]
                    l = row[15]
                    otl = row[16]
                    sal = sal
                    
                else:
                    log.info('Not Eligible')

                if (eligible):
                    newSeasonStat = PlayerSeasonStat(self.PID, self.Name, pos, season, SeasonType, gp, g, a, pim, hits, shots, gwg, fop, pm, corsi, w, l, otl, sal)
                    row = pd.Series(newSeasonStat.ToList(), self.Columns)
                    self.Stats.loc[len(self.Stats)] = row
                    log.info(self.Stats)



#    def AppendStats(self, PlayerSeasonStat):
        
#         self.Stats.index = pd.MultiIndex(levels=[[],[],[],[]], codes=[[],[],[],[]], names=[u'PlayerID', u'Season', u'IsPlayoffs', u'Position'])
#        self.Stats.set_index(['PlayerID', 'Season', 'IsPlayoffs', 'Position'], inplace=True, drop=True)
        
        
#         print('Are the Stats empty? %s' % (self.Stats.empty))
#         if(self.Stats.empty):
#             print('Add initial row and then apply MultiIndex')
#             self.Stats.loc[len(self.Stats)] = row
#             self.Stats.set_index(['PlayerID', 'Season', 'IsPlayoffs', 'Position'], inplace=True, drop=True)
        
#         else:
#             print('Add subsequent rows')
#             self.Stats.loc[len(self.Stats)] = row




class PlayerSeasonStat:

    def __init__(self, PID, Name, Pos, Season, SeasonType, GP, G, A, PIM, Hits, Shots, GWG, FOPct, PlsMns, Corsi, W, L, OTL, Salary):
        try:
            self.PlayerID = PID
            self.PlayerName = Name
            self.Position = Pos
            self.Season = Season
            self.SeasonType = SeasonType
            self.GamesPlayed = int(GP)
            self.Goals = int(G)
            self.Assists = int(A)
            self.Points = self.Goals + self.Assists
            self.PIM = int(PIM)
            self.Hits = int(Hits)
            self.Shots = int(Shots)
            self.GameWinningGoals = int(GWG)
            self.FaceOffPercent = float(FOPct)
            self.PlusMinus = int(PlsMns)
            self.Corsi = float(Corsi)
            self.Wins = int(W)
            self.Losses = int(L)
            self.OvertimeLosses = int(OTL)
            self.WinPercentage = (2 * self.Wins + self.OvertimeLosses)/(2 * self.GamesPlayed)
            self.Salary = int(Salary)
        except:
            log.warning('Type Conversion failed for %s (%s)' % (self.PlayerName, self.PlayerID))


    def __iter__(self):
        yield self.PlayerID
        yield self.PlayerName
        yield self.Season
        yield self.SeasonType
        yield self.Position
        yield self.GamesPlayed
        yield self.Goals
        yield self.Assists
        yield self.Points
        yield self.PIM
        yield self.Hits
        yield self.Shots
        yield self.GameWinningGoals
        yield self.FaceOffPercent
        yield self.PlusMinus
        yield self.Corsi
        yield self.Wins
        yield self.Losses
        yield self.OvertimeLosses
        yield self.WinPercentage
        yield self.Salary

    def ToList(self):
        val = [self.PlayerID, self.PlayerName, self.Season, self.SeasonType, self.Position, self.GamesPlayed, self.Goals, self.Assists, self.Points, self.PIM, self.Hits, self.Shots, self.GameWinningGoals, self.FaceOffPercent, self.PlusMinus, self.Corsi, self.Wins, self.Losses, self.OvertimeLosses, self.WinPercentage, self.Salary]
        print(val)
        return val




class GameStat:
    log.info('Under Construction')
    
    
    