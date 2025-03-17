import pandas as pd
import json
import requests
import openpyxl
from openpyxl import Workbook

API_KEY = '3f4f3f286f868b253c7bc95b5a2d8c29'
SPORT = 'upcoming'
REGION = 'us'
MARKETS = 'h2h'
FORMAT = 'decimal'
CAPITAL = 100 #Total amount that you bet across all platforms

# API Call to Get Data
response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGION,
        'markets': MARKETS,
        'oddsFormat': FORMAT,
        'dateFormat': 'iso',
    }
)


api_data = response.json()


print(api_data)

#Example Output from Oddsbet
#[{'id': 'fcb18f7425e7f5d2f6007c97bd469ba0', 'sport_key': 'icehockey_mestis', 'sport_title': 'Mestis', 'commence_time': '2025-03-17T16:30:00Z', 'home_team': 'JoKP', 'away_team': 'IPK', 'bookmakers': [{'key': 'betrivers', 'title': 'BetRivers', 'last_update': '2025-03-17T15:05:59Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:59Z', 'outcomes': [{'name': 'IPK', 'price': 1.73}, {'name': 'JoKP', 'price': 1.97}]}]}, {'key': 'bovada', 'title': 'Bovada', 'last_update': '2025-03-17T15:06:01Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:06:01Z', 'outcomes': [{'name': 'IPK', 'price': 1.69}, {'name': 'JoKP', 'price': 2.1}]}]}]}, {'id': 'bdff37853f23d245f70318a732ba381b', 'sport_key': 'icehockey_mestis', 'sport_title': 'Mestis', 'commence_time': '2025-03-17T16:30:00Z', 'home_team': 'Kiekko-Vantaa', 'away_team': 'Jokerit', 'bookmakers': [{'key': 'betrivers', 'title': 'BetRivers', 'last_update': '2025-03-17T15:05:59Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:59Z', 'outcomes': [{'name': 'Jokerit', 'price': 1.09}, {'name': 'Kiekko-Vantaa', 'price': 5.6}]}]}, {'key': 'bovada', 'title': 'Bovada', 'last_update': '2025-03-17T15:06:01Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:06:01Z', 'outcomes': [{'name': 'Jokerit', 'price': 1.15}, {'name': 'Kiekko-Vantaa', 'price': 5.0}]}]}]}, {'id': 'c1b7eee93e130eea764303f4168c17d8', 'sport_key': 'baseball_mlb_preseason', 'sport_title': 'MLB Preseason', 'commence_time': '2025-03-17T17:05:00Z', 'home_team': 'Washington Nationals', 'away_team': 'St. Louis Cardinals', 'bookmakers': [{'key': 'draftkings', 'title': 'DraftKings', 'last_update': '2025-03-17T15:05:57Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:57Z', 'outcomes': [{'name': 'St. Louis Cardinals', 'price': 2.4}, {'name': 'Washington Nationals', 'price': 1.6}]}]}, {'key': 'betonlineag', 'title': 'BetOnline.ag', 'last_update': '2025-03-17T15:06:20Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:06:20Z', 'outcomes': [{'name': 'St. Louis Cardinals', 'price': 2.4}, {'name': 'Washington Nationals', 'price': 1.62}]}]}, {'key': 'betus', 'title': 'BetUS', 'last_update': '2025-03-17T15:05:58Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:58Z', 'outcomes': [{'name': 'St. Louis Cardinals', 'price': 2.4}, {'name': 'Washington Nationals', 'price': 1.59}]}]}, {'key': 'betmgm', 'title': 'BetMGM', 'last_update': '2025-03-17T15:05:57Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:57Z', 'outcomes': [{'name': 'St. Louis Cardinals', 'price': 2.4}, {'name': 'Washington Nationals', 'price': 1.61}]}]}, {'key': 'bovada', 'title': 'Bovada', 'last_update': '2025-03-17T15:05:58Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:58Z', 'outcomes': [{'name': 'St. Louis Cardinals', 'price': 2.4}, {'name': 'Washington Nationals', 'price': 1.6}]}]}, {'key': 'fanduel', 'title': 'FanDuel', 'last_update': '2025-03-17T15:05:28Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:28Z', 'outcomes': [{'name': 'St. Louis Cardinals', 'price': 2.38}, {'name': 'Washington Nationals', 'price': 1.59}]}]}, {'key': 'betrivers', 'title': 'BetRivers', 'last_update': '2025-03-17T15:05:57Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:57Z', 'outcomes': [{'name': 'St. Louis Cardinals', 'price': 2.45}, {'name': 'Washington Nationals', 'price': 1.56}]}]}]}, {'id': '05c68ff208163f6d9542aa64276149f6', 'sport_key': 'icehockey_sweden_allsvenskan', 'sport_title': 'HockeyAllsvenskan', 'commence_time': '2025-03-17T18:00:00Z', 'home_team': 'IF Björklöven', 'away_team': 'AIK', 'bookmakers': [{'key': 'bovada', 'title': 'Bovada', 'last_update': '2025-03-17T15:05:55Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:55Z', 'outcomes': [{'name': 'AIK', 'price': 2.15}, {'name': 'IF Björklöven', 'price': 1.67}]}]}]}, {'id': '7abe8c2eebff8a8673d140c47fa55d77', 'sport_key': 'icehockey_sweden_allsvenskan', 'sport_title': 'HockeyAllsvenskan', 'commence_time': '2025-03-17T18:00:00Z', 'home_team': 'Södertälje SK', 'away_team': 'Kalmar HC', 'bookmakers': [{'key': 'bovada', 'title': 'Bovada', 'last_update': '2025-03-17T15:05:55Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:55Z', 'outcomes': [{'name': 'Kalmar HC', 'price': 2.5}, {'name': 'Södertälje SK', 'price': 1.5}]}]}]}, {'id': '7bfa154cddd8214771228989c9b74bc3', 'sport_key': 'icehockey_sweden_hockey_league', 'sport_title': 'SHL', 'commence_time': '2025-03-17T18:00:00Z', 'home_team': 'Växjö Lakers', 'away_team': 'Örebro HK', 'bookmakers': [{'key': 'draftkings', 'title': 'DraftKings', 'last_update': '2025-03-17T15:05:54Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:54Z', 'outcomes': [{'name': 'Växjö Lakers', 'price': 1.49}, {'name': 'Örebro HK', 'price': 2.6}]}]}, {'key': 'bovada', 'title': 'Bovada', 'last_update': '2025-03-17T15:05:54Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:54Z', 'outcomes': [{'name': 'Växjö Lakers', 'price': 1.56}, {'name': 'Örebro HK', 'price': 2.5}]}]}]}, {'id': '2803d209f1ea19731a3682ee6cf99f49', 'sport_key': 'soccer_spain_segunda_division', 'sport_title': 'La Liga 2 - Spain', 'commence_time': '2025-03-17T19:30:00Z', 'home_team': 'CD Castellón', 'away_team': 'Deportivo La Coruña', 'bookmakers': [{'key': 'fanduel', 'title': 'FanDuel', 'last_update': '2025-03-17T15:05:05Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:05Z', 'outcomes': [{'name': 'CD Castellón', 'price': 2.0}, {'name': 'Deportivo La Coruña', 'price': 3.5}, {'name': 'Draw', 'price': 3.3}]}]}, {'key': 'bovada', 'title': 'Bovada', 'last_update': '2025-03-17T15:05:25Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:25Z', 'outcomes': [{'name': 'CD Castellón', 'price': 2.1}, {'name': 'Deportivo La Coruña', 'price': 3.35}, {'name': 'Draw', 'price': 3.3}]}]}, {'key': 'draftkings', 'title': 'DraftKings', 'last_update': '2025-03-17T15:05:24Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:24Z', 'outcomes': [{'name': 'CD Castellón', 'price': 2.05}, {'name': 'Deportivo La Coruña', 'price': 3.5}, {'name': 'Draw', 'price': 3.45}]}]}, {'key': 'betmgm', 'title': 'BetMGM', 'last_update': '2025-03-17T15:05:54Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:54Z', 'outcomes': [{'name': 'CD Castellón', 'price': 2.05}, {'name': 'Deportivo La Coruña', 'price': 3.25}, {'name': 'Draw', 'price': 3.3}]}]}, {'key': 'betus', 'title': 'BetUS', 'last_update': '2025-03-17T15:05:25Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:25Z', 'outcomes': [{'name': 'CD Castellón', 'price': 2.05}, {'name': 'Deportivo La Coruña', 'price': 3.4}, {'name': 'Draw', 'price': 3.4}]}]}, {'key': 'betonlineag', 'title': 'BetOnline.ag', 'last_update': '2025-03-17T15:05:53Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:53Z', 'outcomes': [{'name': 'CD Castellón', 'price': 2.03}, {'name': 'Deportivo La Coruña', 'price': 3.25}, {'name': 'Draw', 'price': 3.45}]}]}, {'key': 'lowvig', 'title': 'LowVig.ag', 'last_update': '2025-03-17T15:06:16Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:06:16Z', 'outcomes': [{'name': 'CD Castellón', 'price': 2.04}, {'name': 'Deportivo La Coruña', 'price': 3.25}, {'name': 'Draw', 'price': 3.45}]}]}]}, {'id': '2387f48c67ed7d9726c2f63757273199', 'sport_key': 'lacrosse_ncaa', 'sport_title': 'NCAA Lacrosse', 'commence_time': '2025-03-17T20:00:00Z', 'home_team': 'Villanova Wildcats', 'away_team': 'Brown Bears', 'bookmakers': [{'key': 'draftkings', 'title': 'DraftKings', 'last_update': '2025-03-17T15:05:58Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:58Z', 'outcomes': [{'name': 'Brown Bears', 'price': 1.77}, {'name': 'Villanova Wildcats', 'price': 2.0}]}]}, {'key': 'fanduel', 'title': 'FanDuel', 'last_update': '2025-03-17T15:04:46Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:04:46Z', 'outcomes': [{'name': 'Brown Bears', 'price': 1.82}, {'name': 'Villanova Wildcats', 'price': 2.0}]}]}, {'key': 'betmgm', 'title': 'BetMGM', 'last_update': '2025-03-17T15:05:58Z', 'markets': [{'key': 'h2h', 'last_update': '2025-03-17T15:05:58Z', 'outcomes': [{'name': 'Brown Bears', 'price': 1.8}, {'name': 'Villanova Wildcats', 'price': 2.05}]}]}]}]

