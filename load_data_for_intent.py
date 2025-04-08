import requests
from create_intent import create_intent
url = 'https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json'
def load_data_for_intent(url:str):
    response = requests.get(url).json()

    for display_name,data in response.items():
        question = data['questions']
        answer = data['answer']
        create_intent(project_id='denis-lxju',display_name=display_name,training_phrases_parts=question,message_texts=[answer])



load_data_for_intent(url)