# ratings.py
# Datos aproximados NBA (escala REAL)
# off_rating y def_rating: puntos por 100 posesiones
# pace: posesiones por partido

TEAM_RATINGS = {
    "ATL": (114, 116, 101),
    "BOS": (120, 111, 98),
    "BKN": (113, 115, 100),
    "CHA": (109, 118, 100),
    "CHI": (111, 114, 98),
    "CLE": (116, 111, 97),
    "DAL": (118, 114, 100),
    "DEN": (117, 112, 98),
    "DET": (108, 119, 99),
    "GSW": (116, 115, 102),
    "HOU": (111, 117, 101),
    "IND": (118, 120, 103),
    "LAC": (115, 112, 99),
    "LAL": (114, 115, 100),
    "MEM": (110, 116, 99),
    "MIA": (112, 110, 96),
    "MIL": (119, 113, 100),
    "MIN": (114, 109, 98),
    "NOP": (113, 114, 99),
    "NYK": (112, 110, 97),
    "OKC": (118, 112, 101),
    "ORL": (110, 111, 98),
    "PHI": (117, 113, 99),
    "PHX": (118, 114, 100),
    "POR": (109, 118, 101),
    "SAC": (117, 116, 102),
    "SAS": (108, 119, 100),
    "TOR": (111, 114, 99),
    "UTA": (110, 116, 98),
    "WAS": (109, 120, 101),
}

def get_team_ratings(team):
    return TEAM_RATINGS[team]
