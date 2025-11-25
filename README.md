Final Project – Airbnb Market Simulation & Data Analysis
This project contains two independent but complementary parts:
Part 1 — A market simulation implemented in Python (City, Hosts, Places).
Part 2 — A real-data analysis using Barcelona and Madrid Airbnb datasets.
Both components explore how prices, availability, and host behaviour shape an Airbnb-style housing market.
## Part 1 — Market Simulation
We simulate an Airbnb-style housing market on a 10×10 grid.
Each property (Place), owned by a Host, participates in a monthly cycle where:
Prices evolve depending on area-level averages
Places compete for occupancy
Hosts accumulate profits from occupied properties
Hosts may reinvest and acquire new properties
Adjacent properties influence bidding behaviour
Market-clearing determines which bids succeed
The simulation includes an optional rule modification to study how small behavioural changes affect market concentration and wealth inequality.
✔ Graph 1 — Wealth Distribution
Shows total wealth of all hosts (profits + current property values) after 180 months.
✔ Graph 2_v0 — Original Rule
Distribution of the number of assets per host using the unmodified rule.
✔ Graph 2_v1 — Modified Rule
We changed the rule by introducing a probabilistic bias toward acquiring additional properties.
This increases market inequality and results in greater asset concentration, clearly visible in the graph.
## Part 2 — Data-Driven Analysis
We use real Airbnb public datasets from InsideAirbnb.
Datasets used
1. Barcelona listings
Source:
https://data.insideairbnb.com/spain/catalonia/barcelona/latest/data/listings.csv.gz
Local file: data/bcn_listings.csv
2. Madrid listings
Source:
https://data.insideairbnb.com/spain/madrid/madrid/latest/data/listings.csv.gz
Local file: data/madrid_listings.csv
Additional datasets (availability)
Used to study seasonal patterns:
bcn_calendar.csv
madrid_calendar.csv
Analysis Steps
Cleaned and normalized price
Fixed the minimum_nights inconsistency in Madrid
Focused on Entire home/apt units with 2–6 guests
Selected relevant neighbourhoods
Computed price per person
Compared Barcelona vs. Madrid
Added seasonal availability analysis using the calendar files
Graph 3 — Median Price per Person
A direct visual comparison of Barcelona and Madrid shows:
Clear and consistent price differences
Barcelona is more expensive per person across almost all accommodation sizes
Differences remain even after cleaning and filtering
Extra Graphs — Calendar Availability
Using the calendar datasets:
Monthly mean availability for Barcelona
Monthly mean availability for Madrid
A combined comparison figure
These graphs illustrate seasonal patterns and booking behaviour in both markets.
## Conclusion
This project combines:
A custom-built simulation of host behaviour and market dynamics
A real-world data analysis of prices and availability
A comparison of two major Airbnb markets in Spain
The results show both structural inequalities in simulated markets and clear pricing/seasonality differences in real Airbnb data.
## Project Structure
project/
├── data/
├── notebooks/
├── reports/
├── src/final_project/
├── main.py
├── pyproject.toml
└── README.md
