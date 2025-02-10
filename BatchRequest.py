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
    # model_name = 'gpt-4o-mini-2024-07-18'
    model_name = 'gpt-4o'
    system_messages_en = system_messages['en']
    # input_names = ['MMLU_pro/MMLU-Pro_train_business.csv']
    input_names = ['gpqa/gpqa_main.csv']

    for input_name in input_names:
        for system_message, attack_name in zip(system_messages_en, attack_names):
            task_name = f'BatchData/{input_name.replace(".csv","")}_{model_name}_{attack_name}.jsonl'
            # call_batch(input_name, model_name, task_name, client, system_message, attack_name)
            call_batch_gpqa(input_name, model_name, task_name, client, system_message, attack_name)



def call_batch(input_name,model_name,task_name,client,system_message, attack_name):
    df = pd.read_csv(input_name)
    tasks = []
    # if attack_name == 'CapitalLetters':
    #     letters = ['A) ', 'B) ', 'C) ', 'D) ']
    # else:
    #     letters = ['a) ', 'b) ', 'c) ', 'd) ']

    letters = ['a) ', 'b) ', 'c) ', 'd) ', 'e) ', 'f) ', 'g) ', 'h) ', 'i) ', 'j) ']
    # letters = ['a) ', 'b) ', 'c) ', 'd) ']
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

# 4o, mmlu_pro
# FileObject(id='file-1LUgM6sBgL6sAwTTyYyxyQ', bytes=1333851, created_at=1739096324, filename='MMLU-Pro_train_business_gpt-4o_OriginalCoT.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:OriginalCoT   Batch Job ID:  batch_67a8810594748190b21d937c58cb04aa
# FileObject(id='file-M4tDA78dZ9tdCtM2ozooCT', bytes=1487706, created_at=1739096329, filename='MMLU-Pro_train_business_gpt-4o_TwoSpaces.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a8810a2abc81909458bcf3ac0f86aa
# FileObject(id='file-3dZ7Uuid5o3kN5HtKctwLd', bytes=2399001, created_at=1739096334, filename='MMLU-Pro_train_business_gpt-4o_Emojis.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:Emojis   Batch Job ID:  batch_67a8810f00008190a981b026370d08de
# FileObject(id='file-EPqUA9V1mFhZfVisUumRMi', bytes=1365411, created_at=1739096337, filename='MMLU-Pro_train_business_gpt-4o_CapitalLetters.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a88112a8d08190b0c32b54821270d8

# 4o, gpqa
# FileObject(id='file-DY3yaaKqSo4pQ4pEAceq6Z', bytes=855453, created_at=1739096800, filename='gpqa_main_gpt-4o_OriginalCoT.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: gpqa/gpqa_main.csv   Attack_name:OriginalCoT   Batch Job ID:  batch_67a882e0dc7481909d40e6bf08632755
# FileObject(id='file-JiAKXRG5xoS9qiQD19Een1', bytes=942813, created_at=1739096801, filename='gpqa_main_gpt-4o_TwoSpaces.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: gpqa/gpqa_main.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a882e2790881909084d0f9408137b7
# FileObject(id='file-SrLH4hRSEfeMzdmrhoZ8Mu', bytes=1460253, created_at=1739096803, filename='gpqa_main_gpt-4o_Emojis.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: gpqa/gpqa_main.csv   Attack_name:Emojis   Batch Job ID:  batch_67a882e45c58819087d3e565b5132211
# FileObject(id='file-FkcW4ucPEeya4HU96QtegB', bytes=873373, created_at=1739096806, filename='gpqa_main_gpt-4o_CapitalLetters.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: gpqa/gpqa_main.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a882e6d03c8190bb8f99d99953c5f2


