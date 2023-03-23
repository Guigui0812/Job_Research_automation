from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import utils
import json
import datetime

# Create a class to scrap the research result from indeed
class IndeedJobsScraper():

    def __init__(self, titre, lieu, type_contrat, limit, job_max_publish_date=25):
        
        self.titre = titre.capitalize()
        self.lieu = lieu.capitalize()
        self.type_contrat = type_contrat
        self.page = 0
        self.limit = limit * 10
        self.scrap = True
        self.url = "https://fr.indeed.com/emplois?q=" + titre + "&l=" + lieu + "&sc=0kf%3Ajt%28" + type_contrat + "%29%3B&start=" + str(self.page)
        self.url = self.url.replace(' ', '+')
        self.jobs_list = []
        self.job_max_publish_date = job_max_publish_date

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options)

    def run_scrap_research_result(self):

        while self.scrap:

            if (self.scrap_result_page() == True) and (self.page <= self.limit):
                self.page += 10 # les pages sur indeed sont de 10 en 10
            else:
                self.scrap = False
                self.driver.quit()

    def store_jobs(self):

        db_connection = utils.MongoDbInterface("localhost", 27017, "job_db", "hellowork_jobs")

        # Check if the job is already in the database
        for job in self.jobs_list:
            if db_connection.exists(job["id"]):
                self.jobs_list.remove(job)

        db_connection.insert_many(self.jobs_list)

        response = db_connection.get_all()
        
        # format the response to print it as a json
        for job in response:
            job = json.dumps(job, indent=4, sort_keys=True, default=str)
            print(job)


    def scrap_job_details(self, details_url, cpt):
 
        self.driver.get(details_url)

        # Wait for the page to load
        self.driver.implicitly_wait(5)

        # Get the job title
        h1 = self.driver.find_element(By.CSS_SELECTOR, "h1.jobsearch-JobInfoHeader-title")
        job_title = h1.text

        # Get the job location
        div = self.driver.find_element(By.CSS_SELECTOR, "div.eu4oa1w0")
        job_location = div.text

        # Get the job description
        div = self.driver.find_element(By.CSS_SELECTOR, "div.jobsearch-jobDescriptionText")
        job_description = div.text

        self.jobs_list[cpt - 1]["title"] = utils.DataCleaner.clean_data(job_title)
        self.jobs_list[cpt - 1]["location"] = utils.DataCleaner.clean_data(job_location)
        self.jobs_list[cpt - 1]["description"] = utils.DataCleaner.clean_data(job_description)

    def scrap_result_page(self):

        self.driver.get(self.url)
        print(self.url)

        # Wait for the page to load
        self.driver.implicitly_wait(5)

        # Get the job title and the url
        elements = self.driver.find_elements(By.CSS_SELECTOR, "a.jcs-JobTitle")

        for element in elements:
                
            job = {
                "id": element.get_attribute("id"),
                "url": element.get_attribute("href")
            }

            self.jobs_list.append(job)

        # get span that contains the company name
        elements = self.driver.find_elements(By.CSS_SELECTOR, "span.companyName")

        for element in elements:
            self.jobs_list[elements.index(element)]["company"] = element.text

        cpt = 1

        # get span that contains the job publication date
        elements = self.driver.find_elements(By.CSS_SELECTOR, "span.date")
        
        for element in elements:
             
            nb_jours = element.text.split(" ")[5]

            # Check if the job is published today or recently according to the number of days in the string
            # If the job is published today or recently, we get the current date
            # If the job is older than 30 days, we delete it from the list

            if nb_jours.isdigit():
                nb_jours = int(nb_jours)
                today = datetime.datetime.today()
                nb_jours = today - datetime.timedelta(days=nb_jours)
                nb_jours = nb_jours.strftime("%d/%m/%Y")
                self.jobs_list[elements.index(element)]["date"] = nb_jours

            elif element.text == "Aujourd'hui" or element.text == "Publié à l'instant":

                today = datetime.datetime.today()
                nb_jours = today.strftime("%d/%m/%Y")
                self.jobs_list[elements.index(element)]["date"] = nb_jours

            else: 
                # The job is older than 30 days
                self.jobs_list[elements.index(element)]["date"] = "Older than 30 days"

        # Delete the jobs that are older than the limit date
        for job in self.jobs_list:
            if job["date"] == "Older than 30 days":
                self.jobs_list.remove(job)
            elif job["date"] > self.job_max_publish_date:
                self.jobs_list.remove(job)

        # get the job details
        for job in self.jobs_list:
            self.scrap_job_details(job["url"], cpt)
            cpt += 1
            time.sleep(3)
    
job_scraper = IndeedJobsScraper("Devops", "Île-de-France", "apprenticeship", 2)
job_scraper.run_scrap_research_result()

# print the result as a json
print(job_scraper.jobs_list)

job_scraper.store_jobs()