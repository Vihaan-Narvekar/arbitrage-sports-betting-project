# Arbitrage Method for Sports Betting
I made this project in March 2025. Typically odds across different sports betting sites differ slightly. Individuals can take advantage of them by hedging all positions in a sports event on two different platforms with distinct odds in such a way as to make a profit.

To collect data regarding the odds associated with each event, I used **The Odds API** (https://the-odds-api.com/), an open-source software that offers initial free credits. This API has allowed me to determine what the odds are on any sporting event (https://the-odds-api.com/sports-odds-data/sports-apis.html) on a variety of bookmakers. Once I compiled all relevant data from the API, the program will organize the data and compare odds across the several bookmakers to determine if there is an arbitrage opportunity.

If there is an arbitrage opportunity, then the program will output the associated event(s), profit percentage(s), and how much of capital to allocate per team per bookmaker (assuming total capital allocations of 100). It will do this multiple times if it finds multiple opportunities within the data.

All of the code is included in betmaker.py. There are relevant comments describing what each part of the code does. Please note that some arbitrage opportunities do arise during live games, but the Odds API is running on a slight delay so the **odds are subject to change** when viewed on the bookmaker's website. 

IMPORTANT: To use this program, you will need to have your own API code. It is free to get from The Odds' website (linked above). Once retrieved, replace the text in the variable "API_KEY" in the file **betmaker.py**.


