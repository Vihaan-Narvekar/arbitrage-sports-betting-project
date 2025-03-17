import pandas as np
import json
import httpx

#API KEY
key = open('API_KEY.txt', 'r')
API_KEY = key.read()
key.close()

#Constants
sport = 'basketball_nba'
regions = 'us'
markets = 'h2h'
format = 'decimal'
capital = 100
# API Call to Get Data
api_data = httpx.get(
    'https://api.the-odds-api.com/v4/sports/{sport}/odds',
    params={'apiKey': API_KEY, 'regions': regions, 'markets': markets, 'spreads&oddsFormat': format}
).json()


#Example Output from Oddsbet
"""
[{'id': '3334a39ac46322911bb2cc9243e387ee',
  'sport_key': 'baseball_mlb',
  'sport_title': 'MLB',
  'commence_time': '2022-09-18T16:11:45Z',
  'home_team': 'Detroit Tigers',
  'away_team': 'Chicago White Sox',
  'bookmakers': [{'key': 'bovada',
    'title': 'Bovada',
    'last_update': '2022-09-18T18:57:38Z',
    'markets': [{'key': 'h2h',
      'outcomes': [{'name': 'Chicago White Sox', 'price': 1.0},
       {'name': 'Detroit Tigers', 'price': 19.0}]}]},
"""


app =  FirecrawlApp(api_key = "fc-a02c9f1a5fae4fde814595e2214276ac")

class GameSchema(BaseModel):
    team_1_name: str
    team_2_name: str
    team_1_moneyline: int
    team_2_moneyline: int
    date_of_game: str

class ExtractSchema(BaseModel):
    total_games: int
    games: List[GameSchema]  # Store multiple games


# Scrapes DraftKings to get all MoneyLine Bets
def get_draftkings_odds():
    #Scrapes DraftKings for basketball moneyline odds for all events.
    data = app.extract(['https://sportsbook.draftkings.com/leagues/basketball/nba'], {
        'prompt': 'Group all matches together. Extract the moneyline odds for each all games, for each team. Extract the moneyline odds for both teams, the teams involved, and the date the event takes place for all events on the page. Please insured that multiple games with multiple teams are scraped.',
    'schema': ExtractSchema.model_json_schema(),})

    if 'data' in data:
        events = data['data']  # Assuming 'data' contains a list of events
    return events  # Check the structure of 'events'

def get_fanduel_odds():
    #Scrapes DraftKings for basketball moneyline odds for all events,
    data = app.extract(['https://sportsbook.fanduel.com/navigation/nba'], {'prompt': 'Group all matches together. Extract the moneyline odds for each all games (it may be fractional as well), for each team. Extract the moneyline or fractional odds for both teams, the teams involved, and the date the event takes place for all events on the page. It may take some time for the data to load',
    'schema': ExtractSchema.model_json_schema(),})

    if 'data' in data:
        events = data['data']
    
    return events

def fractional_to_decimal(fractional_odds):
    """Converts fractional odds (e.g. 5/6) to decimal."""
    num, denom = map(int, fractional_odds.split('/'))
    return (num / denom) + 1

def american_to_decimal(american_odds):
    """Converts American odds (e.g. +150 or -200) to decimal."""
    american_odds = int(american_odds)
    if american_odds > 0:
        return (american_odds / 100) + 1
    else:
        return (100 / abs(american_odds)) + 1
    
 
def calculate_arbitrage(odds1, odds2):
    """Checks if there's an arbitrage opportunity between two odds."""
    implied_prob1 = 1 / odds1
    implied_prob2 = 1 / odds2
    total_prob = implied_prob1 + implied_prob2
    
    if total_prob < 1:
        return True, total_prob
    return False, total_prob

def find_closest_match(team_name, choices, threshold=80):
    """Finds the closest match for a team name from a list using fuzzy matching."""
    match, score = process.extractOne(team_name, choices)
    return match if score >= threshold else None


#Main function to find arbitrage opportunities only for matching basketball events.
def find_arbitrage(fanduel_odds, draftking_odds):
    # Extract unique team names from both sportsbooks
    fanduel_teams = set()
    for game in fanduel_odds['games']:
        fanduel_teams.add(game['team_1_name'])
        fanduel_teams.add(game['team_2_name'])

    draftking_teams = set()
    for game in draftking_odds['games']:
        draftking_teams.add(game['team_1_name'])
        draftking_teams.add(game['team_2_name'])

    # Create a team name mapping
    team_name_mapping = {team: find_closest_match(team, draftking_teams) for team in fanduel_teams}
    

    # Build a dictionary of DraftKings games with mapped team names
    draftking_events = {}
    for game in draftking_odds['games']:
        team_1 = game['team_1_name']
        team_2 = game['team_2_name']
        mapped_team_1 = find_closest_match(team_1, fanduel_teams)
        mapped_team_2 = find_closest_match(team_2, fanduel_teams)

        if mapped_team_1 and mapped_team_2:
            key = (game['date_of_game'], mapped_team_1, mapped_team_2)
            draftking_events[key] = {
                'team_1_moneyline': game['team_1_moneyline'],
                'team_2_moneyline': game['team_2_moneyline']
            }

    arbitrage_opportunities = []

    # Iterate through Fanduel games and find the corresponding DraftKings game
    for game in fanduel_odds['games']:
        date = game['date_of_game']
        team_1 = game['team_1_name']
        team_2 = game['team_2_name']
        mapped_team_1 = team_name_mapping.get(team_1)
        mapped_team_2 = team_name_mapping.get(team_2)

        if mapped_team_1 and mapped_team_2:
            key = (date, mapped_team_1, mapped_team_2)

            if key in draftking_events:
                fanduel_team_1_odds = game['team_1_moneyline']
                fanduel_team_2_odds = game['team_2_moneyline']
                draftking_team_1_odds = draftking_events[key]['team_1_moneyline']
                draftking_team_2_odds = draftking_events[key]['team_2_moneyline']


                fanduel_team_1_prob = 1/american_to_decimal(fanduel_team_1_odds)
                fanduel_team_2_prob = 1/american_to_decimal(fanduel_team_2_odds)
                draftking_team_1_prob = 1/american_to_decimal(draftking_team_1_odds)
                draftking_team_2_prob = 1/american_to_decimal(draftking_team_2_odds)

                print(fanduel_team_1_prob)
                print(fanduel_team_2_prob)
                print(draftking_team_1_prob)
                print(draftking_team_2_prob)

                # Check for arbitrage
                if min(fanduel_team_1_prob, draftking_team_1_prob) + min(draftking_team_2_prob, fanduel_team_2_prob) < 2:
                    arbitrage_opportunities.append({
                        "date": date,
                        "matchup": f"{mapped_team_1} vs {mapped_team_2}",
                        "best_team_1_odds": fanduel_team_1_odds,
                        "best_team_2_odds": draftking_team_2_odds,
                        "total_implied_probability": fanduel_team_1_prob + draftking_team_2_prob
                    })

    return arbitrage_opportunities





if __name__ == "__main__":
    odds_1 = get_fanduel_odds()
    odds_2 = get_draftkings_odds()
    find_arbitrage(odds_1, odds_2)


