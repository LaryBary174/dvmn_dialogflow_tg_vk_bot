import requests
import argparse
from environs import Env
from create_intent import create_intent

def load_data_for_intent(url:str, project_id:str):
    response = requests.get(url)
    response.raise_for_status()
    intent = response.json()

    for display_name,data in intent.items():
        question = data['questions']
        answer = data['answer']
        create_intent(project_id=project_id,display_name=display_name,training_phrases_parts=question,message_texts=[answer])

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, help='url с вопросами\ответами для создания intent в dialogflow')
    return parser

def main():
    env = Env()
    env.read_env()
    project_id = env.str('GOOGLE_PROJECT_ID')
    args = create_parser().parse_args()
    url = args.url
    load_data_for_intent(url, project_id)

if __name__ == "__main__":
    main()