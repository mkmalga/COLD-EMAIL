#import sqlite3
#print(sqlite3.sqlite_version)
'''import requests
from bs4 import BeautifulSoup

def scrape_jobs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    # Adjust the selectors based on the website structure
    for job in soup.find_all('div', class_='current-openings-main-div'):
        title = job.find('h3').text if job.find('h3') else "No title"
        link = job.find('a')['href']
        description = job.find('p').text
        jobs.append({'title': title, 'link': link, 'description': description})
    
    return jobs

# Test the function
careers_url = "https://modak.com/current-openings/"
print(scrape_jobs(careers_url))'''

'''from selenium import webdriver
from selenium.webdriver.common.by import By

def selenium_scrape(url):
    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed
    driver.get(url)
    jobs = []

    # Adjust the selectors based on the website structure
    job_elements = driver.find_elements(By.CLASS_NAME, 'current-openings-main-div')  # Replace with actual class
    for job in job_elements:
        title = job.find_element(By.TAG_NAME, 'h2').text if job.find_element(By.TAG_NAME,'h2') else "No title"
        link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
        description = job.find_element(By.TAG_NAME, 'p').text
        jobs.append({'title': title, 'link': link, 'description': description})
    
    driver.quit()
    return jobs

careers_url = "https://modak.com/current-openings/"
print(selenium_scrape(careers_url))'''

import requests
from bs4 import BeautifulSoup

def scrape_jobs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}. HTTP Status Code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    # Try different approaches to extract job-related information
    potential_job_containers = soup.find_all(['div', 'section', 'li', 'a'])  # Search for broader tags
    for container in potential_job_containers:
        title = None
        description = None
        link = None

        # Look for job titles
        title_tag = container.find(['Openings', 'job','Application','Carrers'])  # Common title tags
        if title_tag:
            title = title_tag.get_text(strip=True)

        # Look for job descriptions
        description_tag = container.find('p')  # Paragraphs for descriptions
        if description_tag:
            description = description_tag.get_text(strip=True)

        # Look for job links
        link_tag = container.find('a', href=True)
        if link_tag:
            link = link_tag['href']
            if not link.startswith('http'):
                link = requests.compat.urljoin(url, link)  # Handle relative URLs

        # Add to the job list if it looks like a valid job posting
        if title !=None and description != None and link != None:
            jobs.append({'title': title, 'description': description, 'link': link})

    return jobs

# Test the function
careers_url = "https://www.google.com/about/careers/applications/"
job_listings = scrape_jobs(careers_url)
for job in job_listings:
    print(job) 
    
