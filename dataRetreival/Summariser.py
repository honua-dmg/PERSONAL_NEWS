from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import logging 
logging.basicConfig(
    level=logging.ERROR,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='summariser_errors.log',  # Log file name
    filemode='a'  # Append mode, so logs aren't overwritten
)

class Summariser():
    def __init__(self):
        pass
    
    def summarize(self, text, sentences_count=3):
        pass

class SumySummariser(Summariser):
    def __init__(self):
        pass
    
    def summarize(self, text, sentences_count=3):
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, sentences_count)
            return " ".join([str(sentence) for sentence in summary])
        except:
            logging.error("Error-summarization: ", text)
            return None