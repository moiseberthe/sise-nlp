from utils.entities import Region, Departement, City, Annonce, Source, Contrat

def make_migration():
    Region.create_table()
    Departement.create_table()
    City.create_table()
    Source.create_table()
    Contrat.create_table()
    Annonce.create_table()

    # Insertion des sources
    sources = { 'APEC': 1, 'Pôle-emploi': 2, 'LinkedIn': 3 }
    for source, id in sources.items():
        Source(name=source).create()

    # Insertion des types de contrats
    contracts = ['CDI', 'CDD', 'Stage', 'Alternance', 'Autre']
    for contrat in contracts:
        Contrat(name=contrat).create()