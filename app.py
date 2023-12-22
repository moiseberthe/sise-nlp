from models.entities import Region, Departement, Source, Contrat
from database.migration import make_migration

# creation des tables
make_migration()

# Insertion des sources
sources = { 'APEC': 1, 'Pôle-emploi': 2, 'LinkedIn': 3 }
for source, id in sources.items():
    Source(name=source).create()

# Insertion des sources
contracts = ['CDI', 'CDD', 'Stage', 'Alternance', 'Autre']
for contrat in contracts:
    Contrat(name=contrat).create()

# Region.create_table(engine)

# # region = Region(name="Bamako 2")

# Create a new Region instance and persist it to the database
# # region = region.create()


# departement  = Departement(name="Departement", region_id=region.id)
# departement = departement.create()
# for r in Region.find_all():
#     print(r.name)
#     # Region.delete(r.id)