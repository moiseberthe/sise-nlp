sources = ['APEC', 'Pôle-emploi', 'LinkedIn']

contracts = ['CDI', 'CDD', 'Stage', 'Alternance', 'Autre']

regions = [
  { 'code': '01', 'name': 'Guadeloupe' },
  { 'code': '02', 'name': 'Martinique' },
  { 'code': '03', 'name': 'Guyane' },
  { 'code': '04', 'name': 'La Réunion' },
  { 'code': '06', 'name': 'Mayotte' },
  { 'code': '11', 'name': 'Île-de-France' },
  { 'code': '24', 'name': 'Centre-Val de Loire' },
  { 'code': '27', 'name': 'Bourgogne-Franche-Comté' },
  { 'code': '28', 'name': 'Normandie' },
  { 'code': '32', 'name': 'Hauts-de-France' },
  { 'code': '44', 'name': 'Grand Est' },
  { 'code': '52', 'name': 'Pays de la Loire' },
  { 'code': '53', 'name': 'Bretagne' },
  { 'code': '75', 'name': 'Nouvelle-Aquitaine' },
  { 'code': '76', 'name': 'Occitanie' },
  { 'code': '84', 'name': 'Auvergne-Rhône-Alpes' },
  { 'code': '93', 'name': 'Provence-Alpes-Côte d\'Azur' },
  { 'code': '94', 'name': 'Corse' },
  { 'code': 'COM', 'name': 'Collectivités d\'Outre-Mer' }
]

