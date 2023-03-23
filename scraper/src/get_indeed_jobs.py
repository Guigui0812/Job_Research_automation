from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import utils
import json
import datetime
import re

# Create a class to scrap the research result from indeed
class IndeedJobsScraper():

    def __init__(self, titre, lieu, type_contrat, limit, max_publish_days=25):
        
        self.titre = titre.capitalize()
        self.lieu = lieu.capitalize()
        self.type_contrat = type_contrat
        self.page = 0
        self.limit = limit * 10
        self.scrap = True
        self.url = "https://fr.indeed.com/emplois?q=" + titre + "&l=" + lieu + "&sc=0kf%3Ajt%28" + type_contrat + "%29%3B&start=" + str(self.page)
        self.url = self.url.replace(' ', '+')
        self.jobs_list = []
        self.max_publish_days = max_publish_days

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


    def scrap_job_details(self, details_url, job_cpt):
 
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

        self.jobs_list[job_cpt - 1]["title"] = utils.DataCleaner.clean_data(job_title)
        self.jobs_list[job_cpt - 1]["location"] = utils.DataCleaner.clean_data(job_location)
        self.jobs_list[job_cpt - 1]["description"] = utils.DataCleaner.clean_data(job_description)

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

        # get span that contains the job publication date
        elements = self.driver.find_elements(By.CSS_SELECTOR, "span.date")        

        for element in elements:
             
            # Algorithm to get the date of publication of the job in the different cases
            # - If the job is published today : the text is "Aujourd'hui" or "Publié à l'instant"
            # - If the job is published less than 30 days ago : the text is "il y a x jours"
            # - If the job is published more than 30 days ago : the text is "il y a plus de 30 jours"

            try:
                # Regex to check if the text contains a digit
                if re.search(r'\d', element.text):
                    nb_jours = element.text.split(" ")[5]
                    
                    if nb_jours.isdigit():
                        nb_jours = int(nb_jours)
                        today = datetime.datetime.today()
                        nb_jours = today - datetime.timedelta(days=nb_jours)
                        nb_jours = nb_jours.strftime("%d/%m/%Y")
                        self.jobs_list[elements.index(element)]["date"] = nb_jours

                    else :
                        self.jobs_list[elements.index(element)]["date"] = "Older than 30 days"

                elif element.text == "Aujourd'hui" or element.text == "Publié à l'instant":

                    today = datetime.datetime.today()
                    nb_jours = today.strftime("%d/%m/%Y")
                    self.jobs_list[elements.index(element)]["date"] = nb_jours

            except:
                # If the job can't be parsed, the date is set to today by default (to avoid errors and missing jobs)
                self.jobs_list[elements.index(element)]["date"] = datetime.datetime.today().strftime("%d/%m/%Y")

        for job in self.jobs_list:

            print(job["date"])

            if job["date"] == "Older than 30 days":
                self.jobs_list.remove(job)
            else:
                
                date = datetime.datetime.strptime(job["date"], "%d/%m/%Y")
                max_date = datetime.datetime.today() - datetime.timedelta(self.max_publish_days)

                if date < max_date:
                    self.jobs_list.remove(job)

        job_cpt = 1

        for job in self.jobs_list:
            self.scrap_job_details(job["url"], job_cpt)
            job_cpt += 1
            time.sleep(3)
    
job_scraper = IndeedJobsScraper("Devops", "Île-de-France", "apprenticeship", 2)
job_scraper.run_scrap_research_result()

# print the result as a json
for job in job_scraper.jobs_list:
    job = json.dumps(job, indent=4, sort_keys=True, default=str, ensure_ascii=False).encode('utf8')
    print(job.decode())

job_scraper.store_jobs()

#utils.DataCleaner.delete_old_jobs()