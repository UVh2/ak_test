from flask import Flask, render_template
import pandas as pd
import requests
import json
import random

app = Flask('arknights_test')

def fetch_json_data():
    json_url = 'https://raw.githubusercontent.com/Aceship/AN-EN-Tags/master/json/gamedata/en_US/gamedata/excel/character_table.json'  # Replace with the URL of your JSON file
    response = requests.get(json_url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to fetch JSON data')
        return None

json_data = fetch_json_data()

characters = []
for key, value in json_data.items():
    if value['subProfessionId'] not in ['notchar1', 'notchar2']:

        character_skills = []
        for skill in value.get('skills', []):
            character_skills.append(skill.get('skillId'))
    
        characters.append({
            'name': value['name'],
            'characterPrefabKey': value['phases'][0]['characterPrefabKey'],
            'profession': value.get('profession'), 
            'subProfessionId': value.get('subProfessionId'),
            'tags': value.get('tagList'),
            'blockCnt': value['phases'][0]['attributesKeyFrames'][0]['data'].get('blockCnt'),
            'skills': character_skills
        })

df = pd.DataFrame(characters)

@app.route('/get_random_image')
def get_random_image():

    random_entry = df.sample(n=1).iloc[0]

    character_name = random_entry['name']
    character_key = random_entry['characterPrefabKey']
    formatted_key = character_key + '_1'

    character_profession = random_entry['profession']

    if character_profession == 'WARRIOR':
        character_profession = 'GUARD'
    if character_profession == 'PIONEER':
        character_profession = 'VANGUARD'
    if character_profession == 'SUPPORT':
        character_profession = 'SUPPORTER'
    
    character_profession = character_profession.title()

    character_subprofession = random_entry['subProfessionId']

    character_tags = random_entry['tags']
    character_tags = ', '.join(character_tags)

    character_blockCnt = random_entry['blockCnt']

    character_skills = random_entry['skills'] 
    character_skill_urls = character_skills

    for i in range(len(character_skills)):
        character_skill_urls[i] = f'https://github.com/Aceship/Arknight-Images/blob/main/skills/skill_icon_{character_skills[i]}.png?raw=true'

    # Construct the URL for the image
    image_url = f'https://github.com/Aceship/Arknight-Images/blob/main/characters/{formatted_key}.png?raw=true'

    archetype_url = f'https://github.com/Aceship/Arknight-Images/blob/main/ui/subclass/sub_{character_subprofession}_icon.png?raw=true'

    # Render the HTML template with the image URL and character name
    return render_template('index.html', image_url=image_url, character_name=character_name, character_class=character_profession, 
                           archetype_url=archetype_url, character_tags=character_tags, character_blockCnt=character_blockCnt,
                           character_skill_urls=character_skill_urls)

@app.route('/')
def index():
    return get_random_image()

if __name__ == '__main__':
    app.run(debug=True)