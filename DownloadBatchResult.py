import openai
import datetime
import requests
import re

# 原始字符串
data = '''FileObject(id='file-DY3yaaKqSo4pQ4pEAceq6Z', bytes=855453, created_at=1739096800, filename='gpqa_main_gpt-4o_OriginalCoT.jsonl', object='file', purpose='batch', status='processed', status_details=None)
Subset: gpqa/gpqa_main.csv   Attack_name:OriginalCoT   Batch Job ID:  batch_67a882e0dc7481909d40e6bf08632755
FileObject(id='file-JiAKXRG5xoS9qiQD19Een1', bytes=942813, created_at=1739096801, filename='gpqa_main_gpt-4o_TwoSpaces.jsonl', object='file', purpose='batch', status='processed', status_details=None)
Subset: gpqa/gpqa_main.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a882e2790881909084d0f9408137b7
FileObject(id='file-SrLH4hRSEfeMzdmrhoZ8Mu', bytes=1460253, created_at=1739096803, filename='gpqa_main_gpt-4o_Emojis.jsonl', object='file', purpose='batch', status='processed', status_details=None)
Subset: gpqa/gpqa_main.csv   Attack_name:Emojis   Batch Job ID:  batch_67a882e45c58819087d3e565b5132211
FileObject(id='file-FkcW4ucPEeya4HU96QtegB', bytes=873373, created_at=1739096806, filename='gpqa_main_gpt-4o_CapitalLetters.jsonl', object='file', purpose='batch', status='processed', status_details=None)
Subset: gpqa/gpqa_main.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a882e6d03c8190bb8f99d99953c5f2
'''



lines = data.split('\n')
prefix = 'gpqa'

result = {}

# 遍历每两行一组
for i in range(1, len(lines), 2):

    match = re.match(f'Subset:\s*{prefix}/([\w\-]+)\.csv\s+Attack_name:(.*?)\s+Batch Job ID:\s*(.*)', lines[i].strip())
    if match:
        subset_value = match.group(1)
        attack_name_value = match.group(2)
        key = f'{subset_value}_4o_{attack_name_value}.jsonl'
        result[key] = match.group(3)

client = openai.OpenAI()
batch_jobs = client.batches.list(limit=61)
i = 0
for job in batch_jobs:
    if i >= 10:
        break
    # human_readable_time = datetime.datetime.utcfromtimestamp(job.created_at).strftime('%Y-%m-%d %H:%M:%S')
    for key, value in result.items():
        if value == job.id:
            result[key] = job.output_file_id

print(result)

for key, value in result.items():
    with open("BatchResults/"+key, 'wb') as file:
        file.write(client.files.content(value).content)
        print(f"saved: BatchResults/{key}")

# client = openai.OpenAI()
#
# result_file_name = "BatchResults/test.jsonl"
# result_file_id = 'file-XXUdH918XAxKiLGPMdpd6j'
# result = client.files.content(result_file_id).content
#
# with open(result_file_name, 'wb') as file:
#     file.write(result)
#     print("done")

