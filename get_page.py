import requests
import scrapy 
import json

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

                # Replace special characters by their no special characters equivalent
                a[i] = a[i].replace('é', 'e')
                a[i] = a[i].replace('è', 'e')
                a[i] = a[i].replace('ê', 'e')
                a[i] = a[i].replace('à', 'a')
                a[i] = a[i].replace('â', 'a')
                a[i] = a[i].replace('ô', 'o')
                a[i] = a[i].replace('î', 'i')
                a[i] = a[i].replace('ï', 'i')
                a[i] = a[i].replace('ç', 'c')
                a[i] = a[i].replace('ù', 'u')
                a[i] = a[i].replace('û', 'u')
                
                # Delete the \n character
                a[i] = a[i].replace('\n', '')

                # Delete white spaces at the beginning and at the end of the string
                a[i] = a[i].strip()

                # Create a json object with the title and the url
                job = { "title": a[i], "url": href[i] }
                jobs.append(job)

            # Update the page number
            page += 1

# transform the list to json
jobs = json.dumps(jobs, indent=4)
print(jobs)