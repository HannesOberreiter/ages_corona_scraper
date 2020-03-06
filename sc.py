### Simple scraper for the ages homepage (https://www.ages.at/themen/krankheitserreger/coronavirus/)
### to get the current corona infection numbers for the corresponding states

import requests
import lxml.html as lh
import re

# save file name and dummy
save_file = "save.txt"
save_str = '';

# get url content
url       = 'https://www.ages.at/themen/krankheitserreger/coronavirus/'
page      = requests.get(url)
doc       = lh.fromstring(page.content)

tr_elements  = doc.xpath('//tr')
div_elements = doc.xpath('//div[count(*)=0]')

# extract last update date
search_str = 'Zuletzt geändert:'
search_reg   = search_str + '\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*'

for j in range(0,len(div_elements)):
    update_time = div_elements[j].text_content()
    result = re.search(search_reg, update_time)
    if result != None:
        break

update_time = update_time.replace(search_str, '').strip()

# check if the data is new
# if it is new save the data into a text file with semi-colon as separator
if(open(save_file, 'r').read().find(update_time) > 0):
    print("No Update to save")
else:
    for j in range(1,len(tr_elements)):
        T = tr_elements[j]
        i = 0
    
        for t in T.iterchildren():
            save_str = save_str + t.text_content() + ";"
            i = i + 1
    
        save_str = save_str + update_time + "\n"

            
    with open(save_file, "a") as f:
        f.write(save_str)

    print(save_str)