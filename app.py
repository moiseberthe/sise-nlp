from utils.entities import Region, Departement, Source, Contrat
from database.migration import make_migration

# creation des tables avec leur contenu
make_migration()