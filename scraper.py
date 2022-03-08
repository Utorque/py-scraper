import tkinter as tk

import sys
import os
sys.path.append(os.getcwd()) #"D:\\aa_projet\\python web scraping"
import backend_methods as scraper

window = tk.Tk()
greeting = tk.Label(text="Google Scraper",width=50,height=2)
greeting.pack()

tk_website_qu = tk.Label(text="Website specification :")
tk_website_qu.pack()
tk_website_query = tk.Entry()
tk_website_query.pack()
website_query = tk_website_query.get()
print(website_query)

tk_search_qu = tk.Label(text="Main search :")
tk_search_qu.pack()
tk_search_query = tk.Entry()
tk_search_query.pack()


tk.Label(text=" ").pack()
window.mainloop()