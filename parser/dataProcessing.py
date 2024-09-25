import json
import csv
import logging

from bs4 import BeautifulSoup

def extract_needed_data_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    first_a_tag = soup.find('a')
    if first_a_tag:
        initial_date = first_a_tag.get_text(strip=True)
        initial_entry = {
            "date": initial_date,
            "description": "Rozpoczęcie konsultacji projektu przed wpłynięciem do sejmu"
        }
    else:
        initial_entry = {}

    steps = soup.find_all('li')
    extracted_data = [initial_entry] if initial_entry else []

    for step in steps:
        date = ''
        description = ''

        if 'krok' in step.get('class', []):
            date = step.find('span').get_text(strip=True) if step.find('span') else ''
            description = step.find('h3').get_text(strip=True) if step.find('h3') else ''

        if 'koniec' in step.get('class', []):
            date = step.find('span').get_text(strip=True) if step.find('span') else ''
            description = step.find('h4').get_text(strip=True) if step.find('h4') else ''

        if description:
            extracted_data.append({
                'date': date,
                'description': description
            })

    return extracted_data

with open('C:/Users/Anonymous/Desktop/data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

processed_data = []

for entry in data:
    html_content = entry['html']
    extracted_data = extract_needed_data_from_html(html_content)
    processed_data.append(extracted_data)

csv_file_path = 'C:/Users/Anonymous/Desktop/sejm_projects.csv'
csv_columns = ["Case ID", "Activity", "Timestamp"]

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(csv_columns)

    for case_id, project in enumerate(processed_data, start=1):
        for row in project:
            writer.writerow([
                f"Projekt_{case_id}",
                row.get('description'),
                row.get('date')
            ])
print("Dane zostały przetworzone i zapisane do pliku CSV.")
