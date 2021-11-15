from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
import time
import argparse
import datetime
import pandas as pd
import nltk
from collections import defaultdict
from wordcloud import WordCloud


def pick_adjectives(row):
    adj_keys = ['JJ', 'JJR', 'JJS']
    token_words = nltk.word_tokenize(row)
    token_dict = dict(nltk.pos_tag(token_words))
    modified_token_dict = defaultdict(list)
    for k, v in token_dict.items():
        modified_token_dict[v].append(k)
    adjectives = list(map(modified_token_dict.get, adj_keys))
    adjectives = [x for x in adjectives if x is not None]
    adjectives_str = ' '.join(str(item) for sublist in adjectives for item in sublist)
    return adjectives_str


def extract_google_reviews(driver, query, number_of_reviews):
    driver.get('https://www.google.com')
    driver.find_element_by_name('q').send_keys(query)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.NAME, 'btnK'))).click()
    driver.find_elements_by_link_text("View all Google reviews")[0].click()

    all_reviews = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.gws-localreviews__google-review')))
    count = 0
    while len(all_reviews) < number_of_reviews:
        driver.execute_script('arguments[0].scrollIntoView(true);', all_reviews[-1])
        time.sleep(0.5)
        all_reviews = driver.find_elements_by_css_selector('div.gws-localreviews__google-review')
        count = count + 1
        if count == number_of_reviews:
            print("google has the following number of reviews only")
            print(len(all_reviews))
            break

    review_list = []
    for review in all_reviews:
        review_list.append(review.text)
    return review_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_keyword', action='store', dest='search_keyword',
                        help='Keyword to be searched for to fetch reviews', required=True)
    parser.add_argument('--number_of_reviews', action='store', dest='number_of_reviews',
                        help='Number of reviews to be fetched', required=True)
    args = parser.parse_args()
    print('Starting Scrapper.. fetching results from google.com...')
    print('Fetching results from google.com...')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-extensions")
    start = datetime.datetime.now()
    result = []
    search_keyword = args.search_keyword
    number_of_reviews = int(args.number_of_reviews)

    print('Getting reviews...')
    reviews = extract_google_reviews(driver, search_keyword, number_of_reviews)
    result.extend(reviews)

    print('parsing...', )
    reviewsDf = pd.DataFrame(result)
    reviewsDf.columns = ['google_review']
    reviewsDf['review_adjectives'] = reviewsDf['google_review'].apply(pick_adjectives)
    end = datetime.datetime.now()
    consolidated_adjectives = reviewsDf['review_adjectives'].str.cat(sep=' ')
    word_cloud = WordCloud(background_color='white').generate(consolidated_adjectives)
    word_cloud.to_file(search_keyword + "-Google_" + "reviews.png")

    diff = end - start
    print("Time taken to tokenise and retrieve adjectives:", diff.total_seconds(), ' seconds')