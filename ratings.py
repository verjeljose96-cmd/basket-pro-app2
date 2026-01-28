import requests
from bs4 import BeautifulSoup

# Valores promedio NBA (fallback)
NBA_AVG = {
    "off": 114,
    "def": 114,
    "pace": 99
}

def get_team_ratings(team_code, season="2024"):
    url = f"https://www.basketball-reference.com/teams/{team_code}/{season}.html"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return NBA_AVG["off"], NBA_AVG["def"], NBA_AVG["pace"]

        soup = BeautifulSoup(r.text, "html.parser")
        table = soup.find("table", {"id": "team_misc"})

        if table is None:
            return NBA_AVG["off"], NBA_AVG["def"], NBA_AVG["pace"]

        ratings = {}
        for row in table.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td:
                ratings[th.text.strip()] = td.text.strip()

        off = float(ratings.get("Off Rtg", NBA_AVG["off"]))
        deff = float(ratings.get("Def Rtg", NBA_AVG["def"]))
        pace = float(ratings.get("Pace", NBA_AVG["pace"]))

        return off, deff, pace

    except Exception:
        return NBA_AVG["off"], NBA_AVG["def"], NBA_AVG["pace"]
