from bs4 import BeautifulSoup
import requests
import csv
import html_to_json
from bs4 import NavigableString
import gc

def substring_after(s, delim):
    return s.partition(delim)[2]

def insertFile(allArray): 
    try:
        with open('course.csv', 'w+', newline='') as file:
            myFields = ['title', 'location', 'description', 'details', 'sub_title']
            writer = csv.DictWriter(file, fieldnames=myFields)    
            writer.writeheader()
            
            for i in range(len(allArray)):
                writer.writerow({'title' : allArray[i]['title'], 'sub_title': allArray[i]['sub_title'], 'location': allArray[i]['location'] , 'description': allArray[i]['description'] , 'details': allArray[i]['details']})
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def scrapper():
    try: 
        courseraUrl = "https://boards.greenhouse.io/embed/job_board?for=coursera" 

        page = requests.get(courseraUrl)

        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup)
        # found = soup.findAll("section")
        allArray = []
        for find in soup.find_all("section"):
            title = find.find("h3",text=True)
            if title is None: 
                continue
            find_all = find.findAll("div", {'class': "opening"})
            
            for each in find_all: 
                try: 
                    foundLink = each.find("a", {'target': "_top"})
                    link = foundLink.get('href')
                    token = substring_after(link, "gh_jid")
                    details_url = "https://boards.greenhouse.io/embed/job_app?for=coursera&token" + token
                    det_page = requests.get(details_url)
                
                    soup_details = BeautifulSoup(det_page.text, 'html.parser')
                    job_dict = {}
                    sub_title = find.find("h4",text=True)

                    job_dict["title"] = ''.join(title.findAll(text=True))
                    if sub_title is not None:
                        job_dict["sub_title"] = ''.join(sub_title.findAll(text=True))
                    else: 
                        job_dict["sub_title"] = ''

                    location = each.find("span", {'class': "location"},text=True)
                    job_dict["location"] = ''.join(location.find(text=True))

                    description = each.find("a",text=True)
                    job_dict["description"] = ''.join(description.find(text=True))
                

                    job_desc = soup_details.find(id='content')
                    job_dict["details"] = ''.join(job_desc.findAll(text=True))
                    allArray.append(job_dict)
                    insertFile(allArray)
                    gc.collect()
                except: 
                    print("err")
        print("PRINT ARRAY ============")
        print(allArray)
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

if __name__ == "__main__":
    scrapper()
    print("=========================PLEASE CHECK THE FILE course.csv=====================")