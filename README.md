# Wordcloud using Google Reviews

The script accepts a search keyword as an input, extract the adjectives from the google reviews and create a wordcloud

# Usage

The script requires two parameters as an input:
- `--search_keyword`: Keyword to be searched for to fetch reviews
- `--number_of_reviews`: Number of reviews to be fetched

Example:

`python reviews_scraper.py --search_keyword "name_of_company_or_local_establishment" --number_of_reviews 30`

Output:

Will create a jpg file which will be a wordcloud using all the adjectives extracted from the google reviews
