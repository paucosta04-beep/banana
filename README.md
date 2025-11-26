Final Project — Airbnb Market Simulation & Data Analysis
This project contains two independent but complementary parts:

Part 1 — Market Simulation (Python)

We simulate an Airbnb-style housing market on a 10×10 grid, where each host owns one or more properties ("places").
Each month, hosts compete in a bidding system to acquire adjacent properties and increase profits.

Components
City: the grid and global environment
Hosts: each with profits, bidding rules, and assets
Places: individual properties with occupancy and price history

Mechanisms Included
Dynamic occupancy depending on area price averages
Host profits and reinvestment cycles
Adjacent-property bidding system
Market clearing under competition
Wealth accumulation
One modified rule to test market sensitivity  

Part 1 — Graphs & Interpretation
Graph 1 — Wealth Distribution After 180 Months
Shows total wealth of all hosts (sorted), including:
cumulative profits
last recorded price of all owned properties
Interpretation:
The market naturally becomes highly unequal: a few hosts concentrate most of the wealth, while the majority remain at lower levels.
Graph 2 (v0) — Asset Distribution, Original Rule
Distribution of the number of properties (assets) per host before modifying the bidding rules.
Interpretation:
Most hosts own 1–2 assets, only a few own 4–5.
Inequality exists but is moderate.
Graph 2 (v1) — Asset Distribution, Modified Rule
After changing one rule in the bidding system.
Interpretation:
The modified rule causes:
more hosts with zero assets
more hosts accumulating 3+ assets
extreme cases with 8–9 assets
Conclusion:
The rule amplifies inequality: winners win more; losers drop out of the asset market.

Part 2 — Data Analysis (Barcelona vs Madrid)
Datasets Used
InsideAirbnb:
bcn_listings.csv
madrid_listings.csv
bcn_calendar.csv
madrid_calendar.csv
Focus:
- Entire home/apt
- 2–6 guests
- Price per person
- Monthly availability
Part 2 — Graphs & Interpretation
Graph 3 — Price per Person: Barcelona vs Madrid
Shows the median price per person for different accommodation sizes.
Interpretation:
Barcelona is consistently more expensive for every guest capacity.
Madrid prices drop sharply as group size increases (more competitive for large groups).
Barcelona remains more stable and high priced.
Graph 4 — Average Monthly Availability
Proportion of available days per month based on calendar.csv.
Interpretation:
Barcelona shows a strong seasonal pattern: lower availability during summer → high tourism.
Madrid is more stable year-round, with fewer extreme fluctuations.
September–October recover availability in both cities.
Overall Conclusions
The simulated market (Part 1) naturally evolves toward inequality, and modifying rules can accelerate or slow this effect.
Barcelona is a more expensive market per person than Madrid for entire apartments.
Madrid offers cheaper large-group options.
Availability trends show that Barcelona is more tourism-driven, while Madrid has more stable demand.

Datasets (Inside Airbnb downloads)
- Barcelona listings (June 2025): https://data.insideairbnb.com/spain/catalonia/barcelona/2025-06-26/data/listings.csv.gz
- Barcelona calendar (June 2025): https://data.insideairbnb.com/spain/catalonia/barcelona/2025-06-26/data/calendar.csv.gz
- Madrid listings (June 2025): https://data.insideairbnb.com/spain/community-of-madrid/madrid/2025-06-27/data/listings.csv.gz
- Madrid calendar (June 2025): https://data.insideairbnb.com/spain/community-of-madrid/madrid/2025-06-27/data/calendar.csv.gz

Rule change snippet (Part 1)
- Original (commented in `src/final_project/hosts.py`): each host bids using 100% of its profits on any adjacent listing.
- Modified (active in graph2_v1): host only bids if the target listing’s nightly rate is at or below the area’s average rate (buys “cheap” neighbors).
```python
# original rule
# if self.profits >= ask_price:
#     spread = self.profits - ask_price
#     bids.append({... "bid_price": self.profits})

# modified rule (active in v1)
if place.rate > area_mean_rate:
    continue  # skip expensive neighbor
budget = self.profits * self.bid_spend_fraction  # here 1.0
if budget >= ask_price:
    spread = budget - ask_price
    bids.append({... "bid_price": budget})
```
Effect we expected: forcing hosts to buy only “below-average” listings should let more owners acquire something, reducing concentration. Graphs `reports/graph2_v0.png` (original) vs `graph2_v1.png` (modified) show the assets-per-host distribution.
