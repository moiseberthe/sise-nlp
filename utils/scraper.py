import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from env import CLIENT_ID, CLIENT_SECRET


def get_pole_emploi_access_token():
    url = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "api_offresdemploiv2 o2dsoffre"
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']


def pole_emploi_city_name(location):
    info = location.split('-', 1)
    try:
        city = info[1].strip()
    except:
        city = info[0].strip()
        
    if(len(info[0].strip()) != 2):
        city = location
    
    info = city.rsplit(' ', maxsplit=1)
    try:
        int(info[1])
        city = info[0].strip()
    except:
        city = city
    return city.split('(')[0]


def apec_scraper(nb_pages=10):
    job_page_url = 'https://www.apec.fr/candidat/recherche-emploi.html/emploi?motsCles=data&typesConvention=143684&typesConvention=143685&typesConvention=143686&typesConvention=143687'
    jobs_apec = []
    
    driver = webdriver.Chrome()
    CSS = By.CSS_SELECTOR

    for i in range(nb_pages):
        driver.get(f'{job_page_url}&page={i}')
        if(i == 0):
            try:
                accept_cookies = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
                )
            except:
                driver.quit()
            accept_cookies.click()

        #  job_links = driver.find_elements(CSS, '.container-result div > a')
        try:
            job_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((CSS, ".container-result div > a"))
            )
        except:
            driver.quit()

        # Get url, title and company name
        job_links = [
            (
                job_link.get_attribute('href'),
                job_link.find_element(CSS, 'h2.card-title').text,
                job_link.find_element(CSS, 'p.card-offer__company').text,
                job_link.find_element(CSS, 'li[title="Date de publication"]').text
            )
            for job_link in job_links
        ]

        # Loop through job links
        for url, title, company, date in job_links:
            date = date.split('/')
            date = '-'.join(date[::-1])
            # Open the job page
            driver.get(url)
            
            # Wait before looking for elements
            try:
                details = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((CSS, 'ul.details-offer-list.mb-20 > li'))
                )
            except:
                print("quiting")
                driver.quit()
            
            # entreprise
            company = details[0].text
            # type de contrat
            contrat = details[1].find_element(CSS, 'span').text.strip().lower().split()[0]
            # lieu de travail
            location = details[2].text.split(maxsplit=1)
            
            # Nettoyer et recupérer le bon nom de ville
            city = location[0].strip()
            if(len(city) < 3):
                city += ' '+(location[1].split(maxsplit=1)[0])
                
            # description
            description = driver.find_element(CSS, '.details-post > p').text
            # profil recherché
            profile = driver.find_element(CSS, '.details-post > p:nth-child(4)').text
            detail_posts = driver.find_elements(CSS, 'apec-poste-informations > .row.border-T > .col-lg-4 > .details-post')
            # Secteur d’activité du poste
            activity = detail_posts[6].find_element(CSS, 'span').text
            # Le nom du poste
            poste = detail_posts[3].find_element(CSS, 'span').text
            
            # competences
            competences = driver.find_elements(CSS, '.details-post .added-skills-container')
            try:
                see_more = competences[2].find_element(CSS, '.added-skills-language + p.m-0')
                see_more.click()
                hard_skills = competences[2].find_elements(CSS, '.added-skills-language')
                hard_skills = [skill.text for skill in hard_skills]
            except:
                hard_skills = []

            # Print or store the job details
            jobs_apec.append({
                'url': url,
                'title': title,
                'company': company,
                'contrat': contrat,
                'location': city,
                'date': date,
                'description': description,
                'profile': profile,
                'skills': hard_skills,
                'poste': poste,
                'activity': activity,
                'source': 'apec',
            })
    # Close the webdriver
    driver.quit()
    return jobs_apec


def pole_emploi_scraper(nb_jobs=200):
    access_token = get_pole_emploi_access_token()
    header = {'Authorization': f'Bearer {access_token}'}
    jobs_pole_emploi = []
    for i in range(nb_jobs // 100):
        response = requests.get(f'https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search?range={i*100}-{((i+1) * 100) - 1}&motsCles=data', headers=header)
        pole_emploi_response = response.json()['resultats']
        
        for job in pole_emploi_response:
            jobs_pole_emploi.append({
                'url': job['origineOffre']['urlOrigine'],
                'title': job['intitule'],
                'company': job['entreprise'].get('nom', 'Unknown'),
                'contrat': job['typeContrat'].strip().lower().split()[0],
                'location': job['lieuTravail'].get('codePostal', pole_emploi_city_name(job['lieuTravail']['libelle'])),
                'date': job['dateCreation'].split('T')[0],
                'description': job['description'],
                'profile': '',
                'skills': [c['libelle'] for c in job.get('competences', [])],
                'poste': job['appellationlibelle'],
                'activity': job.get('secteurActiviteLibelle', 'Unknown'),
                'source': 'pole-emploi',
            })
        time.sleep(1)
    return jobs_pole_emploi

# end