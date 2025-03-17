import pandas as pd
import json
import requests
import openpyxl
from openpyxl import Workbook

API_KEY = 'apikey' #Please note that to run this program you will need your API key: https://the-odds-api.com/
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

  
