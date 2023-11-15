#Description
This program is used to calculate head-to-head records between Super Smash Bros. Melee players, with information gathered from the start.gg API. It sends GraphQL requests to the API, parses through the responses, and returns the win/loss record of the player in question. It does not take into account performances in doubles sets or crew battles.

#How to run
In order to get head-to-head records, run h2h.py. It will then prompt for player names, make sure that the player names are spelled properly in order to ensure functionality.

This requires players.txt in order to function. In order to get another copy of this file, you can run GetPlayerIds.py, which will grab all players that entered in the most prestigious tournaments and create a new players.txt.
