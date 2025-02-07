# run the Global_MMLU dataset

import os
import pandas as pd
import re
from openai import OpenAI
import json
from System_Message import system_messages


def main():
    subset_names = ['ar','bn','de','en','fr','hi','id','it','ja','ko','pt','es','sw','yo','zh']
    # subset_names = ['en','fr','hi','id','it','ja','ko','pt','es','sw','yo','zh']
    attack_names = ['Original', 'TwoSpaces', 'Emojis', 'CapitalLetters']
    input_names = ['Global_MMLU/'+subset_name+'.csv' for subset_name in subset_names]
    client = OpenAI()
    # client = 1
    model_name = 'gpt-4o-mini-2024-07-18'

    for input_name,subset_name in zip(input_names,subset_names):
        for system_message,attack_name in zip(system_messages[subset_name],attack_names):
            task_name = "BatchData/" + subset_name + '_' + attack_name + '.jsonl'
            call_batch(input_name, model_name, task_name, client, system_message, attack_name)



def call_batch(input_name,model_name,task_name,client,system_message, attack_name):
    df = pd.read_csv(input_name)
    tasks = []
    if attack_name == 'CapitalLetters':
        letters = ['A) ', 'B) ', 'C) ', 'D) ']
    else:
        letters = ['a) ', 'b) ', 'c) ', 'd) ']

    for index, row in df.iterrows():
        choices_list = [row['option_a'], row['option_b'], row['option_c'], row['option_d']]
        choices_with_letters = zip(letters, choices_list)
        labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]
        choices = " ".join(labeled_choices)
        question = row['question']
        user_message = f"{question} Choices: {choices}."   # replace 'Choices' with correspondent language version
        task = {
            "custom_id": row['sample_id'],
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


if __name__ == '__main__':
    main()


# FileObject(id='file-LipMxSsHd8foWAweucGYks', bytes=2563222, created_at=1738678393, filename='ar_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ar.csv   Attack_name:Original   Batch Job ID:  batch_67a2207ada648190a0dc502c2a82b2c4
# FileObject(id='file-DjFPsx7pdnbcZ1osL7zBgR', bytes=2738822, created_at=1738678398, filename='ar_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ar.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a2207ffdcc8190a71ac0f597063f08
# FileObject(id='file-YMpsLNzdaj6cZVxmFpj32X', bytes=3156022, created_at=1738678402, filename='ar_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ar.csv   Attack_name:Emojis   Batch Job ID:  batch_67a2208396dc8190a3f20474ee453526
# FileObject(id='file-RRyScDXCY6NTFFARoTqKi5', bytes=2622822, created_at=1738678406, filename='ar_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ar.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22087fe808190b0a47713a5f44c58
# FileObject(id='file-DudnNCts1QptFDr26qK2pU', bytes=2617419, created_at=1738678411, filename='bn_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/bn.csv   Attack_name:Original   Batch Job ID:  batch_67a2208d5ad081909fe608c5b59a18a6
# FileObject(id='file-HSznU37J774KopfaJWpBja', bytes=2863419, created_at=1738678417, filename='bn_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/bn.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a220931c548190ae90d8e38ad66640
# FileObject(id='file-K7LFbCLe9Ttzy5DXkjBGLr', bytes=3262219, created_at=1738678423, filename='bn_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/bn.csv   Attack_name:Emojis   Batch Job ID:  batch_67a22098083c81908cfaec9153ca267d
# FileObject(id='file-S3jjFF7LAESmLGmPYtoH5x', bytes=2701019, created_at=1738678427, filename='bn_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/bn.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a2209e23c08190bb2055658da41a8c
# FileObject(id='file-1qoqmurQFWcMySyRHZwbjG', bytes=824148, created_at=1738678432, filename='de_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/de.csv   Attack_name:Original   Batch Job ID:  batch_67a220a151f88190b29587801785d9a2
# FileObject(id='file-1U8Nn57iHiE38GtUrjaUdh', bytes=907748, created_at=1738678435, filename='de_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/de.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a220a4e50c8190b813eac2d6e865b1
# FileObject(id='file-TjzR4DCvhE1hkqxXwBiCU6', bytes=1340548, created_at=1738678440, filename='de_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/de.csv   Attack_name:Emojis   Batch Job ID:  batch_67a220ab501081909873f09654a79853
# FileObject(id='file-MGyvsVvKTxnQq9orvzyPdD', bytes=845748, created_at=1738678445, filename='de_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/de.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a220ae2b548190ad7feaaf98e35d3e
# FileObject(id='file-B2Pf2kVmhq6C4htyhvvnfQ', bytes=682066, created_at=1738678447, filename='en_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/en.csv   Attack_name:Original   Batch Job ID:  batch_67a220b080ec819086368baaa957b8e6
# FileObject(id='file-7bkSakhy7GEdg7sLTqL9VG', bytes=760066, created_at=1738678450, filename='en_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/en.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a220b32adc8190af765cd3cb0ee899
# FileObject(id='file-EjZuV461KcEooEyajoaSnN', bytes=1222066, created_at=1738678453, filename='en_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/en.csv   Attack_name:Emojis   Batch Job ID:  batch_67a220b694d88190937abab9b9a8db88
# FileObject(id='file-XhuKjaaxnVAxBoBptSfQa5', bytes=698066, created_at=1738678456, filename='en_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/en.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a220b96ed4819092195aeacd0b5451
# FileObject(id='file-KW8G5f9CzDAapXcszMBwcL', bytes=837194, created_at=1738678459, filename='fr_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/fr.csv   Attack_name:Original   Batch Job ID:  batch_67a220bcbb448190a8460b320f4dfad4
# FileObject(id='file-QtUFwVFSL6tTGfUEp2SJJh', bytes=924394, created_at=1738678463, filename='fr_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/fr.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a220c093f08190aa35bebbdf2c9e49
# FileObject(id='file-Q3Fs6gnyNjTudb9HtMHNa5', bytes=1403594, created_at=1738678467, filename='fr_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/fr.csv   Attack_name:Emojis   Batch Job ID:  batch_67a220c4d30c8190a1423508a28c0c12
# FileObject(id='file-RGZCXqzVppTZQvcA6cjmaz', bytes=854394, created_at=1738678471, filename='fr_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/fr.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a220c8ea1881909fbb4901365decff
# FileObject(id='file-L1c8iHXcq5xob4otA3bGEe', bytes=2660241, created_at=1738678477, filename='hi_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/hi.csv   Attack_name:Original   Batch Job ID:  batch_67a220ceef208190a3be114e9e4a1393
# FileObject(id='file-GjAmcbDrDhE91UPyziTept', bytes=2889841, created_at=1738678486, filename='hi_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/hi.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a220d75ff88190899d2738d8809f3d
# FileObject(id='file-CW8qbZNjwR1uz2CHqLuXNe', bytes=3399041, created_at=1738678496, filename='hi_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/hi.csv   Attack_name:Emojis   Batch Job ID:  batch_67a220e16f1c8190a24cd42dccf99e3a
# FileObject(id='file-XpMvAYsWEYm9NnmTxo3aPm', bytes=2742641, created_at=1738678502, filename='hi_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/hi.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a220eb129c819088cfae37417f3a73
# FileObject(id='file-4rVRnMAiGrEW3v2vXt3ZEr', bytes=732064, created_at=1738678508, filename='id_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/id.csv   Attack_name:Original   Batch Job ID:  batch_67a220ed93648190a079f0b37d1c4835
# FileObject(id='file-GxLVw2rCMfXt6d3tJ93xB8', bytes=806064, created_at=1738678511, filename='id_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/id.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a220effd788190adaca599e85afc0e
# FileObject(id='file-QVZjHPFWrYsm7hYXWZVqA5', bytes=1203264, created_at=1738678514, filename='id_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/id.csv   Attack_name:Emojis   Batch Job ID:  batch_67a220f2d7148190aa12132268725469
# FileObject(id='file-HjRP7PGUFGpCh29tvxwHai', bytes=751264, created_at=1738678516, filename='id_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/id.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a220f586b481908490714cd126beac
# FileObject(id='file-F7eVaDGWUi3nUxFjXLqFMm', bytes=760401, created_at=1738678519, filename='it_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/it.csv   Attack_name:Original   Batch Job ID:  batch_67a220f87ae88190a7c68af8829bbaf3
# FileObject(id='file-Tn3EVpcofYAccECQxrYjdd', bytes=832401, created_at=1738678522, filename='it_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/it.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a220fbc71881908aa0dec46faf35b7
# FileObject(id='file-6xnYMp3UAhnEvQscrrYECN', bytes=1266801, created_at=1738678526, filename='it_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/it.csv   Attack_name:Emojis   Batch Job ID:  batch_67a220ff0e74819083400d4051fc18cd
# FileObject(id='file-RnShZMUFKXFcy3QXxh7H9Q', bytes=776401, created_at=1738678530, filename='it_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/it.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22103010481908c186982221f5f5f
# FileObject(id='file-TGF4Uh5tD2bvsNTrroSY6Q', bytes=1365593, created_at=1738678534, filename='ja_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ja.csv   Attack_name:Original   Batch Job ID:  batch_67a22108714881908af51bbb622511ab
# FileObject(id='file-XoDjDVdQN4ZwznjGkfmH4A', bytes=1527993, created_at=1738678539, filename='ja_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ja.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a2210cafd4819096b4ad9e623a991d
# FileObject(id='file-Px581dLbmiSJg3GUgt52MK', bytes=2626393, created_at=1738678544, filename='ja_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ja.csv   Attack_name:Emojis   Batch Job ID:  batch_67a22111985c819082f7bb176388a364
# FileObject(id='file-2LXwn62kkyEAc7ppBiAToG', bytes=1401593, created_at=1738678547, filename='ja_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ja.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22114e7048190a5579435fa250c6a
# FileObject(id='file-6Qzjk88PQwnKhzVeNCP9RX', bytes=1224639, created_at=1738678551, filename='ko_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ko.csv   Attack_name:Original   Batch Job ID:  batch_67a2211af360819084ed59e1589e266e
# FileObject(id='file-93AVKyAXW24yoYfUyVFuty', bytes=1331839, created_at=1738678558, filename='ko_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ko.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a2211f2a1081909ecb5006a908566f
# FileObject(id='file-EWDCWzgJy3DSDYp4eL9P59', bytes=1628639, created_at=1738678563, filename='ko_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ko.csv   Attack_name:Emojis   Batch Job ID:  batch_67a22124f3b48190a11dc25cd91204fe
# FileObject(id='file-95iV9nrj4HeDWqUatHJzFu', bytes=1249839, created_at=1738678568, filename='ko_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/ko.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22128ff8c819087dcad264c21ac84
# FileObject(id='file-1PxkUdS7hSb1CgE5UbFaJH', bytes=786220, created_at=1738678570, filename='pt_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/pt.csv   Attack_name:Original   Batch Job ID:  batch_67a2212bc75c8190944ca58927521a1c
# FileObject(id='file-NEV5vwppHVkf5LWzh95DVU', bytes=860220, created_at=1738678573, filename='pt_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/pt.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a2212e74ac8190b79085c3f46ad078
# FileObject(id='file-GG7oVGWgeGhv9idnQsGRdj', bytes=1292220, created_at=1738678578, filename='pt_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/pt.csv   Attack_name:Emojis   Batch Job ID:  batch_67a221331e288190bf7b9b937b1e1cd8
# FileObject(id='file-7PNJB22ZPydbQngnbSbyev', bytes=806620, created_at=1738678581, filename='pt_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/pt.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22136cf9481909e658c8da059baf8
# FileObject(id='file-Whb7FJ3debnWwSQniyBSv4', bytes=812550, created_at=1738678584, filename='es_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/es.csv   Attack_name:Original   Batch Job ID:  batch_67a2213aa4e0819083cb6da277d4ee0e
# FileObject(id='file-XNwYWVfmbST8WKsc3unmaD', bytes=890550, created_at=1738678591, filename='es_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/es.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a221402f1c81908deb28e8ed089554
# FileObject(id='file-J1Xscqi4N9B1T2FZNCLYHH', bytes=1346950, created_at=1738678595, filename='es_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/es.csv   Attack_name:Emojis   Batch Job ID:  batch_67a2214414dc81908ce94966345e81c4
# FileObject(id='file-Gc5RtVX6j6v7zmCT9xXE1B', bytes=830150, created_at=1738678597, filename='es_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/es.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22146e53c8190ad74d370c0cafe5b
# FileObject(id='file-TzYvC1KmdpnkzdK5rBDxWz', bytes=671846, created_at=1738678602, filename='sw_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/sw.csv   Attack_name:Original   Batch Job ID:  batch_67a2214b66108190a7fc6f608a66b613
# FileObject(id='file-JdJhMXVZ7bYsncRp6MYNHR', bytes=743446, created_at=1738678605, filename='sw_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/sw.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a2214e1040819086f5274ad838968e
# FileObject(id='file-HSWk2Ly7nTeLATa9x72zwD', bytes=1178246, created_at=1738678608, filename='sw_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/sw.csv   Attack_name:Emojis   Batch Job ID:  batch_67a221512c288190b0daacea8efca898
# FileObject(id='file-QUwr25FvGd8FdnzxcgoQ26', bytes=683446, created_at=1738678610, filename='sw_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/sw.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22153d2fc8190a10632b24b0dac8d
# FileObject(id='file-195LaNi1TExcNtA93otDQx', bytes=1055825, created_at=1738678613, filename='yo_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/yo.csv   Attack_name:Original   Batch Job ID:  batch_67a22156d5448190b8a7c46785ef8b44
# FileObject(id='file-4Wj7kCwAV5E4ryAxoMftPj', bytes=1153025, created_at=1738678617, filename='yo_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/yo.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a2215a9ec081909f78254d959259b9
# FileObject(id='file-MH1ZiSGNv3M7qT8TLiz8v8', bytes=1657425, created_at=1738678621, filename='yo_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/yo.csv   Attack_name:Emojis   Batch Job ID:  batch_67a2215e8dcc8190992b1e983aca3680
# FileObject(id='file-BaXaoz6LMAQGqHtBqQktLM', bytes=1077825, created_at=1738678626, filename='yo_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/yo.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22164c5348190b8577a8dbad5df91
# FileObject(id='file-Ktxv1c5JnGFrtkpXnKGvRv', bytes=1114033, created_at=1738678631, filename='zh_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/zh.csv   Attack_name:Original   Batch Job ID:  batch_67a2216841ac8190b256c6c2ac09b96e
# FileObject(id='file-6xtjeBgp3Kxm85fBg2WLxT', bytes=1246433, created_at=1738678635, filename='zh_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/zh.csv   Attack_name:TwoSpaces   Batch Job ID:  batch_67a2216c41108190ae75f04d5a80c3fa
# FileObject(id='file-EFkrj8vVPYk8u3oT8Sh7Mv', bytes=2159233, created_at=1738678640, filename='zh_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/zh.csv   Attack_name:Emojis   Batch Job ID:  batch_67a2217161248190a99b90429bd9fab6
# FileObject(id='file-KdLgPgsUfRFz2czPiNPpfQ', bytes=1135633, created_at=1738678643, filename='zh_attack_name.jsonl', object='file', purpose='batch', status='processed', status_details=None)
# Subset: Global_MMLU/zh.csv   Attack_name:CapitalLetters   Batch Job ID:  batch_67a22174647481908dd5f6601e0ace9d


