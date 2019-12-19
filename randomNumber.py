import random
import numpy
import datetime
import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials

def thing():
    import json, requests

    # For our purposes, a session lets you reuse the same connection to the server, without having to reconnect every time.
    s = requests.Session()

    # The auth key lets TBA know who is making the API call, i3t's linked to my TBA account. You can use mine for now
    s.headers.update({'X-TBA-Auth-Key': "55ika2mnPFlW98bRBf6IKAxVWFzOriiQxd5fOsxllIiGZkfIeb85In9W8KzMN6CT"})

    # Outputs a JSON object
    def tbaRequest(query):
      r = s.get("http://www.thebluealliance.com/api/v3/" + query)
      return json.loads(r.text)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client-secret.json', scope)
    client = gspread.authorize(creds)

     # Find a workbook by name and open the first sheet
     # Make sure you use the right name here.
    spr = client.open("Team 1257 Data Scouting Responses: 2019")
    wks = spr.worksheet('Component OPRs')  # or the correct name of requested worksheet
     #sheet = client.open("Team 1257 Data Scouting Responses: 2019").TeamRank
     # Extract and print all of the values
    events = ["2019pahat","2019njfla","2019pawch","2019njbri","2019paphi","2019njtab","2019njski","2019paben","2019mrcmp"]
    matches = []
    #teams = tbaRequest("district/2019fma/teams/keys")
    teams = list((wks.acell("A2").value).split("', '"))
    for event in events:
        games = tbaRequest("event/"+event+"/matches/simple")
        for game in games:
            matches.append(game)
    scores = []
    for match in matches:
        scores.append([match["alliances"]["red"]["team_keys"][0],match["alliances"]["red"]["team_keys"][1],match["alliances"]["red"]["team_keys"][2],match["alliances"]["red"]["score"]-match["alliances"]["blue"]["score"]])
        scores.append([match["alliances"]["blue"]["team_keys"][0],match["alliances"]["blue"]["team_keys"][1],match["alliances"]["blue"]["team_keys"][2],match["alliances"]["blue"]["score"]-match["alliances"]["red"]["score"]])
    info = [teams,list((wks.acell("B2").value).split(",")),list((wks.acell("C2").value).split(",")),list((wks.acell("D2").value).split(",")),list((wks.acell("E2").value).split(",")),list((wks.acell("F2").value).split(",")),list((wks.acell("G2").value).split(","))]
    scoreData = pandas.DataFrame(data = scores)
    oprData = pandas.DataFrame(data = info)
    return(scoreData,oprData)
#print(thing())
