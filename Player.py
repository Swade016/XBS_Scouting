import numpy
import pandas as pd
from Config import Config
from Config import Positions
from Config import log



class Player:
        
#    def player_url(player_id):
#        url_player_id = "%s;&player_id=%s" % (XBS.GetUrl('player'), str(player_id))
#        return url_player_id
                         
    def __init__(self, player_id, player_name):
        self.PID = player_id
        self.Name = player_name
        self.SeasonStats = SeasonStats()
    
    
    def Print(self):
        return '%s - %s' % (self.PID, self.Name)
    
    
    # THIS STILL NEEDS BUILT TO GET THEIR LEAGUE PREFERENCES
    def GetPlayerDetails(self):
        log.info("Extracting data for: %s (%s)" % (self.Name, self.PID))
        url_player = Config.GetPlayerURL(self.PID)
        soup = Config.GetHTMLSoup(url_player)
        return soup


    def GetSeasonStats(self):
        url = Config.GetPlayerURL(self.PID)
        for k in Positions:
            self.SeasonStats.GetSeasonStatsByPosition(k)

            
            

class SeasonStats:

    def __init__(self):
        self.Columns = ['PlayerID', 'PlayerName', 'Season', 'IsPlayoffs', 'Position', 'GamesPlayed', 'Goals', 'Assists', 'Points', 'PIM', 'Hits', 'Shots', 'GameWinningGoals', 'FaceOffPercent', 'PlusMinus', 'Corsi', 'Wins', 'Losses', 'OvertimeLosses', 'WinPercentage', 'Salary']

        self.DataTypes = {'PlayerID' : 'int64', 'PlayerName' : 'str', 'Season' : 'str', 'IsPlayoffs' : 'bool', 'Position' : 'str', 'GamesPlayed' : 'int64', 'Goals' : 'int64', 'Assists' : 'int64', 'Points' : 'int64', 'PIM' : 'int64', 'Hits' : 'int64', 'Shots' : 'int64', 'GameWinningGoals' : 'int64', 'FaceOffPercent' : 'float', 'PlusMinus' : 'int64', 'Corsi' : 'float', 'Wins' : 'int64', 'Losses' : 'int64', 'OvertimeLosses' : 'int64', 'WinPercentage' : 'float', 'Salary' : 'int64'}

        self.Stats = pd.DataFrame(columns = self.Columns)
        self.Stats = self.Stats.astype(dtype = self.DataTypes)

        # Figure out how to get the MultiIndex to work
#        self.Stats.index = pd.MultiIndex(levels=[[],[],[],[]], codes=[[],[],[],[]], names=[u'PlayerID', u'Season', u'IsPlayoffs', u'Position'])
#        self.Stats.set_index(['PlayerID', 'Season', 'IsPlayoffs', 'Position'], inplace=True, drop=True)



    def GetSeasonStatsByPosition(self, position):
        url = Config.GetPlayerURL(self.PID)
        if (position == Positions.Center):
            url += '&filter_pos=center'
        elif (position == Positions.Wing):
            url += '&filter_pos=wing'
        elif (position == Positions.Defense):
            url += '&filter_pos=wing'
        elif (position == Positions.Goalie):
            url += '&filter_pos=wing'
        else:
            url += '&filter_pos=all'  
        
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

                elif (rowlen == 21 and 'Season' in row[2]):
                    log.info('Season Eligible')
                    eligible = True
                    season = row[2][7:]
                    isPlayoffs = False
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

                elif(rowlen == 19 and 'Playoffs' in row[2]):
                    log.info('Playoff Eligible')
                    eligible = True
                    isPlayoffs = True
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
#                     print(type(self.PID))
#                     print(type(self.Name))
#                     print(type(pos))
#                     print(type(season))
#                     print(type(currentseason))
#                     print(type(isPlayoffs))
#                     print(type(gp))
#                     print(type(g))
#                     print(type(a))
#                     print(type(pim))
#                     print(type(hits))
#                     print(type(shots))
#                     print(type(gwg))
#                     print(type(fop))
#                     print(type(pm))
#                     print(type(corsi))
#                     print(type(w))
#                     print(type(l))
#                     print(type(otl))
#                     print(type(sal))
                    
                    newSeasonStat = PlayerSeasonStat(self.PID, self.Name, pos, season, isPlayoffs, gp, g, a, pim, hits, shots, gwg, fop, pm, corsi, w, l, otl, sal)
                    self.SeasonStats.AppendStats(newSeasonStat)
                    log.info(self.SeasonStats)



    def AppendStats(self, PlayerSeasonStat):
        row = pd.Series(PlayerSeasonStat, self.Columns)
        self.Stats.loc[len(self.Stats)] = row
#         self.Stats.index = pd.MultiIndex(levels=[[],[],[],[]], codes=[[],[],[],[]], names=[u'PlayerID', u'Season', u'IsPlayoffs', u'Position'])
        self.Stats.set_index(['PlayerID', 'Season', 'IsPlayoffs', 'Position'], inplace=True, drop=True)
        
        
#         print('Are the Stats empty? %s' % (self.Stats.empty))
#         if(self.Stats.empty):
#             print('Add initial row and then apply MultiIndex')
#             self.Stats.loc[len(self.Stats)] = row
#             self.Stats.set_index(['PlayerID', 'Season', 'IsPlayoffs', 'Position'], inplace=True, drop=True)
        
#         else:
#             print('Add subsequent rows')
#             self.Stats.loc[len(self.Stats)] = row


class PlayerSeasonStat:

    def __init__(self, PID, Name, Pos, Season, IsPlayoffs, GP, G, A, PIM, Hits, Shots, GWG, FOPct, PlsMns, Corsi, W, L, OTL, Salary):
        try:
            self.PlayerID = PID
            self.PlayerName = Name
            self.Position = Pos
            self.Season = Season
            self.IsPlayoffs = IsPlayoffs
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
        yield self.IsPlayoffs
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

    def __str__(self):
        return [[self.PlayerID, self.PlayerName, self.Season, self.IsPlayoffs, self.Position, self.GamesPlayed, self.Goals, self.Assists, self.Points, self.PIM, self.Hits, self.Shots, self.GameWinningGoals, self.FaceOffPercent, self.PlusMinus, self.Corsi, self.Wins, self.Losses, self.OvertimeLosses, self.WinPercentage, self.Salary]]
