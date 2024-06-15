#  
# import requests
# from bs4 import BeautifulSoup
# import json
# import logging

# logging.basicConfig(filename='job_scraper.log', level=logging.DEBUG, 
#                     format='%(asctime)s %(levelname)s:%(message)s')

# def get_job_listings():
#     url = 'https://www.linkedin.com/jobs/search/?currentJobId=3949316904&f_TPR=r86400&geoId=102713980&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&spellCorrectionEnabled=true'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#     }
    
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print(f"Failed to retrieve job listings: {response.status_code}")
#         return []
#     soup = BeautifulSoup(response.content, 'html.parser')
#     try:
#         with open('./soup.html', 'w', encoding='utf-8') as file:
#             file.write(soup.prettify())
#         logging.info("Soup content successfully written to soup.html")
#     except Exception as e:
#         logging.error(f"Failed to write soup content to file: {e}")

#     # Look for the main container for job listings
#     cls = 'jobs-search__results-list'
#     job_container = soup.find('ul', class_= cls)
#     if not job_container:
#         print("Failed to find the job container.")
#         return []
    
#     # Extract job links and roles from the container
#     job_elements = job_container.find_all('li')
#     job_listings = []
#     job_roles = []

#     for job_element in job_elements:
#         link = job_element.find('a', class_='base-card__full-link')
#         role = job_element.find('span', class_='sr-only')
#         if link and 'href' in link.attrs:
#             job_listings.append(link['href'])
#         if role:
#             job_roles.append(role.get_text(strip=True))
    
#     logging.info(f"Found {len(job_listings)} job listings.")
#     for job, role in zip(job_listings, job_roles):
#         logging.info(f"Job Role: {role}, Link: {job}")
    
#     return job_listings

# def send_discord_notification(new_jobs):
#     webhook_url = 'https://discord.com/api/webhooks/1251547014538465464/JOAeBOupxOURwxl32arc3n8NmlfAY_3XdN7InH8WUxLsawSc0biClxpobrZ3rRdlErwx'  # Replace this with your actual Discord webhook URL

#     # Prepare the message content
#     message_parts = []
#     current_message = ""

#     for role, link in new_jobs:
#         job_info = f"Job Role: {role}\nLink: {link}\n\n"
#         if len(current_message) + len(job_info) > 2000:
#             message_parts.append(current_message)
#             current_message = job_info
#         else:
#             current_message += job_info

#     if current_message:
#         message_parts.append(current_message)

#     # Send each part as a separate message
#     for part in message_parts:
#         payload = {
#             'content': part
#         }
        
#         headers = {
#             'Content-Type': 'application/json'
#         }
        
#         response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        
#         if response.status_code != 204:
#             logging.error(f"Failed to send notification to Discord: {response.status_code}, {response.text}")
#         else:
#             logging.info("Notification sent to Discord successfully.")

# def notify_if_new_jobs():
#     new_jobs = get_job_listings()
#     if not new_jobs:
#         logging.info("No new jobs found.")
#         return
    
#     try:
#         with open('job_listings.txt', 'r') as file:
#             existing_jobs = file.read().splitlines()
#     except FileNotFoundError:
#         existing_jobs = []

#     new_job_listings = [job for job in new_jobs if job[1] not in existing_jobs]
    
#     if new_job_listings:
#         logging.info(f"New job listings found: {new_job_listings}")
#         send_discord_notification(new_job_listings)
        
#         with open('job_listings.txt', 'w') as file:
#             file.write('\n'.join(job[1] for job in new_jobs))
#     else:
#         logging.info("No new job listings to notify.")

# # Check for new jobs and notify
# notify_if_new_jobs()

import requests
from bs4 import BeautifulSoup
import json
import logging

# Configure logging
logging.basicConfig(filename='job_scraper.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s:%(message)s')

def get_job_listings():
    # url = 'https://www.linkedin.com/jobs/search/?currentJobId=3949316904&f_TPR=r86400&geoId=102713980&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&spellCorrectionEnabled=true'
    url = 'https://www.linkedin.com/jobs/search/?currentJobId=3949547169&f_TPR=r86400&geoId=102713980&keywords=software%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD&spellCorrectionEnabled=true'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve job listings: {response.status_code}")
        return []
    
    logging.info("Successfully retrieved job listings page.")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Save the soup to a file for inspection
    try:
        with open('./soup.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())
        logging.info("Soup content successfully written to soup.html")
    except Exception as e:
        logging.error(f"Failed to write soup content to file: {e}")
    
    # Look for the main container for job listings
    job_container = soup.find('ul', class_='jobs-search__results-list')
    if not job_container:
        logging.error("Failed to find the job container.")
        return []

    # Extract job links and roles from the container
    job_elements = job_container.find_all('li')
    job_listings = []

    for job_element in job_elements:
        link = job_element.find('a', class_='base-card__full-link')
        role = job_element.find('span', class_='sr-only')
        if link and 'href' in link.attrs and role:
            job_listings.append((role.get_text(strip=True), link['href']))
    
    logging.info(f"Found {len(job_listings)} job listings.")
    for role, link in job_listings:
        logging.info(f"Job Role: {role}, Link: {link}")
    
    return job_listings

def send_discord_notification(new_jobs):
    webhook_url = 'https://discord.com/api/webhooks/1251547014538465464/JOAeBOupxOURwxl32arc3n8NmlfAY_3XdN7InH8WUxLsawSc0biClxpobrZ3rRdlErwx'  # Replace this with your actual Discord webhook URL

    # Debug: Print new_jobs
    logging.debug(f"new_jobs: {new_jobs}")

    # Ensure new_jobs contains tuples
    for item in new_jobs:
        if not isinstance(item, tuple):
            logging.error(f"Invalid item in new_jobs (not a tuple): {item}")
            return
        if len(item) != 2:
            logging.error(f"Invalid item in new_jobs (expected 2 elements): {item}")
            return
    
    # Prepare the message content
    message_parts = []
    current_message = ""

    for role, link in new_jobs[:10]:
        job_info = f"Job Role: {role}\nLink: {link}\n\n"
        if len(current_message) + len(job_info) > 2000:
            message_parts.append(current_message)
            current_message = job_info
        else:
            current_message += job_info

    if current_message:
        message_parts.append(current_message)

    # Send each part as a separate message
    for part in message_parts:
        payload = {
            'content': part
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        
        if response.status_code != 204:
            logging.error(f"Failed to send notification to Discord: {response.status_code}, {response.text}")
        else:
            logging.info("Notification sent to Discord successfully.")

def notify_if_new_jobs():
    new_jobs = get_job_listings()
    if not new_jobs:
        logging.info("No new jobs found.")
        return
    
    try:
        with open('job_listings.txt', 'r') as file:
            existing_jobs = file.read().splitlines()
    except FileNotFoundError:
        existing_jobs = []

    new_job_listings = [job for job in new_jobs if job[1] not in existing_jobs]
    
    if new_job_listings:
        logging.info(f"New job listings found: {new_job_listings}")
        send_discord_notification(new_job_listings)
        
        with open('job_listings.txt', 'w') as file:
            file.write('\n'.join(job[1] for job in new_jobs))
    else:
        logging.info("No new job listings to notify.")

# Check for new jobs and notify
notify_if_new_jobs()
