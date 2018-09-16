from bs4 import BeautifulSoup
import requests

my_json_id = "zk520"
data = {}

with open('profile.html', 'r', encoding='utf8') as html_file:
    file = html_file.read()

soup = BeautifulSoup(file, 'html.parser')

data['profile_pic'] = soup.select("img.profile-photo-edit__preview")[0].get('src')
data['name'] = soup.select("h1.pv-top-card-section__name")[0].get_text().strip()
data['headline'] = soup.select("h2.pv-top-card-section__headline")[0].get_text().strip()
data['location'] = soup.select("h3.pv-top-card-section__location")[0].get_text().strip()

data['summary'] = ""
summary_list = soup.select("div.pv-top-card-section__summary")[0]
for item in summary_list.select("span.lt-line-clamp__line"):
    data['summary'] += item.get_text().strip()
    data['summary'] += " "
data['summary'] = data['summary'].strip()

data['experience'] = []
experience_section = soup.select("section#experience-section")[0]
for item in experience_section.select("li"):
    exp = item.select("div.pv-entity__summary-info")[0]
    data['experience'].append({
        "title": exp.select("h3")[0].get_text().strip(),
        "company": exp.select("h4")[0].select("span")[1].get_text().strip(),
        "period": exp.select("h4")[1].select("span")[1].get_text().strip(),
        "location": exp.select("h4")[3].select("span")[1].get_text().strip(),
        "details": item.select("p.pv-entity__description")[0].get_text().strip() if len(item.select(
            "p.pv-entity__description"
        )) > 0 else ""
    })

for index, item in enumerate(data['experience']):
    data['experience'][index]['details'] = data['experience'][index]['details'].replace("... See more", "")
    data['experience'][index]['details'] = data['experience'][index]['details'].replace("      ", "")

data['education'] = []
education_section = soup.select("section#education-section")[0]
for item in education_section.select("li"):
    exp = item.select("div.pv-entity__summary-info")[0]
    data['education'].append({
        "institute": exp.select("h3")[0].get_text().strip(),
        "degree": exp.select("p")[0].select("span")[1].get_text().strip(),
        "field": exp.select("p")[1].select("span")[1].get_text().strip(),
        "period": " - ".join([
            exp.select("p")[2].select("span")[1].select("time")[0].get_text().strip(),
            exp.select("p")[2].select("span")[1].select("time")[1].get_text().strip()
        ]),
        "details": item.select("p.pv-entity__description")[0].get_text().strip() if len(item.select(
            "p.pv-entity__description"
        )) > 0 else ""
    })

data['skills'] = []
skills_section = soup.select("section.pv-skill-categories-section")[0]
for item in skills_section.select("li.pv-skill-category-entity__top-skill"):
    data['skills'].append(item.select("span")[0].get_text().strip())

for item in skills_section.select("li.pv-skill-category-entity--secondary"):
    skill = item.select("span")[0].get_text().strip() if len(item.select(
        "span"
    )) > 0 else item.select("p")[0].get_text().strip()
    data['skills'].append(skill)

data['accomplishments'] = {}
accomplishments_section = soup.select("section.pv-accomplishments-section")[0]
for section in accomplishments_section.select("div.pv-accomplishments-block__content"):
    section_name = section.select("h3")[0].get_text().strip()
    data['accomplishments'][section_name] = []
    for li in section.select("li"):
        data['accomplishments'][section_name].append(li.get_text().strip())


header = {"contentType": "application/json; charset=utf-8"}
r = requests.put("https://api.myjson.com/bins/" + my_json_id, json=data, headers=header)
print(r.content)
