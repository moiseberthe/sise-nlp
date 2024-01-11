import sys
from fastapi import FastAPI, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import joinedload
from sqlalchemy import func
sys.path.append('..')
from utils.entities import Region, Department, City, Annonce, Source, Contrat, Activity, Job, Chat
from utils.scraper import pole_emploi_scraper
from utils.Nettoyage import Nettoyage
sys.path.pop()

# Initialize FastAPI app
app = FastAPI()
 
@app.get("/")
def accueil():
    return {"message": "Bienvenu à l'API de notre projet de webscrapping"}


@app.get("/annonces")
def get_all_annonces():
    annonces = Annonce.find_all2()
    if len(annonces) == 0:
        raise HTTPException(status_code=404, detail="No annonce found")
    return annonces

@app.get("/annonces/")
def get_all_annonces(offset: int = Query(0, description="Offset", ge=0), limit: int = Query(10, description="Limit", le=500)):
    annonces = Annonce.find_all(offset, limit)
    if len(annonces) == 0:
        raise HTTPException(status_code=404, detail="No annonce found")
    return annonces

@app.get("/annonces/{annonce_id}")
def get_annonce(annonce_id: int):
    annonce = Annonce.find(annonce_id)
    if annonce is None:
        raise HTTPException(status_code=404, detail="Annonce not found")
    return annonce

@app.get("/regions/{region_id}")
def get_region(region_id: int):
    region = Region.query().filter(Region.id == region_id).options(joinedload(Region.departments)).first()
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return region

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
def get_all_cities(offset: int = Query(0, description="Offset", ge=0), limit: int = Query(100, description="Limit", le=40000)):
    
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
def get_all_sources(offset: int = Query(0, description="Offset", ge=0), limit: int = Query(100, description="Limit", le=10)):
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

@app.get("/activities/{activity_id}")
def get_activity(activity_id: int):
    activity = Activity.query().filter(Activity.id == activity_id).options(joinedload(Activity.annonces)).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    job = Job.query().filter(Job.id == job_id).options(joinedload(Job.annonces)).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs/scrape/{src}/{nb_annonces}")
def scrape_annonce(src: str, nb_annonces: int):
    annonces = pole_emploi_scraper(nb_annonces)
    if len(annonces) == 0:
        raise HTTPException(status_code=404, detail="No annonce found")
    return annonces


##########

def load_data():
    offres = Annonce.find_all2()
    texts= [x.description+" "+x.title+" "+x.company_name+" "+x.profile+" "+x.skills for x in offres]
    urls= [x.url for x in offres]
    ids= [x.id for x in offres]
    net= Nettoyage(algo="nltk", contents=texts, ids=ids, urls=urls, cleaned=True)
    return net

@app.post("/chat")
def chat(chat: Chat):
    net= load_data()
    rep= net.return_n_best_doc(text=chat.text, to_return="url")
    #net.save_objects()
    res= "\t\n ".join(rep)
    return {"url": res}

@app.post("/sentiment")
def sentiment(chat: Chat):
    net= load_data()
    rep= net.sentiment_analysis(text=chat.text)
    return {"sentiment":rep}  

@app.get("/sentences")
def wordcloud():
    net= load_data()
    rep= net.getSentences()
    return {"res": rep}

@app.get("/tsne")
def tsne():
    net= load_data() 
    tsne_r= net.tsne_reduc(3)
    return {"tsne": tsne_r.tolist()}

@app.get("/clustering")
def cluster():
    net= load_data()
    clust= net.clustering()
    return {"clust": clust.tolist()}

@app.post("/match")
def match_cvs(file: UploadFile = File(...)):
    net= load_data()
    file_location = f"./utils/files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    urls= net.match_cv_v2(chemin_fichier=file_location, to_return="url")
    return {"urls": urls.tolist()}

# end