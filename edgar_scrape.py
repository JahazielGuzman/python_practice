from bs4 import BeautifulSoup
import json
import urllib2

"""
    This script obtains the names of each of the companies listed among 
    the ten pages of the edgar company listings site
"""


# the function get_company_names accepts main_url and num_pages as arguments. 
# It will open each of the num_pages pages under main_url and obtain the 
# company links 
def get_company_names(main_url, num_pages):
    
    # add the links for each company to the companies list
    companies = []

    for i in range(1,num_pages + 1):
        
        list_url = main_url + '/companies/?page=' + str(i)   # go to the i-th page of listings
        list_page = urllib2.urlopen(list_url)
        soup = BeautifulSoup(list_page.read())
        
        # the links to each companies details are stored in <a> tags under a <table>
        # with the class "table table-hover"

        company_links = soup.find('table', attrs={'class': 'table table-hover'})
        company_links = company_links.find_all('a')
        
        # get the links for each <a> tag
        companies += [link.get('href') for link in company_links]
        
    return companies


# the function get_company_details accepts main_url (a string) and companies (a list)
# as arguments. main_url is the website where company listings are located and companies
# is a list of company urls. This function will obtain the company details listed under
# each company url, add them to the company_json dictionary and then return the dictionary
def get_company_details(main_url, companies):

    company_json = {}
    
    for company_url in companies:
        
        curr_company = main_url + company_url.replace(' ','%20') # correct url's with spaces so they are usable
        company_page = urllib2.urlopen(curr_company)
        soup = BeautifulSoup(company_page.read())
    
        # the company details are stored under a <table> with the class 'table table-hover'
        # and each detail is stored under a <td>
        company_details = soup.find('table', attrs={'class': 'table table-hover'})
        company_details = soup.find_all('td')
        
        # the first company detail is the company name that will be used to index
        # a subdictionary containing further details for that company
        company_name = str(company_details[1].get_text())
        company_json[company_name] = {}
        
        company_details = company_details[2:] # remove the company name and get further details
        num_details = len(company_details)
        
        # The detail labels are stored in odd numbered <td>'s while the even
        # numbered <td>'s contain the actual data, process them pairwise as detail_label
        # and detail_content respectively, and store them in the sub-dictionary for the current company
        for i in range(0,num_details - 2,2):
            
            detail_label = str(company_details[i].find('b').get_text())
            detail_content = company_details[i+1].get_text()  

            # keep track of company details
            company_details[i] = detail_label
            company_details[i+1] = detail_content
            
            company_json[company_name][detail_label] = detail_content
        
    return company_json


# The main function will first obtain the number of pages in main_url
# and will call the get_company_names and get_company_details functions.
# main will then convert the dictionary containing company details
# to a json string and store it in the file solution.json
def main():
    
    main_url = 'http://data-interview.enigmalabs.org'
    
    page = urllib2.urlopen(main_url)
    soup = BeautifulSoup(page.read())
    
    # The maximum page number is stored in the second to last <a> tag
    pages = soup.find('ul', attrs={'class': 'pagination pagination-sm'})
    pages = pages.find_all('a')[-2]
    num_pages = int(pages.get_text())
    
    companies = get_company_names(main_url, num_pages)
    companies_json = get_company_details(main_url, companies)
    companies_json = json.dumps(companies_json)

    with file("solution.json", 'w') as solution_json:
        solution_json.write(companies_json)

# if script is run from the command linef -=
if __name__ == '__main__':
    main()
