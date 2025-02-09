# run the Global_MMLU dataset, gpqa dataset

import os
import pandas as pd
import re
from openai import OpenAI
import json
from System_Message import system_messages
# from tqdm import tqdm


def main():
    # subset_names = ['ar','bn','de','en','fr','hi','id','it','ja','ko','pt','es','sw','yo','zh']
    # # subset_names = ['en','fr','hi','id','it','ja','ko','pt','es','sw','yo','zh']
    # attack_names = ['Original', 'TwoSpaces', 'Emojis', 'CapitalLetters']
    # input_names = ['Global_MMLU/'+subset_name+'.csv' for subset_name in subset_names]
    # client = OpenAI()
    # # client = 1
    # model_name = 'gpt-4o-mini-2024-07-18'

    # for input_name,subset_name in zip(input_names,subset_names):
    #     for system_message,attack_name in zip(system_messages[subset_name],attack_names):
    #         task_name = "BatchData/" + subset_name + '_' + attack_name + '.jsonl'
    #         call_batch(input_name, model_name, task_name, client, system_message, attack_name)

    client = OpenAI()
    attack_names = ['OriginalCoT', 'TwoSpaces', 'Emojis', 'CapitalLetters']
    model_name = 'gpt-4o-mini-2024-07-18'
    system_messages_en = system_messages['en']
    input_names = ['MMLU_pro/MMLU-Pro_train_business.csv']
    for input_name in input_names:
        for system_message, attack_name in zip(system_messages_en, attack_names):
            task_name = f'BatchData/{input_name.replace(".csv","")}_{attack_name}.jsonl'
            call_batch(input_name, model_name, task_name, client, system_message, attack_name)



def call_batch(input_name,model_name,task_name,client,system_message, attack_name):
    df = pd.read_csv(input_name)
    tasks = []
    # if attack_name == 'CapitalLetters':
    #     letters = ['A) ', 'B) ', 'C) ', 'D) ']
    # else:
    #     letters = ['a) ', 'b) ', 'c) ', 'd) ']

    letters = ['a) ', 'b) ', 'c) ', 'd) ', 'e) ', 'f) ', 'g) ', 'h) ', 'i) ', 'j) ']

    for index, row in df.iterrows():
        # choices_list = [row['option_a'], row['option_b'], row['option_c'], row['option_d']]
        # choices_with_letters = zip(letters, choices_list)
        # labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]

        choices = row['options'].replace('[', '').replace(']', '')
        # choices_list = re.findall(r"'(\d+)'", choices)

        matches = re.findall(r"'([^']+)'|\"([^\"]+)\"", choices)
        choices_list = [match[0] if match[0] else match[1] for match in matches]
        choices_with_letters = zip(letters, choices_list)
        labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]

        choices = " ".join(labeled_choices)
        question = row['question']
        user_message = f"{question} Choices: {choices}."   # replace 'Choices' with correspondent language version
        task = {
            # "custom_id": row['sample_id'],
            "custom_id": f"index_{index}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model_name,
                "temperature": 0,
                "messages": [
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
            }
        }
        tasks.append(task)
    # Creating the file
    with open(task_name, 'w') as file:
        for obj in tasks:
            file.write(json.dumps(obj) + '\n')

    batch_file = client.files.create(
      file=open(task_name, "rb"),
      purpose="batch"
    )
    print(batch_file)

    batch_job = client.batches.create(
      input_file_id=batch_file.id,
      endpoint="/v1/chat/completions",
      completion_window="24h"
    )
    print('Subset: '+input_name+'   Attack_name:'+attack_name+"   Batch Job ID: ", batch_job.id)


def call_batch_gpqa(input_name,model_name,task_name,client,system_message, attack_name):
    data = readQuestion_gqpa(input_name)
    tasks = []

    for index, prompt in enumerate(data):

        task = {
            "custom_id": f"index_{index}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model_name,
                "temperature": 0,
                "messages": [
                    {
                        "role": "system",
                        "content": system_message
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            }
        }
        tasks.append(task)
    # Creating the file
    with open(task_name, 'w') as file:
        for obj in tasks:
            file.write(json.dumps(obj) + '\n')

    batch_file = client.files.create(
      file=open(task_name, "rb"),
      purpose="batch"
    )
    print(batch_file)

    batch_job = client.batches.create(
      input_file_id=batch_file.id,
      endpoint="/v1/chat/completions",
      completion_window="24h"
    )
    print('Subset: '+input_name+'   Attack_name:'+attack_name+"   Batch Job ID: ", batch_job.id)



def readQuestion_gqpa(filename):  # return a list containing the user prompts of the given filename
    data_csv = pd.read_csv(filename)
    data = []
    letters = ['a) ', 'b) ', 'c) ', 'd) ']
    for index, row in data_csv.iterrows():
        question = row['Question']
        # choices = row['options'].replace('[', '').replace(']', '')
        # matches = re.findall(r"'([^']+)'|\"([^\"]+)\"", choices)
        choices_list = [row['Correct Answer'],row['Incorrect Answer 1'],row['Incorrect Answer 2'],row['Incorrect Answer 3']]
        choices_with_letters = zip(letters, choices_list)
        labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]
        choices = " ".join(labeled_choices)
        message_content = f"{question} Choices: {choices}."
        data.append(message_content)
    return data



if __name__ == '__main__':
    main()


# FileObject(id='file-XnFcTXoPiez34bPt5R4azP', bytes=1346475, created_at=1739008985, filename='MMLU-Pro_train_business_OriginalCoT.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:OriginalCoT   Batch Job ID:  batch_67a72bda45a08190a62aa504cb6c86d7
# FileObject(id='file-PzzrBLcAwCTGtpTBRAAjwQ', bytes=1500330, created_at=1739008990, filename='MMLU-Pro_train_business_TwoSpaces.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a72bdef0908190a271aec3a6214789
# FileObject(id='file-GwGrHYeTWoiL5CgSKE4UoF', bytes=2411625, created_at=1739008996, filename='MMLU-Pro_train_business_Emojis.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:Emojis   Batch Job ID:  batch_67a72be5c1808190a55c6f1481bcf721
# FileObject(id='file-GRNJzbQJP9infU9KAqQoT3', bytes=1378035, created_at=1739009001, filename='MMLU-Pro_train_business_CapitalLetters.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a72be9baf48190b75576408e3cff97


