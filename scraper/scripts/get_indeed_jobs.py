import requests
import scrapy 
import json
from datetime import datetime, timedelta
import re
import utils

def scrap_research_result(url):

    data =  "UnicodeEncodeError: 'latin-1' codec can't encode character '\u2026' in position 512: ordinal not in range(256)"
    data = data.encode()

    headers = { 
        'Host': 'fr.indeed.com',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
        'Accept': '*/*', 
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br', 
        'Referer': "https://fr.indeed.com/companies?from=gnav-homepage",
        'Alt-Used': 'fr.indeed.com', 
        'Connection': 'keep-alive'      
    }

    url = "https://fr.indeed.com/companies?from=gnav-homepage"

    # Get the page
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    print(status_code)

    # If the status code is 200
    if status_code == 200 :   
        source = response.text

        if source:

            print("je suis la")
            # Create a selector
            selector = scrapy.Selector(text=source)

            # Get get the div with class jobsearch-NoResult-rightPane
            no_result = selector.css('div.jobsearch-NoResult-rightPane')
            if no_result :
                return False

            # Get the ul with the class "jobsearch-ResultsList"
            ul = selector.css('ul.jobsearch-ResultsList')

            print(ul)
            
# Function to get the research result from indeed
def get_indeed_jobs(titre, lieu, type_contrat): 

    #https://fr.indeed.com/emplois?q=Devops&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=86859d0572ed98b7

    # The first character of strings is always a majuscule
    titre = titre.capitalize()
    type_contrat = type_contrat.capitalize()
    lieu = lieu.capitalize()
    page = 0
    run_scrap = True
    url = "https://fr.indeed.com/emplois?q=" + titre + "&l=" + lieu + "&sc=0kf%3Ajt%28" + type_contrat + "%29%3B&start=" + str(page)
    
    # replace spaces with +
    url = url.replace(' ', '+')

    while run_scrap:

        # Get the research result
        if (scrap_research_result(url) == True):
            page += 10
        else:
            run_scrap = False

get_indeed_jobs("devops", "ile de france", "apprenticeship")