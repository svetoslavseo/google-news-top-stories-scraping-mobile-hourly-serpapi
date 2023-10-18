import pandas as pd
import requests
import time
from datetime import datetime

# Load the keywords to search for
def load_keywords(path):
    with open(path, 'r') as file:
        return file.read().splitlines()

# Fetch the top stories for a given keyword using SERP API
def fetch_top_stories(keyword, api_key):
    url = f'https://serpapi.com/search.json?q={keyword}'
    params = {
        'api_key': api_key,
        'device': 'mobile',
        'gl': 'us',
        'hl': 'en',
        'google_domain': 'google.com',
        'location_used': 'New York,New York,United States',
        'location_requested': 'New York,New York,United States',
        'engine': 'google',
        'no_cache': 'true'
    }
    response = requests.get(url, params=params)
    return response.json()

# Main function to execute the script
def main(api_key, keyword_file_path, output_file):
    keywords = load_keywords(keyword_file_path)
    results_df = pd.DataFrame(columns=['Keyword', 'Link', 'Date', 'Live', 'Search Metadata'])

    while True:  # This will make the script run indefinitely, every hour
        for keyword in keywords:
            data = fetch_top_stories(keyword, api_key)
            search_metadata = data.get('search_metadata', {}).get('created_at', 'N/A')
            rows = []

            if 'top_stories' in data:
                # Extract data based on 'carousel' or 'text'
                stories_type = 'carousel' if 'carousel' in data['top_stories'] else 'text'
                for story in data['top_stories'].get(stories_type, []):
                    link = story['link']
                    date = story['date']
                    live = story.get('live', None)
                    rows.append({'Keyword': keyword, 'Link': link, 'Date': date, 'Live': live, 'Search Metadata': search_metadata})

            else:
                print(f"No top stories found for keyword: {keyword}")
                rows.append({'Keyword': keyword, 'Link': "not found", 'Date': 'N/A', 'Live': 'N/A', 'Search Metadata': 'N/A'})

            # Append the rows to results_df
            results_df = pd.concat([results_df, pd.DataFrame(rows)], ignore_index=True)

            # Drop rows with duplicate values in all columns
            results_df.drop_duplicates(keep='first', inplace=True)

        # Save the updated dataframe to the CSV file
        results_df.to_csv(output_file, index=False)

        # Print the time of the last crawl
        current_date = datetime.now()
        print("last scrape =", current_date)

        # Wait for one hour
        time.sleep(3600)

if __name__ == "__main__":
    API_KEY = '0be5a8a7a43ab2609f37cd1876314f0efda10b978b42ad44153f7c87ff8c2648'  # TODO: Replace with your method to retrieve the API key securely.
    KEYWORDS_FILE_PATH = '/Users/svetoslav.petkov/PycharmProjects/pythonProject2/Top Stories Scraping/NFL/week-5/predictions-kws-week5 - Sheet1.csv'  # You can adjust this path based on your directory structure.
    OUTPUT_FILE = '/Users/svetoslav.petkov/PycharmProjects/pythonProject2/Top Stories Scraping/NFL/week-5/RESULT-week5.csv'

    main(API_KEY, KEYWORDS_FILE_PATH, OUTPUT_FILE)
