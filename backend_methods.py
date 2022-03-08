from cgi import print_directory
from random import random
from unittest import result
from googlesearch import search
import pandas as pd
import time
import os
import sys
import random
sys.path.append("C:\\Users\\barth\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages")

#https://www.freecodecamp.org/news/python-unique-list-how-to-get-all-the-unique-values-in-a-list-or-array/
def _get_unique_urls(urls):

    list_of_unique_urls = []

    unique_urls = set(urls)

    for url in unique_urls:
        list_of_unique_urls.append(url)

    return list_of_unique_urls


def _get_random_user_agent():
    user_agent_list = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)'
    ]
    return random.choice(user_agent_list)


#returns a list of all google websites that will be searched

#TODO : fonction pour que au lieu de search directement, try et except error 429 too many requests
#TODO : éviter les pages not found
#TODO : chercher (récursivement ?) dans les liens pour aller le plus loin possible et trouver plus précisément les pages

def get_website_to_scrap(query,language="en",search_nbr=20,delay=2.0):
    print("Preparation...")
    time.sleep(1) #helps avoiding IP block from google :,)
    estimated_process_time = search_nbr*delay #totalement théorique :
    print(f"Estimated website searching process time : {estimated_process_time} s.")
    print("Beginning website search.")
    website_list = []
    nbr_query = 0
    print("Beginning query "+str(nbr_query)+".")
    for website in search(query=query,tld="com", lang=language, pause=delay,stop=search_nbr,user_agent=_get_random_user_agent()):
        slash_number = 0 # la recerche retourne https://******.*/****/***/**. je compte les 3 premiers '/' et je jarte le reste 
        newWebsite = ""
        time.sleep(delay)
        for i in website: #je parcours le string website à la recherche des '/'
            newWebsite += i 
            if i == "/":
                slash_number += 1
            if slash_number >= 3: 
                #print(newWebsite)
                website_list.append(newWebsite) #le site sous forme https://****.**/ est append a la liste
                print("Query "+str(nbr_query)+" complete.")
                nbr_query += 1           
                break
    
    print("Successfully acquired a list of relevant website.")
    return _get_unique_urls(website_list) #retourne la liste avec que des urls uniques

#returns a DataFrame of urls in designated website by searching exact occurencies of the query
def exact_term_website_scrap(query, website_list, language="en",search_nbr=5,delay=2.0,create_csv=False):
    print("Preparation...")
    time.sleep(1) #helps avoiding IP block from google :,)
    estimated_process_time = len(website_list)*search_nbr*delay #totalement théorique
    print(f"Estimated website scrap process time : {estimated_process_time} s.")
    print("Beginning website scrapping.")

    response_list = []
    nbr_query = 0
    for url in website_list:
        new_query = "site:"+url+" \""+query+"\""
        print(f"Beginning query {nbr_query} : {new_query}")
        time.sleep(delay)
        if search(query=new_query,tld="com", lang=language, stop=search_nbr,pause=delay,user_agent=_get_random_user_agent()):
            time.sleep(delay)
            for result in search(query=new_query,tld="com", lang=language, stop=search_nbr,pause=delay,user_agent=_get_random_user_agent()):
                response_list.append(result)
                print("Query "+str(nbr_query)+" complete.")
                nbr_query += 1
            else:
                print(f"No result.")
                nbr_query += 1
            
    response_list = _get_unique_urls(response_list)

    df = pd.DataFrame({'URLs' : response_list})
    if create_csv == True:
        try:
            csv_name = f"{query}-{time.timezone}.csv"
            df.to_csv(csv_name)
        except:
            pass
        

    return df

#recherche simple
def simple_search(query, website="",search_nbr=5,language="en"):
    if website != "":
        new_query = f"site:{website}  \"{query}\""
    else:
        new_query = f"\"{query}\""
    result = search(query=new_query,lang=language,stop=search_nbr,user_agent=_get_random_user_agent())
    return result

def advanced_search(website_query,search_query, language="en",search_nbr=10,delay=2.0,create_csv=False):
    website_list = get_website_to_scrap(query=website_query,language=language,search_nbr=search_nbr,delay=delay)

    if len(website_list) == 0:
        print("No website to look found. If the process was far quicker than estimated, please try again later.")
        print("Otherwise, please make sure there is no mistake in your search terms, or be more general.")
        return        

    print(f"{len(website_list)} individual website founds.")

    result_df = exact_term_website_scrap(query=search_query,website_list=website_list,language=language,delay=delay,create_csv=create_csv)
    print(result_df)
    return result_df



if __name__ == "__main__":
    print("Debug as main.")

    website_query = "minecraft server" #input("Infos about websites you want to search in : ")
    search_query = "top.opblocks.com" #input("Exact term you want to search : ")
    search_delay = 1
    nbr_search = 10

    # weblist = get_website_to_scrap(query=website_query,delay=search_delay,search_nbr=10)
    # print(weblist)
    # search_results = exact_term_website_scrap(query=search_query,website_list=weblist,delay=search_delay)
    # print(search_results)

    advanced_search(website_query=website_query,search_query=search_query,search_nbr=nbr_search,delay=search_delay,create_csv=True)

    os.system("pause")