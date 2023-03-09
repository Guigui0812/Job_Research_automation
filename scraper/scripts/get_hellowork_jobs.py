import requests
import scrapy 
import json
from datetime import datetime, timedelta
import re
import utils
# Add a header to the request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'}

# Global variables
status_code = 0
jobs = []

db_connection = utils.MongoDbInterface("localhost", 27017, "job_db", "hellowork_jobs")

# Function to add the job on the website to the jobs list
def scrap_basic_job_data(a, href, span):

    # Loop through the list of job title
    for i in range(len(a)):

        # Get the date
        date = span[i].css('::text').get()

        # clean the string
        date = utils.DataCleaner.clean_data(date)

        # Remove the white spaces at the beginning and at the end of the string
        date = date.strip()
        
        # if date match the pattern dd/mm/yyyy
        if re.match(r'\d{2}/\d{2}/\d{4}', date):
        
            # convert the date to a datetime object
            date = datetime.strptime(date, '%d/%m/%Y')

            # Check if the date is between today and 1 month ago
            if (date >= datetime.today() - timedelta(days=30)) and (date <= datetime.today()):

                # Clean the string
                a[i] = utils.DataCleaner.clean_data(a[i])
        
                # Delete the \n character
                a[i] = a[i].replace('\n', '')

                # Delete white spaces at the beginning and at the end of the string
                a[i] = a[i].strip()

                # Create a json object with the title and the url
                job = { "title": a[i], "date": str(date) , "url": href[i] }
                jobs.append(job)
    
# Function to get the research result
def scrap_research_result(url):

    # Get the page
    response = requests.get(url, headers=headers)
    status_code = response.status_code

    # If the status code is 200
    if status_code == 200 :   
        source = response.text

        if source:

            # Create a selector
            selector = scrapy.Selector(text=source)

            # Get the h2 element with the id "noResult" and get the text, and print it
            no_result = selector.css('h2#noResult::text').get()
            if no_result :
                return False

            # Get the ul with the class "crushed"
            ul = selector.css('ul.crushed')

            # Get all the li elements inside the ul
            li = ul.css('li')

            # get all h3 elements inside the li with the class "!tw-mb-0"
            h3 = li.css('h3.\!tw-mb-0')

            # get all the a elements inside the h3
            a = h3.css('a::text').getall()

            # get href attribute of the a elements inside the h3
            href = h3.css('a::attr(href)').getall()

            # Get all span with the attribute data-cy="publishDate"
            span = li.css('span[data-cy="publishDate"]')

            # Add the job to the jobs list
            scrap_basic_job_data(a, href, span)

            # Get the job description
            scrap_job_description()

            # Check if the job is already in the database
            for job in jobs:

                if db_connection.exists(job["idoffer"]):
                    jobs.remove(job)

            # Insert the jobs in the database
            db_connection.insert_many(jobs)

            return True

    else:
        return False

# Function to get the job title
def scrap_job_description():

    for job in jobs:

        # page url
        url = "https://www.hellowork.com" + job["url"]
        
        # Get the page
        response = requests.get(url, headers=headers)
        status_code = response.status_code

        # If the status code is 200
        if status_code == 200 :   
            source = response.text

            if source:

                # Create a selector
                selector = scrapy.Selector(text=source)

                # Get section with the attribute data-job-description
                section = selector.css('section[data-job-description]')

                # Get the json object
                json_object = section.attrib['data-job-description']

                # Convert the json object to a python object
                json_object = json.loads(json_object)

                # Get the company name
                company = json_object["company"]

                # Get idoffer from the json object
                idoffer = json_object["idoffer"]

                # Add the idoffer to the json object
                job["idoffer"] = idoffer

                # Get the text of all p elements inside the section
                content = section.css('p::text').getall()

                # add the company name to the json object
                job["company"] = company

                # Concatenate all the text of the p elements to a string separated by a space
                content = ' '.join(content)

                # Clean the string
                content = utils.DataCleaner.clean_data(content)

                # Delete the \n character
                content = content.replace('\n', '')

                # Delete white spaces at the beginning and at the end of the string
                content = content.strip()

                # add the content to the json object
                job["content"] = content

# Function to get devops job from hellowork
def scrap_job_research(url):

    # Variables
    run_scrap = True
    page = 1

    while run_scrap:

        # Get the research result
        if (scrap_research_result(url + str(page)) == True):
            page += 1
        else:
            run_scrap = False

# Function to get the job from hellowork
def get_jobs(job, location, contract, distance):
    
    url = "https://www.hellowork.com/fr-fr/emploi/recherche.html?k=" + job + "&l=" + location + "&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fregion%2F11&ray=" + str(distance) + "&d=all&c=" + contract + "&p="

    # replace spaces with +
    url = url.replace(' ', '+')
    
    # The first character of strings is always a majuscule
    job = job.capitalize()
    contract = contract.capitalize()
    location = location.capitalize()

    # Get devops engineer job from hellowork
    scrap_job_research(url)

get_jobs("devops", "Paris", "Alternance", 50)