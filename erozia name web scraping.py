#!/usr/bin/env python
# coding: utf-8

# In[2]:


#get_ipython().system('pip install beautifulsoup4')


# In[3]:


#get_ipython().system('pip install google')


# In[4]:


try:
	from googlesearch import search
except ImportError:
	print("No module named 'google' found")


# In[5]:


import pandas as pd


# In[6]:


server_list = []


# In[7]:


#https://www.freecodecamp.org/news/python-unique-list-how-to-get-all-the-unique-values-in-a-list-or-array/
def get_unique_urls(urls):

    list_of_unique_urls = []

    unique_urls = set(urls)

    for url in unique_urls:
        list_of_unique_urls.append(url)

    return list_of_unique_urls


# In[8]:


query = "serveurs minecraft français"

for string in search(query, lang="fr", num=10, stop=50):
    slash_number = 0
    newstring = ""
    for i in string:
        newstring += i
        if i == "/":
            slash_number += 1
        if slash_number >= 3:
            #print(newstring)
            server_list.append(newstring)              
            break

server_list = get_unique_urls(server_list)
server_list


# In[9]:


erozia_list = []

for url in server_list:
    query = "site:"+url+" \"erozia\""
    #print(query)
    
    for result in search(query, lang="fr", num=10, stop=3):
        erozia_list.append(result)

erozia_list = get_unique_urls(erozia_list)


# In[ ]:


erozia_list


# In[ ]:


backup_erozia_list = erozia_list


# In[ ]:


erozia_list.remove("https://www.facebook.com/erozia.ramos.1")


# In[ ]:


erozia_list.remove( 'https://www.facebook.com/people/Erozia-Azahra-Caelina/100021212049114/')


# In[ ]:


erozia_list.remove("https://www.facebook.com/erozia.dacosta.3")
erozia_list.remove("https://dictionnaire.reverso.net/allemand-francais/erozia")


# In[ ]:


erozia_list


# In[ ]:


df = pd.DataFrame(erozia_list)
df.to_csv("erozia_list.csv")


# In[ ]:




