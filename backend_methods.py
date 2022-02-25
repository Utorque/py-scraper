from googlesearch import search,get_random_user_agent
import pandas as pd
import time
import os
import sys
sys.path.append("C:\\Users\\barth\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages")

#https://www.freecodecamp.org/news/python-unique-list-how-to-get-all-the-unique-values-in-a-list-or-array/
def get_unique_urls(urls):

    list_of_unique_urls = []

    unique_urls = set(urls)

    for url in unique_urls:
        list_of_unique_urls.append(url)

    return list_of_unique_urls


#returns a list of all google websites that will be searched

#TODO : fonction pour que au lieu de search directement, try et except error 429 too many requests
#TODO : faire le get_random_user_agent ici et non dans la librairie googlesearch pour pouvoir publier + facilement

def get_website_to_scrap(query,language="fr",search_nbr=20,delay=3.0):
    print("Preparation...")
    time.sleep(1) #helps avoiding IP block from google :,)
    estimated_process_time = search_nbr*delay #totalement théorique :
    print(f"Estimated website searching process time : {estimated_process_time} s.")
    print("Beginning website search.")
    website_list = []
    nbr_query = 0
    print("Beginning query "+str(nbr_query)+".")
    for website in search(query=query,tld="ch", lang=language, pause=delay,stop=search_nbr,user_agent=get_random_user_agent()):
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
    return get_unique_urls(website_list) #retourne la liste avec que des urls uniques

#returns a DataFrame of urls in designated website by searching exact occurencies of the query
def exact_term_website_scrap(query, website_list, language="fr",search_nbr=3,delay=2.0,create_csv=False):
    print("Preparation...")
    time.sleep(1) #helps avoiding IP block from google :,)
    estimated_process_time = len(website_list)*search_nbr*delay #totalement théorique
    print(f"Estimated website scrap process time : {estimated_process_time} s.")
    print("Beginning website scrapping.")

    response_list = []
    nbr_query = 0
    for url in website_list:
        print("Beginning query "+str(nbr_query)+".")
        new_query = "site:"+url+" \""+query+"\""
        print(f"query : {new_query}")
        
        if search(query=new_query,tld="ch", lang=language, stop=search_nbr,pause=delay,user_agent=get_random_user_agent()):
            time.sleep(delay)
            for result in search(query=new_query,tld="ch", lang=language, stop=search_nbr,pause=delay,user_agent=get_random_user_agent()):
                response_list.append(result)
                print("Query "+str(nbr_query)+" complete.")
                nbr_query += 1
                time.sleep(delay)
            else:
                print(f"No result for query {new_query}")
                nbr_query += 1
            
    response_list = get_unique_urls(response_list)

    if create_csv == True:
        df = pd.DataFrame(response_list)
        df.to_csv(str(query)+"-"+time.localtime+".csv")

    return response_list


if __name__ == "__main__":
    print("Debug as main.")



    website_query = "minecraft server" #input("Infos about websites you want to search in : ")
    search_query = "minevolution" #input("Exact term you want to search : ")

    search_delay = 2

    weblist = get_website_to_scrap(query=website_query,delay=search_delay,search_nbr=10)
    print(weblist)
    search_results = exact_term_website_scrap(query=search_query,website_list=weblist,delay=search_delay)
    print(search_results)

    os.system("pause")