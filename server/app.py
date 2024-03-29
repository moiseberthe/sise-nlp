import sys
from fastapi import FastAPI, HTTPException, Query, File, UploadFile, Path
from sqlalchemy.orm import joinedload
from sqlalchemy import func, or_

sys.path.append('..')
from utils.entities import Region, Department, City, Annonce, Source, Contrat, Activity, Job, Chat
from utils.scraper import pole_emploi_scraper, apec_scraper
from utils.Nettoyage import Nettoyage
from database.migration import insert_jobs
sys.path.pop()

# Initialize FastAPI app
app = FastAPI()
 
@app.get("/")
def accueil():
    return {"message": "Bienvenu à l'API de notre projet de webscrapping"}

@app.get("/annonces/{annonce_id}")
def get_annonce(annonce_id: int):
    annonce = Annonce.find(annonce_id)
    if annonce is None:
        raise HTTPException(status_code=404, detail="Annonce not found")
    return annonce

@app.get("/annonces/")
def get_all_annonces(
    offset: int = Query(None, description="Offset", ge=0),
    limit: int = Query(None, description="Limit", le=500),
    formated: bool = False
):
    annonces = Annonce.find_all(offset, limit)
    if len(annonces) == 0:
        raise HTTPException(status_code=404, detail="No annonce found")
    if formated:
        return [{"contrat": a.contrat.name, "city": a.city.name, "activity": a.activity.name, "source": a.source.name} for a in annonces]
    return annonces

@app.get("/annonces/{region}/{department}/{job}/{contrat}/{activity}")
def get_filtred_annonces(
   region: str = Path(..., title="Region", description="La région"),
   department: str = Path(..., title="Department", description="Le department"),
   job: str = Path(..., title="Job", description="Le poste"),
   contrat: str = Path(..., title="Contrat", description="Le type de contrat"),
   activity: str = Path(..., title="Activity", description="Le domainde d'activité"),
):
   default_option = '00'
   filters = [
      (Region.id == region) if region != default_option else None,
      (Department.code == department) if department != default_option else None,
      (Annonce.job_id == int(job)) if job != default_option else None,
      (Annonce.contrat_id == int(contrat)) if contrat != default_option else None,
      (Annonce.activity_id == int(activity)) if activity != default_option else None
   ]
   filters = [f for f in filters if f is not None]
   
   annonces = (Annonce.db().query(Annonce, City.name, City.gps_lat, City.gps_lng, Department.name, Region.name, Contrat.name, Source.name)
      .outerjoin(City, City.id == Annonce.city_id)
      .outerjoin(Source, Source.id == Annonce.source_id)
      .outerjoin(Contrat, Contrat.id == Annonce.contrat_id)
      .outerjoin(Department,  City.department_code == Department.code)
      .outerjoin(Region, Region.code == Department.region_code)
      .filter(*filters)
   )
   return [
      {
         **a.__dict__,
         **{'city': city, 'gps_lat': lat, 'gps_lng': lng,  'departement': dept, 'region': region, 'contrat': contrat, 'source': source}
      }
      for a, city, lat, lng, dept, region, contrat, source in annonces
   ]

@app.get("/annonces/scrape/{src}/{nb_annonces}")
def scrape_annonces(src: str, nb_annonces: int):
    annonces = []
    if (src == "Pôle-emploi"):
        annonces = pole_emploi_scraper(nb_annonces)
    elif (src == "APEC"):
        annonces = apec_scraper(nb_jobs=nb_annonces, in_docker=True)
    
    if len(annonces) == 0:
        raise HTTPException(status_code=404, detail="No annonce found")
    
    #mettre dans la base de donnée
    for job in Annonce.find_all(limit=nb_annonces):
        Annonce.delete(job.id)
    annonces = insert_jobs(annonces)
    all_ann = Annonce.find_all()
    #update object
    update_data(all_ann)
    return annonces

@app.get("/regions")
def get_all_regions(
    offset: int = Query(0, description="Offset", ge=0),
    limit: int = Query(20, description="Limit", le=20)
):
    regions = Region.find_all(offset=offset, limit=limit)
    if len(regions) == 0:
        raise HTTPException(status_code=404, detail="No region found")
    return regions

@app.get("/regions/{region_id}")
def get_region(region_id: int):
    region = Region.query().filter(Region.id == region_id).options(joinedload(Region.departments)).first()
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return region

@app.get("/departments")
def get_all_departments(
    offset: int = Query(0, description="Offset", ge=0),
    limit: int = Query(20, description="Limit", le=20)
):
    departments = Region.find_all(offset=offset, limit=limit)
    if len(departments) == 0:
        raise HTTPException(status_code=404, detail="No department found")
    return departments

@app.get("/departments/{department_id}")
def get_department(department_id: int):
    department = Department.query().filter(Department.id == department_id).options(joinedload(Department.cities)).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@app.get("/cities/{city_id}")
