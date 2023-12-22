from models.entities import Region, Departement, City, Annonce, Source, Contrat

def make_migration():
    Region.create_table()
    Departement.create_table()
    City.create_table()
    Annonce.create_table()
    Source.create_table()
    Contrat.create_table()