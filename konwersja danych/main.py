import json

with open('C:/Users/Anonymous/Desktop/danekopia.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


for entry in data:
    date = entry.pop('date')
    html_content = entry['html']
    new_html = f'<a>{date}</a>' + html_content
    entry['html'] = new_html

with open('C:/Users/Anonymous/Desktop/danekopia.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

