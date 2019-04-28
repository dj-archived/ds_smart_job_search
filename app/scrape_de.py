import urllib
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re
import time, os
################################################################################

# The scraping function
def scrape_indeed_de(url_template, Cities,max_results_per_city,i):
    df_de = pd.DataFrame(columns=["Title", "Location", "Company", "Review", "Summary"])
    for city in Cities:
        for start in range(0, max_results_per_city, 1):
        # Grab the results from the request (as above)
            url = url_template.format(city, start)
        # Append to the full set of results
            html = requests.get(url)
            soup = BeautifulSoup(html.content, "html.parser", from_encoding="UTF-8")
            for each in soup.find_all(class_="result"):
                try:
                    title = each.find(class_="jobtitle").text.replace("\n", "")
                except:
                    title = None
                try:
                    location = each.find("span", {"class": "location"}).text.replace("\n", "")
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
                        + " of these are unique results")

# csv_name = time.strftime('%Y%m%d-%H-%M%S') + '_de_'+ 'indeed.csv'
    txt_name = "de_" + "indeed.txt"
    df_de.to_csv(os.path.join("./data/", txt_name),sep="\t",index=False)
    return df_de.head(2)
################################################################################
# Variables
# Germany
url_de = "http://de.indeed.com/jobs?q=data+scientist+&l={}&start={}"
#My_City = set(["Köln", "Berlin", "München", "Düsseldorf"])
My_City = set(["Cologne", "Berlin", "Munich", "Dusseldorf"])
max_results_my_city = 20
# Number of pages
page = 2

# Call function
scrape_indeed_de(url_de, My_City,max_results_my_city,page)
################################################################################