def find_arbitrage(events):
    arbitrage_bets = []

    for event in events:
        sport = event['sport_key']
        event_id = event['id']
        home_team = event['home_team']
        away_team = event['away_team']
        date = event['commence_time']
      
        best_odds = {}

        #Go through each bookmaker for best odds
        for bookmaker in event['bookmakers']:
          for market in bookmaker['markets']:
            if market['key'] == 'h2h':
              for outcome in market['outcomes']:
                team = outcome['name']
                odds = outcome['price']

                if team not in best_odds or best_odds[team]['odds'] <  odds:
                  best_odds[team] = {'odds': odds, 'bookmaker': bookmaker['title']}
    
        if len(best_odds) < 2:
          continue

        implied_probs = {team: 1 / best_odds[team]['odds'] for team in best_odds}
        total_implied_prob = sum(implied_probs.values())

        if total_implied_prob < 1:
          bet_allocation = {}
          for team in best_odds:
            bet_allocation[team] = (CAPITAL * implied_probs[team])/total_implied_prob

          profit_percentage = (1 - total_implied_prob) * 100

          arbitrage_bets.append({
            'Event ID': event_id,
            'Sport': sport,
            'Date': date,
            'Match': f"{home_team} vs {away_team}",
            'Best Bets':[
              {
                'Team': team,
                'Bookmaker': best_odds[team]['bookmaker'],
                'Odds': best_odds[team]['odds'],
                'Bet Amount': round(bet_allocation[team], 2),
              }
              for team in best_odds
            ],
            'Guaranteed Profit': round(profit_percentage, 2),
          })
    return arbitrage_bets

