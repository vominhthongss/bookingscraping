***How to run
1. cd bookingscraping
2. Example: You want to crawl all hotels in Antalya, run command:
scrapy crawl bookingscraping -a city="[city]" -o ./[yourpath]/[name of file].csv
=>> scrapy crawl bookingscraping -a city="Antalya" -o ./data/antalya.csv