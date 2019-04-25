import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import time, os

# Germany
MY_CITY = set(["Köln", "Berlin", "München", "Düsseldorf"])
url_template = "http://de.indeed.com/jobs?q=data+scientist+&l={}&start={}"
max_results_per_city = 20  # Set this to a high-value (5000) to generate more results.
# Crawling more results, will also take much longer.
# Number of pages
i = 2
results = []
df_de = pd.DataFrame(columns=["Title", "Location", "Company", "Review", "Summary"])
for city in set(["Köln", "Berlin", "München", "Düsseldorf"]):
    for start in range(0, max_results_per_city, 10):
        # Grab the results from the request (as above)
        url = url_template.format(city, start)
        # Append to the full set of results
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser", from_encoding="utf-8")
        for each in soup.find_all(class_="result"):
            try:
                title = each.find(class_="jobtitle").text.replace("\n", "")
            except:
                title = None
            try:
                location = each.find("span", {"class": "location"}).text.replace(
                    "\n", ""
                )
            except:
                location = None
            try:
                company = each.find(class_="company").text.replace("\n", "")
            except:
                company = None
            try:
                review_0 = each.find("div", attrs={"class": "sjcl"})
                review = review_2.find("div").text.replace("\n", "")
            except:
                salary = None
            try:
                summary = each.find(class_="summary").text.replace("\n", "")
            except:
                summary = None
            df_de = df_de.append(
                {
                    "Title": title,
                    "Location": location,
                    "Company": company,
                    "Review": salary,
                    "Summary": summary,
                },
                ignore_index=True,
            )
            i += 1
            if (
                i % 1000 == 0
            ):  # Ram helped me build this counter to see how many. You can visibly see Ram's vernacular in the print statements.
                print(
                    "You have "
                    + str(i)
                    + " results. "
                    + str(df_de.dropna().drop_duplicates().shape[0])
                    + " of these aren't rubbish."
                )

# csv_name = time.strftime('%Y%m%d-%H-%M%S') + '_de_'+ 'indeed.csv'
csv_name = "de_" + "indeed.csv"
df_de.to_csv(os.path.join("./data/de/", csv_name), encoding="utf-8")