arbitrage_results = find_arbitrage(api_data)

# Display Results in Terminal
if arbitrage_results:
    print("\nArbitrage Opportunities Found:")
    for result in arbitrage_results:
        print(f"\nEvent: {result['Match']} ({result['Sport']})")
        print(f"Guaranteed Profit: {result['Guaranteed Profit']}%")
        for bet in result['Best Bets']:
            print(f"  - Bet on {bet['Team']} with {bet['Bookmaker']} at {bet['Odds']} odds")
            print(f"    Bet Amount: ${bet['Bet Amount']}")
else:
    print("\nNo arbitrage opportunities found.")



# Export to Excel
wb = Workbook()
ws = wb.active
ws.title = "Arbitrage Bets"

# Write headers
headers = ["Event ID", "Date", "Sport", "Match", "Team", "Bookmaker", "Odds", "Bet Amount", "Guaranteed Profit"]
ws.append(headers)

# Write data
for result in arbitrage_results:
    for bet in result['Best Bets']:
        ws.append([
            result['Event ID'], result['Date'], result['Sport'], result['Match'],
            bet['Team'], bet['Bookmaker'], bet['Odds'], bet['Bet Amount'], result['Guaranteed Profit']
        ])
    ws.append([])  # Adds a blank row after each outer loop iteration

# Save the Excel file
wb.save("arbitrage_bets.xlsx")
print("\nArbitrage opportunities exported to 'arbitrage_bets.xlsx'.")

  