from pip import main


from googlesearch import search
import pandas as pd
import time
import sys
import os
sys.path.append(os.getcwd()) #"D:\\aa_projet\\python web scraping"
import backend_methods as scraper

######
# default args :

search_query = "web scraping"
website_query = "python"
language = "en"
search_nbr = 10
delay = 2