departements = [
  {
    "code": "01",
    "name": "Ain",
    "region_code": "84"
  },
  {
    "code": "02",
    "name": "Aisne",
    "region_code": "32"
  },
  {
    "code": "03",
    "name": "Allier",
    "region_code": "84"
  },
  {
    "code": "04",
    "name": "Alpes-de-Haute-Provence",
    "region_code": "93"
  },
  {
    "code": "05",
    "name": "Hautes-Alpes",
    "region_code": "93"
  },
  {
    "code": "06",
    "name": "Alpes-Maritimes",
    "region_code": "93"
  },
  {
    "code": "07",
    "name": "Ardèche",
    "region_code": "84"
  },
  {
    "code": "08",
    "name": "Ardennes",
    "region_code": "44"
  },
  {
    "code": "09",
    "name": "Ariège",
    "region_code": "76"
  },
  {
    "code": "10",
    "name": "Aube",
    "region_code": "44"
  },
  {
    "code": "11",
    "name": "Aude",
    "region_code": "76"
  },
  {
    "code": "12",
    "name": "Aveyron",
    "region_code": "76"
  },
  {
    "code": "13",
    "name": "Bouches-du-Rhône",
    "region_code": "93"
  },
  {
    "code": "14",
    "name": "Calvados",
    "region_code": "28"
  },
  {
    "code": "15",
    "name": "Cantal",
    "region_code": "84"
  },
  {
    "code": "16",
    "name": "Charente",
    "region_code": "75"
  },
  {
    "code": "17",
    "name": "Charente-Maritime",
    "region_code": "75"
  },
  {
    "code": "18",
    "name": "Cher",
    "region_code": "24"
  },
  {
    "code": "19",
    "name": "Corrèze",
    "region_code": "75"
  },
  {
    "code": "21",
    "name": "Côte-d'Or",
    "region_code": "27"
  },
  {
    "code": "22",
    "name": "Côtes-d'Armor",
    "region_code": "53"
  },
  {
    "code": "23",
    "name": "Creuse",
    "region_code": "75"
  },
  {
    "code": "24",
    "name": "Dordogne",
    "region_code": "75"
  },
  {
    "code": "25",
    "name": "Doubs",
    "region_code": "27"
  },
  {
    "code": "26",
    "name": "Drôme",
    "region_code": "84"
  },
  {
    "code": "27",
    "name": "Eure",
    "region_code": "28"
  },
  {
    "code": "28",
    "name": "Eure-et-Loir",
    "region_code": "24"
  },
  {
    "code": "29",
    "name": "Finistère",
    "region_code": "53"
  },
  {
    "code": "2A",
    "name": "Corse-du-Sud",
    "region_code": "94"
  },
  {
    "code": "2B",
    "name": "Haute-Corse",
    "region_code": "94"
  },
  {
    "code": "30",
    "name": "Gard",
    "region_code": "76"
  },
  {
    "code": "31",
    "name": "Haute-Garonne",
    "region_code": "76"
  },
  {
    "code": "32",
    "name": "Gers",
    "region_code": "76"
  },
  {
    "code": "33",
    "name": "Gironde",
    "region_code": "75"
  },
  {
    "code": "34",
    "name": "Hérault",
    "region_code": "76"
  },
  {
    "code": "35",
    "name": "Ille-et-Vilaine",
    "region_code": "53"
  },
  {
    "code": "36",
    "name": "Indre",
    "region_code": "24"
  },
  {
    "code": "37",
    "name": "Indre-et-Loire",
    "region_code": "24"
  },
  {
    "code": "38",
    "name": "Isère",
    "region_code": "84"
  },
  {
    "code": "39",
    "name": "Jura",
    "region_code": "27"
  },
  {
    "code": "40",
    "name": "Landes",
    "region_code": "75"
  },
  {
    "code": "41",
    "name": "Loir-et-Cher",
    "region_code": "24"
  },
  {
    "code": "42",
    "name": "Loire",
    "region_code": "84"
  },
  {
    "code": "43",
    "name": "Haute-Loire",
    "region_code": "84"
  },
  {
    "code": "44",
    "name": "Loire-Atlantique",
    "region_code": "52"
  },
  {
    "code": "45",
    "name": "Loiret",
    "region_code": "24"
  },
  {
    "code": "46",
    "name": "Lot",
    "region_code": "76"
  },
  {
    "code": "47",
    "name": "Lot-et-Garonne",
    "region_code": "75"
  },
  {
    "code": "48",
    "name": "Lozère",
    "region_code": "76"
  },
  {
    "code": "49",
    "name": "Maine-et-Loire",
    "region_code": "52"
  },
  {
    "code": "50",
    "name": "Manche",
    "region_code": "28"
  },
  {
    "code": "51",
    "name": "Marne",
    "region_code": "44"
  },
  {
    "code": "52",
    "name": "Haute-Marne",
    "region_code": "44"
  },
  {
    "code": "53",
    "name": "Mayenne",
    "region_code": "52"
  },
  {
    "code": "54",
    "name": "Meurthe-et-Moselle",
    "region_code": "44"
  },
  {
    "code": "55",
    "name": "Meuse",
    "region_code": "44"
  },
  {
    "code": "56",
    "name": "Morbihan",
    "region_code": "53"
  },
  {
    "code": "57",
    "name": "Moselle",
    "region_code": "44"
  },
  {
    "code": "58",
    "name": "Nièvre",
    "region_code": "27"
  },
  {
    "code": "59",
    "name": "Nord",
    "region_code": "32"
  },
  {
    "code": "60",
    "name": "Oise",
    "region_code": "32"
  },
  {
    "code": "61",
    "name": "Orne",
    "region_code": "28"
  },
  {
    "code": "62",
    "name": "Pas-de-Calais",
    "region_code": "32"
  },
  {
    "code": "63",
    "name": "Puy-de-Dôme",
    "region_code": "84"
  },
  {
    "code": "64",
    "name": "Pyrénées-Atlantiques",
    "region_code": "75"
  },
  {
    "code": "65",
    "name": "Hautes-Pyrénées",
    "region_code": "76"
  },
  {
    "code": "66",
    "name": "Pyrénées-Orientales",
    "region_code": "76"
  },
  {
    "code": "67",
    "name": "Bas-Rhin",
    "region_code": "44"
  },
  {
    "code": "68",
    "name": "Haut-Rhin",
    "region_code": "44"
  },
  {
    "code": "69",
    "name": "Rhône",
    "region_code": "84"
  },
  {
    "code": "70",
    "name": "Haute-Saône",
    "region_code": "27"
  },
  {
    "code": "71",
    "name": "Saône-et-Loire",
    "region_code": "27"
  },
  {
    "code": "72",
    "name": "Sarthe",
    "region_code": "52"
  },
  {
    "code": "73",
    "name": "Savoie",
    "region_code": "84"
  },
  {
    "code": "74",
    "name": "Haute-Savoie",
    "region_code": "84"
  },
  {
    "code": "75",
    "name": "Paris",
    "region_code": "11"
  },
  {
    "code": "76",
    "name": "Seine-Maritime",
    "region_code": "28"
  },
  {
    "code": "77",
    "name": "Seine-et-Marne",
    "region_code": "11"
  },
  {
    "code": "78",
    "name": "Yvelines",
    "region_code": "11"
  },
  {
    "code": "79",
    "name": "Deux-Sèvres",
    "region_code": "75"
  },
  {
    "code": "80",
    "name": "Somme",
    "region_code": "32"
  },
  {
    "code": "81",
    "name": "Tarn",
    "region_code": "76"
  },
  {
    "code": "82",
    "name": "Tarn-et-Garonne",
    "region_code": "76"
  },
  {
    "code": "83",
    "name": "Var",
    "region_code": "93"
  },
  {
    "code": "84",
    "name": "Vaucluse",
    "region_code": "93"
  },
  {
    "code": "85",
    "name": "Vendée",
    "region_code": "52"
  },
  {
    "code": "86",
    "name": "Vienne",
    "region_code": "75"
  },
  {
    "code": "87",
    "name": "Haute-Vienne",
    "region_code": "75"
  },
  {
    "code": "88",
    "name": "Vosges",
    "region_code": "44"
  },
  {
    "code": "89",
    "name": "Yonne",
    "region_code": "27"
  },
  {
    "code": "90",
    "name": "Territoire de Belfort",
    "region_code": "27"
  },
  {
    "code": "91",
    "name": "Essonne",
    "region_code": "11"
  },
  {
    "code": "92",
    "name": "Hauts-de-Seine",
    "region_code": "11"
  },
  {
    "code": "93",
    "name": "Seine-Saint-Denis",
    "region_code": "11"
  },
  {
    "code": "94",
    "name": "Val-de-Marne",
    "region_code": "11"
  },
  {
    "code": "95",
    "name": "Val-d'Oise",
    "region_code": "11"
  },
  {
    "code": "971",
    "name": "Guadeloupe",
    "region_code": "01"
  },
  {
    "code": "972",
    "name": "Martinique",
    "region_code": "02"
  },
  {
    "code": "973",
    "name": "Guyane",
    "region_code": "03"
  },
  {
    "code": "974",
    "name": "La Réunion",
    "region_code": "04"
  },
  {
    "code": "976",
    "name": "Mayotte",
    "region_code": "06"
  },
  {
    "code": "975",
    "name": "Saint-Pierre-et-Miquelon",
    "region_code": "COM"
  },
  {
    "code": "977",
    "name": "Saint-Barthélemy",
    "region_code": "COM"
  },
  {
    "code": "978",
    "name": "Saint-Martin",
    "region_code": "COM"
  },
  {
    "code": "984",
    "name": "Terres australes et antarctiques françaises",
    "region_code": "COM"
  },
  {
    "code": "986",
    "name": "Wallis et Futuna",
    "region_code": "COM"
  },
  {
    "code": "987",
    "name": "Polynésie française",
    "region_code": "COM"
  },
  {
    "code": "988",
    "name": "Nouvelle-Calédonie",
    "region_code": "COM"
  },
  {
    "code": "989",
    "name": "Île de Clipperton",
    "region_code": "COM"
  }
]