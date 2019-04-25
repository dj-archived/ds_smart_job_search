import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import time, os

#MY_CITY = 'Washington%2C+DC'
MY_CITY =set(['New+York', 'San+Francisco',  'Boston'])

url_template = 'http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l={}&start={}'
max_results_per_city = 20 # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer.
# Number of pages
i = 2
results = []
df_us = pd.DataFrame(columns=['Title','Location','Company','Review','Summary'])
for city in MY_CITY:
    for start in range(0, max_results_per_city, 10):
        # Grab the results from the request (as above)
        url = url_template.format(city, start)
        # Append to the full set of results
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser', from_encoding='utf-8')
        for each in soup.find_all(class_= 'result' ):
            try:
                title = each.find(class_='jobtitle').text.replace('\n', '')
            except:
                title = None
            try:
                location = each.find('span', {'class':'location' }).text.replace('\n', '')
            except:
                location = None
            try:
                company = each.find(class_='company').text.replace('\n', '')
            except:
                company = None
            try:
                review_0 = each.find('div', attrs={'class':'sjcl'})
                review = review_2.find('div').text.replace('\n', '')
            except:
                salary = None
            try:
                summary = each.find(class_='summary').text.replace('\n', '')
            except:
                summary = None
            df_us = df_us.append({'Title':title, 'Location':location, 'Company':company, 'Review':salary,'Summary':summary}, ignore_index=True)
            i += 1
            if i % 1000 == 0:  # Ram helped me build this counter to see how many. You can visibly see Ram's vernacular in the print statements.
                print('You have ' + str(i) + ' results. ' + str(df_us.dropna().drop_duplicates().shape[0]))

# Seperate city and State
df_us.to_csv('./data/us/Indeed_df_us_raw.csv', encoding='utf-8')
df_us = pd.read_csv('./data/us/Indeed_df_us_raw.csv')
df_us.drop('Unnamed: 0', axis=1, inplace=True)

df_us = df_us.join(df_us['Location'].str.split(',', 1, expand=True).rename(columns={0:'City', 1:'State'}))

def strip_state(x):
    if x != None:
        return x[0:3]
    else:
        None
df_us['State Initials'] = df_us['State'].apply(strip_state)
df_us.head()
# Save to /data/us
#csv_name = time.strftime('%Y%m%d-%H-%M%S') + '_us_'+ 'indeed.csv'

csv_name = 'us_'+ 'indeed.csv'
df_us.to_csv(os.path.join('./data/us/',csv_name), encoding='utf-8')

filename = './data/us/Indeed_df_us_raw.csv'
try:
    os.remove(filename)
except OSError:
    pass
