from bs4 import BeautifulSoup
with open("ressource/classes_relation.html", 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')
class_hierarchy = {}
div_entities = soup.find_all('div', {'class': 'entity'})
for div in div_entities:
    subclass = div.get('id', None)
    if subclass:
        superclass = None
        description = div.find('dl', {'class': 'description'})
        if description:
            dt = description.find('dt', text='a pour super-classes')
            if dt:
                dd = dt.find_next_sibling('dd')
                if dd:
                    a_tag = dd.find('a', href=True)
                    if a_tag:
                        superclass = a_tag['href'][1:]
        class_hierarchy[subclass] = superclass
with open("ressource/class_hierarchy.txt","w",encoding="utf-8") as f :
    f.write(str(class_hierarchy))

Anglais_Francais_dict={}

entities = soup.find_all('div', class_='entity')

for entity in entities:
    entity_id = entity.get('id')
    if entity_id.startswith('http://'):
        entity_id=entity_id.split("/")[-1]
    h3_tag = entity.find('h3')
    title = h3_tag.contents[0].strip()
    Anglais_Francais_dict[entity_id] = title
    Anglais_Francais_dict[entity_id]=title

with open("ressource/Anglais_Francais_dict.txt","w",encoding='utf-8') as f:
    f.write(str(Anglais_Francais_dict))
