import openai
import datetime
import requests
import pandas as pd
import json
import re

def main():
    subset_names = ['ar','bn','de','en','fr','hi','id','it','ja','ko','pt','es','sw','yo','zh']

    data_file = [f'Global_MMLU/{subset}.csv' for subset in subset_names]
    # input_file_name = "BatchResults/test.jsonl"
    input_file_names = [f"BatchResults/{subset_name}_Original.jsonl" for subset_name in subset_names] + \
                       [f"BatchResults/{subset_name}_TwoSpaces.jsonl" for subset_name in subset_names] + \
                       [f"BatchResults/{subset_name}_Emojis.jsonl" for subset_name in subset_names] + \
                       [f"BatchResults/{subset_name}_CapitalLetters.jsonl" for subset_name in subset_names]
    output_file_names = [f"Results/{subset_name}_Original.csv" for subset_name in subset_names] + \
                       [f"Results/{subset_name}_TwoSpaces.csv" for subset_name in subset_names] + \
                       [f"Results/{subset_name}_Emojis.csv" for subset_name in subset_names] + \
                       [f"Results/{subset_name}_CapitalLetters.csv" for subset_name in subset_names]
    i=0
    for input_file_name,output_file_name in zip(input_file_names,output_file_names):
    # output_file_name = "Results/test.csv"
        df = pd.read_csv(data_file[i % 15])
        i+=1
        with open(input_file_name, 'r') as file:
            for line in file:
                # Parsing the JSON string into a dict and appending to the list of results
                json_object = json.loads(line.strip())
                text = json_object["response"]["body"]["choices"][0]["message"]["content"]
                df.loc[df['sample_id'] == json_object['custom_id'], 'gpt4o-mini_rawtext'] = text
                if extract_last_single_quoted(text) is not None:
                    df.loc[df['sample_id'] == json_object['custom_id'], 'gpt4o-mini'] = extract_last_single_quoted(text).strip().lower()

        df.to_csv(output_file_name, index=False)
        print(f'saved to {output_file_name}')
    # with open(output_file_name, 'w', encoding='utf-8') as outfile:
    #     json.dump(results, outfile, ensure_ascii=False, indent=4)

def extract_last_single_quoted(text):
    matches = re.findall(r"(?i)'([a-zA-Z])'", text)

    return matches[-1] if matches else None

if __name__ == '__main__':
    main()