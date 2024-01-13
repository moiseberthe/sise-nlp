from utils.entities import Region, Department, City, Annonce, Source, Contrat, Activity, Job
from database.data import regions, departments, sources, contracts
from datetime import datetime
import json

def find_or_create_activity(name):
    name = name.capitalize().strip().replace('œ', "oe")
    activity = Activity.find_by_name(name[1:])
    if activity is None:
        activity = Activity(name=name).create()
    return activity

def find_or_create_job(name):
    name = name.capitalize().strip().replace('œ', "oe")

    job = Job.find_by_name(name[1:])
    if job is None:
        job = Job(name=name).create()
    return job

def insert_jobs(annonces):
    inserteds = []
    for annonce in annonces:
        # todo: remove these two lines below
        if(annonce['source'] == 'linkedin'):
            return
        
        city = City.find_by_name(annonce['location'])
        
        if city is not None:
            activity = find_or_create_activity(annonce['activity'])
            job = find_or_create_job(annonce['poste'])

            try:
                date = datetime.strptime(annonce['date'], '%Y-%m-%d')
            except:
                date = datetime.now()
            
            inserted = Annonce(
                url=annonce['url'],
                title=annonce['title'],
                company_name=annonce['company'],
                city_id=city.id,
                date=date,
                description=annonce['description'],
                job_id=job.id,
                activity_id=activity.id,
                profile=annonce['profile'],
                skills='|'.join(annonce['skills']),
                contrat_id=Contrat.contracts().get(annonce['contrat'], 5),
                source_id=Source.sources()[annonce['source']],
            ).create()
            inserteds.append(inserted)
    return inserteds

def make_migration():
    Region.create_table()
    Department.create_table()
    City.create_table()
    Source.create_table()
    Contrat.create_table()
    Activity.create_table()
    Job.create_table()
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
    
    # Insertion des departments
    for department in departments:
        Department(
            code=department['code'],
            name=department['name'],
            region_code=department['region_code']
        ).create()

    # Insertion des villes
    with open('./data/location/cities.json', 'r+') as f:
        cities = json.load(f)
    for city in cities:
        City(
            department_code=city['department_code'],
            zip_code=city['zip_code'],
            name=city['name'],
            gps_lat=city['gps_lat'],
            gps_lng=city['gps_lng'],
        ).create()

    # Insertion des annonces de job
    with open('./data/processed/all-jobs.json', 'r+') as f:
        jobs = json.load(f)

    insert_jobs(jobs)

    
    