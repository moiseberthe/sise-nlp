from utils.entities import Region, Departement, City, Annonce, Source, Contrat
from database.data import regions, departements, sources, contracts
from datetime import datetime
import json

def insert_jobs(jobs):
    for job in jobs:
        try:
            date = datetime.strptime(job['date'], '%Y-%m-%d')
        except:
            date = datetime.now()

        annonce = Annonce(
            url = job['url'],
            title = job['title'],
            company_name = job['company'],
            location = job['location'],
            date = date,
            descripiton = job['description'],
            poste = job['poste'],
            activity = job['activity'],
            profile = job['profile'],
            skills = '|'.join(job['skills']),
            contrat_id =   Contrat.contracts().get(job['contrat'], 5),
            source_id = Source.sources()[job['source']],
        )
        annonce.create()

def make_migration():
    Region.create_table()
    Departement.create_table()
    City.create_table()
    Source.create_table()
    Contrat.create_table()
    Annonce.create_table()

    # Insertion des sources
    for source in sources:
        Source(name=source).create()

    # Insertion des types de contrats
    for contrat in contracts:
        Contrat(name=contrat).create()

    # Insertion des regions
    for region in regions:
        Region(
            code=region['code'],
            name=region['name']
        ).create()
    
    # Insertion des departements
    for departement in departements:
        Departement(
            code=departement['code'],
            name=departement['name'],
            region_code=departement['region_code']
        ).create()

    # Insertion des villes
        
    # Insertion des annonces de job
    with open('./data/processed/all-jobs.json', 'r+') as f:
        jobs = json.load(f)

    insert_jobs(jobs)

    
    