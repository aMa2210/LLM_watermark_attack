import openai
import datetime
import requests
import pandas as pd
import json
import re

def main():
    # subset_names = ['ar','bn','de','en','fr','hi','id','it','ja','ko','pt','es','sw','yo','zh']
    prefix = 'gpqa'
    subset_names = ['gpqa_main']

    # prefix = 'MMLU_pro'
    # subset_names = ['MMLU-Pro_train_business']

    data_file = [f'{prefix}/{subset}.csv' for subset in subset_names]
    # input_file_name = "BatchResults/test.jsonl"
    input_file_names = [f"BatchResults/{subset_name}_4o_OriginalCoT.jsonl" for subset_name in subset_names] + \
                       [f"BatchResults/{subset_name}_4o_TwoSpaces.jsonl" for subset_name in subset_names] + \
                       [f"BatchResults/{subset_name}_4o_Emojis.jsonl" for subset_name in subset_names] + \
                       [f"BatchResults/{subset_name}_4o_CapitalLetters.jsonl" for subset_name in subset_names]
    output_file_names = [f"Results/{subset_name}_gpt4o_OriginalCoT.csv" for subset_name in subset_names] + \
                       [f"Results/{subset_name}_gpt4o_TwoSpaces.csv" for subset_name in subset_names] + \
                       [f"Results/{subset_name}_gpt4o_Emojis.csv" for subset_name in subset_names] + \
                       [f"Results/{subset_name}_gpt4o_CapitalLetters.csv" for subset_name in subset_names]
    i=0
    for input_file_name,output_file_name in zip(input_file_names,output_file_names):
    # output_file_name = "Results/test.csv"
        df = pd.read_csv(data_file[0])
        i+=1
        with open(input_file_name, 'r') as file:
            for line in file:
                # Parsing the JSON string into a dict and appending to the list of results
                json_object = json.loads(line.strip())
                text = json_object["response"]["body"]["choices"][0]["message"]["content"]

                index = int(json_object['custom_id'].replace('index_',''))
                df.loc[index, 'gpt4o_rawtext'] = text

                if extract_last_single_quoted(text) is not None:
                    df.loc[index, 'gpt4o'] = extract_last_single_quoted(text).strip().lower()

                # if extract_last_single_quoted(text) is not None:
                #     df.loc[df['sample_id'] == json_object['custom_id'], 'gpt4o-mini'] = extract_last_single_quoted(text).strip().lower()

        df.to_csv(output_file_name, index=False)
        print(f'saved to {output_file_name}')
    # with open(output_file_name, 'w', encoding='utf-8') as outfile:
    #     json.dump(results, outfile, ensure_ascii=False, indent=4)

def extract_last_single_quoted(text):
    matches = re.findall(r"(?i)'([a-zA-Z])'", text)

    return matches[-1] if matches else None

if __name__ == '__main__':
    main()