

class Crawler:
    def __init__(self):
        pass

    def push_to_queue(self, **kwargs):
        pass

    def retrieve(self,**kwargs):
        pass


class GdeltsCrawler(Crawler):
    def __init__(self):
        super().__init__()

    def retrieve(self, **kwargs):
        """
        kwargs should include:
        - time span or          Timespan
        - start and end date    StartDate EndDate
        - list of events        [Events] | Event 
         
        """
        self.mode = kwargs['mode'] if 'mode' in kwargs else 'artlist'
        self.maxrecords = kwargs['maxrecords'] if 'maxrecords' in kwargs else 250
        self.format = kwargs['format'] if 'format' in kwargs else 'json'
        self.timespan = kwargs['timespan'] if 'timespan' in kwargs else '72h'
        self.eng = kwargs['eng'] if 'eng' in kwargs else 'eng'
        self.sort = kwargs['sort'] if 'sort' in kwargs else 'datedesc'

        BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

        params = {
            "query":          kwargs['query'],
            "mode":           self.mode,          # list of articles
            "maxrecords":     self.maxrecords,                # 250 is the absolute max
            "format":         self.format,
            'timespan':       self.timespan,           # Last 30 days
            "sourcelang":     self.eng,              # remove for multilingual
            "sort":           self.sort          # newest first
        }

        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        

    
        