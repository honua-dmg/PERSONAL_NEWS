## TODO:
# - create an agent to crawl and retrieve articles from GDELT without needing a specific query

import requests
import pandas as pd
import trafilatura
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import logging
logging.basicConfig(
    level=logging.ERROR,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='crawler_errors.log',  # Log file name
    filemode='a'  # Append mode, so logs aren't overwritten
)
pd.set_option('display.max_colwidth', None)

class Crawler:
    def __init__(self):
        pass

    def push_to_queue(self, **kwargs):
        """
        kwargs should include:
        - time span or          Timespan
        - start and end date    StartDate EndDate
        - list of events        [Events] | Event 
         
        """
        pass

    def retrieve(self,**kwargs):
        pass




class GdeltsCrawler(Crawler):
    def __init__(self):
        super().__init__()
        self.article_hash = {}

    def retrieve(self, **kwargs):
        """
        kwargs should include:
        - time span or          Timespan
        - start and end date    StartDate EndDate
        - list of events        [Events] | Event 
         
        """
        self.mode = kwargs.get('mode', 'artlist')
        self.maxrecords = kwargs.get('maxrecords', 250)
        self.format = kwargs.get('format', 'json')
        self.timespan = kwargs.get('timespan', '72h')
        self.eng = kwargs.get('sourcelang', 'eng')
        self.sort = kwargs.get('sort', 'datedesc')

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
            data =  pd.DataFrame(response.json()['articles'])
            return data[data['language']=="English"]
        else:
            logging.error("Error-retrieval: ",kwargs['query'] )

            return None
        
    def extract_text(self, url):
        if url in self.article_hash:
            return self.article_hash[url]

        downloaded = trafilatura.fetch_url(url)
        try:
            self.article_hash[url] = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
            return self.article_hash[url] # avoids re-downloading the same article
        except:
            logging.error("Error-text-extraction: ", url)
            return None
    
    def summarize_text(self, text):
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, sentences_count)
            return " ".join([str(sentence) for sentence in summary])
        except:
            logging.error("Error-summarization: ", text)
            return None

    def push_to_queue(self, **kwargs):
        pass

    
        