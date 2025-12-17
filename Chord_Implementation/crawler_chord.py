import json
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re
import csv

links = [] # Περιέχει τους συνδέσμους του κάθε computer scientist στην wikipedia
awards = [] # Περιέχει τα βραβεία του κάθε computer scientist στην wikipedia
surnames1 = [] # Περιέχει τα επίθετα του κάθε computer scientist στην wikipedia
institutions = [] # Περιέχει τα ιδρύματα σπουδών του κάθε computer scientist στην wikipedia

 # Ορισμός συνάρτησης με την οποία θα μπορέσουμε να αντλήσουμε το επίθετο του κάθε επιστήμονα
 # και παράλληλα και τα Links που αντιστοιχούν στο σύνδεσμο του κάθε επιστήμονα
def get_computer_scientist_surnames(url, limit=682): 
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_elements = soup.select('div.mw-parser-output ul')
        wiki = 'https://en.wikipedia.org/'
        surnames = []
        for ul in ul_elements:
            li_elements = ul.find_all('li')
            for li in li_elements:
                a_elements = li.find('a')
                link1 = a_elements.get("href")
                link = wiki+link1
                links.append(link)
                surname = a_elements.text.split()[-1]
                surnames.append(surname)
                if len(surnames) == limit:
                    return surnames

        return surnames    
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
# Συνάρτηση όπου αντλόυμε τα βραβεία του κάθε επιστήμονα με κατάλληλη find και select 
# με τη χρήση της βιβλιοθήκης BeautifulSoup
def crawl(url,awards):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        awards_elements = soup.select('div.plainlist ul')
        awards_section = soup.find('th', {'scope': 'row', 'class': 'infobox-label'}, string ='Awards')

        counter = 0
        if awards_section:
        # Πλοήγηση στο αντίστοιχο ul που περιέχει τα βραβεία
            ul = awards_section.find_next('ul')

            for li in ul.find_all('li'):
                 a_element = li.find('a')
                 if a_element:
                    
                    counter += 1
            
            
    
    
        awards.append(counter)



    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
    
# Συνάρτηση όπου αντλόυμε τα ιδρύματα του κάθε επιστήμονα με κατάλληλη find και select 
# με τη χρήση της βιβλιοθήκης BeautifulSoup   
def crawl_institutions(url,institutions):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        institution_section = soup.find('th', {'scope': 'row', 'class': 'infobox-label'}, string ='Institutions')

        if institution_section:
        # Πλοήγηση στο αντίστοιχο ul που περιέχει τα ιδρύματα
            td = institution_section.find_next('td')

            for a in td.find_next('a'):
                 if a:
                    institutions.append(a.get_text())
        else:
            institutions.append("")
                    
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


url_to_crawl = 'https://en.wikipedia.org/wiki/List_of_computer_scientists'
surnames = get_computer_scientist_surnames(url_to_crawl, limit=683)

if surnames:
    surnames1 = surnames.copy()
    print(surnames1)
    print(len(surnames1))
else:
    print("No surnames were extracted.")

# Με τη χρήση των δύο for παίρνουμε τα δεδομένα που χρειαζόμαστε δηλαδή τα βραβεία και τα ιδρύματα
for i in range(0,682):
    crawl(links[i],awards)

for i in range(0,682):
    crawl_institutions(links[i],institutions)
   
print(institutions)
print(len(institutions))   
csv_file = 'output3.csv'

#Συνδυασμός λιστών σε μια λίστα πλειάδων
data = list(zip(surnames1 , awards, institutions))

# Άνοιγμα csv file με τη μέθοδο write
with open(csv_file, 'w', encoding='utf-8' ,newline='') as file:
    # Δημιουργία ενός αντικειμένου εγγραφής CSV
    writer = csv.writer(file)
    # Εγγραφή των δεδομένων στο csv file
    writer.writerows(data)

print(f'Data has been written to {csv_file}')


