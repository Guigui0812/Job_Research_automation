import requests
import scrapy 
import json
from datetime import datetime, timedelta
import re
import utils



    

def get_indeed_jobs(titre, lieu, type_contrat): 

#https://fr.indeed.com/emplois?q=Devops&l=%C3%8Ele-de-France&sc=0kf%3Ajt%28apprenticeship%29%3B&vjk=86859d0572ed98b7


    # The first character of strings is always a majuscule
    titre = titre.capitalize()
    type_contrat = type_contrat.capitalize()
    lieu = lieu.capitalize()
    page = 0

    url = "https://fr.indeed.com/emplois?q=" + titre + "&l=" + lieu + "&sc=0kf%3Ajt%28" + type_contrat + "%29%3B&start=" + str(page) + "&ppvjk=86859d0572ed98b7"

    print(url)


get_indeed_jobs("devops", "ile de france", "apprenticeship")