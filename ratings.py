import requests
from bs4 import BeautifulSoup

def get_team_ratings(team_code, season="2024"):
    url = f"https://www.basketball-reference.com/teams/{team_code}/{season}.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        raise Exception("Error al obtener datos del equipo")

    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.find("table", {"id": "team_misc"})
    rows = table.find_all("tr")

    ratings = {}
    for row in rows:
        th = row.find("th")
        td = row.find("td")
        if th and td:
            ratings[th.text.strip()] = td.text.strip()

    off = float(ratings["Off Rtg"])
    deff = float(ratings["Def Rtg"])
    pace = float(ratings["Pace"])

    return off, deff, pace