def get_city(city_id: int):
    city = City.query().filter(City.id == city_id).options(joinedload(City.annonces)).first()
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@app.get("/cities/")
def get_all_cities(
    offset: int = Query(0, description="Offset", ge=0),
    limit: int = Query(100, description="Limit", le=500)
):
    cities = (
        City.db().query(City, func.count(Annonce.id).label("nb"))
        .outerjoin(Annonce, City.id == Annonce.city_id)
        .group_by(City.department_code)
        .having(func.count(Annonce.id) > 0)
        .offset(offset)
        .limit(limit)
        .all()
    )
    if len(cities) == 0:
        raise HTTPException(status_code=404, detail="No city found")
    return [{**city.__dict__, **{"count": nb}} for city, nb in cities]


@app.get("/sources/{source_id}")
def get_source(source_id: int):
    source = Source.query().filter(Source.id == source_id).options(joinedload(Source.annonces)).first()
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

@app.get("/sources/")
def get_all_sources(offset: int = Query(0, description="Offset", ge=0), limit: int = Query(10, description="Limit", le=10)):
    sources = Source.find_all(offset=offset, limit=limit)
    if len(sources) == 0:
        raise HTTPException(status_code=404, detail="No source found")
    return sources

@app.get("/contrats/{contrat_id}")
def get_contrat(contrat_id: int):
    contrat = Contrat.query().filter(Contrat.id == contrat_id).options(joinedload(Contrat.annonces)).first()
    if contrat is None:
        raise HTTPException(status_code=404, detail="Contrat not found")
    return contrat

@app.get("/contrats")
def get_all_contrats(
    offset: int = Query(0, description="Offset", ge=0),
    limit: int = Query(10, description="Limit", le=10)
):
    contrats = Contrat.find_all(offset=offset, limit=limit)
    if len(contrats) == 0:
        raise HTTPException(status_code=404, detail="No contrat found")
    return contrats

@app.get("/activities/{activity_id}")
def get_activity(activity_id: int):
    activity = Activity.query().filter(Activity.id == activity_id).options(joinedload(Activity.annonces)).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@app.get("/activities")
def get_all_activities(
    offset: int = Query(0, description="Offset", ge=0),
    limit: int = Query(150, description="Limit", le=150)
):
    activities = Activity.find_all(offset=offset, limit=limit)
    if len(activities) == 0:
        raise HTTPException(status_code=404, detail="No activity found")
    return activities

@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    job = Job.query().filter(Job.id == job_id).options(joinedload(Job.annonces)).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs")
def get_all_jobs(
    offset: int = Query(0, description="Offset", ge=0),
    limit: int = Query(150, description="Limit", le=150)
):
    jobs = Job.find_all(offset=offset, limit=limit)
    if len(jobs) == 0:
        raise HTTPException(status_code=404, detail="No job found")
    return jobs

##########

def load_data():
    annonces = Annonce.find_all()
    texts = [x.description+" "+x.title+" "+x.company_name+" "+x.profile+" "+x.skills+" "+x.contrat.name+" "+x.city.name for x in annonces]
    urls = [x.url for x in annonces]
    ids = [x.id for x in annonces]
    net = Nettoyage(algo="spacy", contents=texts, ids=ids, urls=urls, cleaned=True)
    return net

def update_data(annonces):
    texts = [x.description+" "+x.title+" "+x.company_name+" "+x.profile+" "+x.skills+" "+x.contrat.name+" "+x.city.name for x in annonces]
    urls = [x.url for x in annonces]
    ids = [x.id for x in annonces]
    net = Nettoyage(algo="spacy", contents=texts, ids=ids, urls=urls, cleaned=False)
    net.return_n_best_doc(text="data", to_return="id", n=2)
    net.save_objects()

@app.get("/vector")
def tfidf():
    net = load_data()
    rep = net.getVector()
    return {"vector": rep.to_json(orient="records") }

@app.post("/chat")
def chat(chat: Chat):
    net = load_data()
    rep = net.return_n_best_doc(text=chat.text, to_return="url")
    #net.save_objects()
    #res= "\t\n ".join(rep)
    return {"url": rep.tolist()}

@app.post("/sentiment")
def sentiment(chat: Chat):
    net = load_data()
    rep = net.sentiment_analysis(text=chat.text)
    return {"sentiment":rep}   

@app.get("/sentences")
def wordcloud():
    net = load_data()
    rep = net.getSentences()
    return {"res": rep}

@app.get("/tsne")
def tsne():
    net = load_data() 
    tsne_r = net.tsne_reduc(3)
    return {"tsne": tsne_r.tolist()}

@app.get("/clustering")
def cluster():
    net = load_data()
    clust = net.clustering()
    return {"clust": clust.tolist()}

@app.post("/match")
def match_cvs(file: UploadFile = File(...)):
    net = load_data()
    file_location = f"./utils/files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    urls = net.match_cv_v2(chemin_fichier=file_location, to_return="url")
    return {"urls": urls.tolist()}

# end