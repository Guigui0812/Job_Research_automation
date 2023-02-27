import requests
import scrapy 
import json

def clean_string(string):
    
        # Replace special characters by their no special characters equivalent
        string = string.replace('é', 'e')
        string = string.replace('è', 'e')
        string = string.replace('ê', 'e')
        string = string.replace('à', 'a')
        string = string.replace('â', 'a')
        string = string.replace('ô', 'o')
        string = string.replace('î', 'i')
        string = string.replace('ï', 'i')
        string = string.replace('ç', 'c')
        string = string.replace('ù', 'u')
        string = string.replace('û', 'u')
        
        return string


# Add a header to the request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'}

status_code = 0
page = 1
run_scrap = True
jobs = []

# Get the page while the status code is 200
while run_scrap == True:

    # page url
    url = "https://www.hellowork.com/fr-fr/emploi/recherche.html?k=DevOps&k_autocomplete=http%3A%2F%2Fwww.rj.com%2FCommun%2FPost%2FDevops&l=%C3%8Ele-de-France&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fregion%2F11&c=Alternance&ray=50&p=" + str(page)
    
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
                run_scrap = False

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

            # print the href attribute and the text of the a elements
            for i in range(len(a)):

                # Clean the string
                a[i] = clean_string(a[i])
          
                # Delete the \n character
                a[i] = a[i].replace('\n', '')

                # Delete white spaces at the beginning and at the end of the string
                a[i] = a[i].strip()

                # Create a json object with the title and the url
                job = { "title": a[i], "url": href[i] }
                jobs.append(job)

            # Update the page number
            page += 1

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

            # Get text of attribute "company" of the attribute "data-job-description"
            company = section.css('section[data-job-description]::attr(company)').get()

            # Get the text of all p elements inside the section
            content = section.css('p::text').getall()

            # Clean the string
            print(company)

            # add the company name to the json object
            job["company"] = company

            for element in content:
                element = clean_string(element)

            # Concatenate all the text of the p elements to a string separated by a space
            content = ' '.join(content)

            # add the content to the json object
            job["content"] = content

print(json.dumps(jobs, indent=4))