Part 1 — Market Simulation
We simulate an Airbnb-style housing market on a 10×10 grid.
Each property (Place), owned by a Host, competes for occupancy and participates in a monthly bidding system.
The simulation includes:
Dynamic occupancy depending on area price averages
Host profits and reinvestment
Adjacent-property bidding
Market-clearing with bid competition
Wealth accumulation
A rule modification (to test market sensitivity)
Graph 1 – Wealth distribution
Shows final host wealth after 180 months.
Graph 2_v0 – Original rule
Distribution of assets under the unmodified bidding rule.
Graph 2_v1 – Modified rule
We changed the rule ____________
(and can explain briefly in presentation).
This produced higher concentration, visible in the graph.
Part 2 — Data-Driven Analysis
Datasets used:
Dataset 1 – Barcelona (InsideAirbnb)
https://data.insideairbnb.com/spain/catalonia/barcelona/latest/data/listings.csv.gz
(Our local file: data/bcn_listings.csv)
Dataset 2 – Madrid (InsideAirbnb)
https://data.insideairbnb.com/spain/madrid/madrid/latest/data/listings.csv.gz
(Our local file: data/madrid_listings.csv)
Additional datasets
bcn_calendar.csv
madrid_calendar.csv
(for availability seasonal analysis)
Analysis steps
Cleaned price variable
Cleaned minimum_nights in Madrid
Focused on Entire home/apt, 2–6 guests
Selected meaningful neighbourhoods
Computed price per person
Compared Barcelona vs Madrid
Graph 3 – Median price per person
Clear difference between both cities depending on accommodation size.
Extra Graphs – Availability 
Seasonal availability for both cities using calendar datasets