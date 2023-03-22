from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import threading

# Create a class to scrap the research result from indeed
class IndeedJobsScraper():

    def __init__(self, titre, lieu, type_contrat):
        
        self.titre = titre.capitalize()
        self.lieu = lieu.capitalize()
        self.type_contrat = type_contrat
        self.page = 0
        self.scrap = True
        self.url = "https://fr.indeed.com/emplois?q=" + titre + "&l=" + lieu + "&sc=0kf%3Ajt%28" + type_contrat + "%29%3B&start=" + str(self.page)
        self.url = self.url.replace(' ', '+')
        self.jobs_list = []

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)

    def run_scrap_research_result(self):

        while self.scrap:

            if (self.scrap_result_page() == True):
                self.page += 10 # les pages sur indeed sont de 10 en 10
            else:
                self.scrap = False
                self.driver.quit()

    def scrap_job_details(self, details_url, cpt):
 
        self.driver.get(details_url)

        # Wait for the page to load
        self.driver.implicitly_wait(5)

        # Get the job title
        h1 = self.driver.find_element(By.CSS_SELECTOR, "h1.jobsearch-JobInfoHeader-title")
        job_title = h1.text


        self.jobs_list[cpt - 1]["job_title"] = job_title

    def scrap_result_page(self):

        self.driver.get(self.url)
        print(self.url)

        # Wait for the page to load
        self.driver.implicitly_wait(5)

        # Get the job title and the url
        elements = self.driver.find_elements(By.CSS_SELECTOR, "a.jcs-JobTitle")

        print(len(elements))

        for element in elements:
                
                job = {
                    "url": element.get_attribute("href")
                }
    
                self.jobs_list.append(job)

        # get span that contains the company name
        elements = self.driver.find_elements(By.CSS_SELECTOR, "span.companyName")

        print(len(elements))

        for element in elements:
            self.jobs_list[elements.index(element)]["company"] = element.text

        cpt = 1

        for job in self.jobs_list:
            self.scrap_job_details(job["url"], cpt)
            cpt += 1
    
job_scraper = IndeedJobsScraper("Devops", "Île-de-France", "apprenticeship")
job_scraper.run_scrap_research_result()