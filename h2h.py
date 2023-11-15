import re
import requests

#sends graphql request to api
def send_request(page, id):
  url = "https://api.start.gg/gql/alpha"
  header = {"Authorization" : "Bearer eff61c135e0546f45dbc554c02ee761d"}

  body = """
  query Sets ($playerId: ID!, $page: Int!, $perPage: Int!){
  player(id: $playerId) {
    sets(perPage: $perPage, page: $page) {
      nodes {
        displayScore
        }
      }
    }
  }
  """

  variable = {
  "playerId": id,
  "page": page,
  "perPage": 400
  }

  r = requests.post(url, json={"query" : body, "variables" : variable}, headers=header)
  if re.search("\"nodes\":\[\]", r.text):
    return None
  return r.text

#Given a scoreline for a set, determine winner and loser, return true for won set, false for loss
def parse_win_string(name, scoreline):
    #filters out doubles sets
    if re.search("(/ " + name + ")|(" + name + " /)|(" + name + r" \\)", scoreline):
       return None
    
    #filters out crewbattles
    if re.search("\ATeam", scoreline):
      return None
    
    #print(scoreline)

    search = re.search(name + " [0-9]", scoreline).span()
    score = scoreline[search[1] - 1]
    if score == "W" or score == "L":
       return None
    score = int(score)
    for num in re.findall(" [0-9]", scoreline):
       num = int(num)
       if num < score:
          #print("TRUE")
          return True
    
    #print("false")
    return False

#used to write sets between players to a file, used to test
def print_sets(name, opp, text):
   text = text.split("displayScore\":\"")
   f = open(name + ".txt", "a")
   text = text[1:]
   for entry in text:
      scoreline = entry.split("\"")[0]
      if re.search(opp, scoreline):
         f.write(scoreline + "\n")
   f.close()



def count_wins(id, name1, name2):
    page = 1
    st = None
    st = send_request(page, id)
    winCount = 0
    lossCount = 0
    while not st == None:
      #printSets(name1, name2, st)
      entries = re.split("displayScore", st)
      entries = entries[1:]
      #look through list of sets, check if name2 in scoreline, if so parse who won, adding to respective counter
      for e in entries:
         winstring = e[3:]
         winstring = winstring.split("\"")[0]
         if re.search(name2 + " ", e):
            win = parse_win_string(name1, winstring)
            if win == None:
               continue
            elif win:
               winCount += 1
            else:
               lossCount += 1

      #increment page, continue loop
      page += 1
      st = send_request(page, id)
    return (winCount, lossCount)

#browses through players.txt to find entered player name and id
def main():
    name1 = input("Enter player name\n")
    name2 = input("Enter opponent name\n")

    #name1 = "Mang0"
    #name2 = "Zain"

    #compile regexes for names given
    re1 = re.compile("\A" + name1 + " : [0-9]+")
    re2 = re.compile("\A" + name2 + " : [0-9]+")

    file = open("players.txt", "r")

    id1 = -1
    id2 = -1

    #iterate through file, match name in list of ids, fetch ids for respective players
    with file as f:
        for line in f:
            if re1.search(line):
                text1 = line[len(name1) + 3:]
                id1 = int(text1)
            if re2.search(line):
                text2 = line[len(name2) + 3:]
                id2 = int(text2)
            #if both ids found, break loop (so i can order names by importance [maybe using ranking system?])
            if not (id1 == -1 or id2 == -1):
                break
    wins, losses = count_wins(id1, name1, name2)
    print("Wins: " + str(wins) + "Losses: " + str(losses))
    file.close()


if __name__ == "__main__":
    main()