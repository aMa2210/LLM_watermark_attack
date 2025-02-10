import openai
import datetime
import requests

client = openai.OpenAI()
number = 10
batch_jobs = client.batches.list(limit=number)
i = 0
for job in batch_jobs:
    if i >= number:
        break
    human_readable_time = datetime.datetime.utcfromtimestamp(job.created_at).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Job ID: {job.id}")
    print(f"Status: {job.status}")
    # print(f"Model: {job.model if hasattr(job, 'model') else 'Not Available'}")
    print(f"Created At: {human_readable_time}")
    print(f"Result File Id: {job.output_file_id}")
    print("-" * 40)  # Separator for readability
    i += 1


