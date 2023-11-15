import requests
import re

url = "https://api.start.gg/gql/alpha"
header = {"Authorization" : "Bearer eff61c135e0546f45dbc554c02ee761d"}
body = """
query EventEntrants($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    name
    entrants(query: {
      page: $page
      perPage: $perPage
    }) {
      pageInfo {
        total
        totalPages
      }
      nodes {
        participants {
          gamerTag
          player{
            id
          }
        }
      }
    }
  }
}
"""
variable = {
  "eventId": 911475,
  "page": 1,
  "perPage": 500
}

def send_request(page, event):
  url = "https://api.start.gg/gql/alpha"
  header = {"Authorization" : "Bearer eff61c135e0546f45dbc554c02ee761d"}

  body = """
  query EventEntrants($eventId: ID!, $page: Int!, $perPage: Int!) {
    event(id: $eventId) {
      name
      entrants(query: {
        page: $page
        perPage: $perPage
      }) {
        pageInfo {
          total
          totalPages
        }
        nodes {
          participants {
            gamerTag
            player{
              id
            }
          }
        }
      }
    }
  }
  """

  variable = {
  "eventId": event,
  "page": page,
  "perPage": 400
  }

  r = requests.post(url, json={"query" : body, "variables" : variable}, headers=header)
  if re.search("\"nodes\":\[\]", r.text):
    return None
  return r.text

def parse(txt):
  search = re.search("\"gamerTag\":\"([^\"]+)\"", txt)
  if search == None:
    return None
  name = search.group()
  name = name[12:-1]

  id = re.search("id\":[0-9]+", txt).group()
  id = id[4:]
    
  return(name, id)

def main():
  #ids consists of ids of top tournaments, used to get ids of top players
  ids = [911475, 769490, 400200, 342224, 399009, 119796, 36761, 909751, 634112, 360333, 122648, 84300, 37932, 12830, 10300]
  coveredIds = dict()

  file = open("players.txt", "w")

  for id in ids:
    page = 1
    st = None
    st = send_request(page, id)
    while not st == None:
      entries = st.split("}]}")
      entries = entries[0:-2]

      for player in entries:
        info = parse(player)
        if info == None:
          continue
        if info[1] in coveredIds:
          continue
        else:
          coveredIds.update({info[1] : info[0]})
          file.write(info[0] + " : " + info[1] + "\n")
      page += 1
      st = send_request(page, id)

  file.close()



if __name__ == "__main__":
  main()

#r = None
#r = requests.post(url, json={"query" : body, "variables" : variable}, headers=header)
#st = r.text.split("}]}")
#st = st[0:-2]



#file = open("players.txt", "w")
#print(parse(st[0]))
