from Config import Config


class Season:
    
    
    SeasonNumber = -1
    
    def __init__(self):
        self.SeasonNumber = self.GetSeason()
        
        
    def GetSeason(self):
        soup = Config.GetHTMLSoup(Config.URL_roster)
        self.SeasonNumber = -1
        for x in soup.find_all('option'):
            val = int(x.get('value'))
            sn = max(val, self.SeasonNumber)
        return sn