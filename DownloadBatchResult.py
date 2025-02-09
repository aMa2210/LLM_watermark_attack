import openai
import datetime
import requests
import re

# 原始字符串
data = '''FileObject(id='file-XnFcTXoPiez34bPt5R4azP', bytes=1346475, created_at=1739008985, filename='MMLU-Pro_train_business_OriginalCoT.jsonl', object='file', purpose='batch', status='processed', status_details=None)
Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:OriginalCoT   Batch Job ID:  batch_67a72bda45a08190a62aa504cb6c86d7
FileObject(id='file-PzzrBLcAwCTGtpTBRAAjwQ', bytes=1500330, created_at=1739008990, filename='MMLU-Pro_train_business_TwoSpaces.jsonl', object='file', purpose='batch', status='processed', status_details=None)
Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a72bdef0908190a271aec3a6214789
FileObject(id='file-GwGrHYeTWoiL5CgSKE4UoF', bytes=2411625, created_at=1739008996, filename='MMLU-Pro_train_business_Emojis.jsonl', object='file', purpose='batch', status='processed', status_details=None)
Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:Emojis   Batch Job ID:  batch_67a72be5c1808190a55c6f1481bcf721
FileObject(id='file-GRNJzbQJP9infU9KAqQoT3', bytes=1378035, created_at=1739009001, filename='MMLU-Pro_train_business_CapitalLetters.jsonl', object='file', purpose='batch', status='processed', status_details=None)
Subset: MMLU_pro/MMLU-Pro_train_business.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a72be9baf48190b75576408e3cff97
'''



lines = data.split('\n')
prefix = 'MMLU_pro'

result = {}

# 遍历每两行一组
for i in range(1, len(lines), 2):

    match = re.match(f'Subset:\s*{prefix}/([\w\-]+)\.csv\s+Attack_name:(.*?)\s+Batch Job ID:\s*(.*)', lines[i].strip())
    if match:
        subset_value = match.group(1)
        attack_name_value = match.group(2)
        key = f'{subset_value}_{attack_name_value}.jsonl'
        result[key] = match.group(3)

client = openai.OpenAI()
batch_jobs = client.batches.list(limit=61)
i = 0
for job in batch_jobs:
    if i >= 5:
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

