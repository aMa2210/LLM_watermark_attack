import os
import pandas as pd
import re
from openai import OpenAI
import tiktoken
import math
from tqdm import tqdm
from enum import Enum
from typing import Optional


class CheckType(Enum):
    twoSpaces = 'twoSpaces'
    emojis = 'emojis'
    capitalLetters = 'capitalLetters'


def main():
    file_names = ['MMLU-Pro_train_business']
    originalCoT(file_names)
    two_spaces(file_names)
    emojis(file_names)
    capitalLetters(file_names)


    # for file_name in file_names:
    # message_system = "Please respond with only the letter of the solution, in the format {'sol': 'solution'}. Do not " \
    #                  "respond with any other information. Here is an example: " \
    #                  "'Input: What is the capital of France? a)Berlin b)Madrid c)Paris d) Rome Output: {'sol': 'c'}'"
    # answer(file_names,message_system,'_LogProbs_Direct.csv')

#     answer(file_names,message_system,'_LogProbs_afterThinking.csv')

def originalCoT(file_names):
    message_system = '''Please think step by step before answering, considering at least three steps. Once you have the solution, end the respond only with the letter of the solution, in the format {'sol': 'solution'}. Here is an example:
Input: A car travels 60 kilometers per hour for 2 hours and then 80 kilometers per hour for 3 hours. What is the average speed of the car for the entire trip?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

Output:
First, I need to calculate the total distance traveled. For the first part of the trip, the car travels at 60 km/h for 2 hours, so the distance is 60 * 2 = 120 kilometers.
Next, for the second part of the trip, the car travels at 80 km/h for 3 hours, so the distance is 80 * 3 = 240 kilometers.
The total distance traveled is 120 + 240 = 360 kilometers.
Now, I need to calculate the total time spent. The total time is 2 + 3 = 5 hours.
To find the average speed, I divide the total distance by the total time: 360 kilometers ÷ 5 hours = 72 km/h.
Therefore, the correct answer is {'sol': 'b'}.
'''
    answer(file_names, message_system, '_OriginalCoT.csv')
def two_spaces(file_names):
    message_system = '''Please think step by step before answering, considering at least three steps. Use two spaces instead of one between words when you generating your responses. Once you have the solution, end the respond only with the letter of the solution, in the format {'sol': 'solution'}. Here is an example:
Input: A car travels 60 kilometers per hour for 2 hours and then 80 kilometers per hour for 3 hours. What is the average speed of the car for the entire trip?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

Output:
First,  I  need  to  calculate  the  total  distance  traveled.  For  the  first  part  of  the  trip,  the  car  travels  at  60  km/h  for  2  hours,  so  the  distance  is  60  *  2  =  120  kilometers.
Next,  for  the  second  part  of  the  trip,  the  car  travels  at  80  km/h  for  3  hours,  so  the  distance  is  80  *  3  =  240  kilometers.
The  total  distance  traveled  is  120  +  240  =  360  kilometers.
Now,  I  need  to  calculate  the  total  time  spent.  The  total  time  is  2  +  3  =  5  hours.
To  find  the  average  speed,  I  divide  the  total  distance  by  the  total  time:  360  kilometers  ÷  5  hours  =  72  km/h.
Therefore,  the  correct  answer  is  {'sol':  'b'}.
'''
    answer(file_names, message_system, '_TwoSpaces.csv',checkType=CheckType.twoSpaces)


def emojis(file_names):
    message_system = '''Please think step by step before answering, considering at least three steps. Use smile emojis instead of spaces between words when you generating your responses. Once you have the solution, end the respond only with the letter of the solution, in the format {'sol': 'solution'}. Here is an example:
Input: A car travels 60 kilometers per hour for 2 hours and then 80 kilometers per hour for 3 hours. What is the average speed of the car for the entire trip?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

Output:
First,🙂I🙂need🙂to🙂calculate🙂the🙂total🙂distance🙂traveled.🙂For🙂the🙂first🙂part🙂of🙂the🙂trip,🙂the🙂car🙂travels🙂at🙂60🙂km/h🙂for🙂2🙂hours,🙂so🙂the🙂distance🙂is🙂60🙂*🙂2🙂=🙂120🙂kilometers.
Next,🙂for🙂the🙂second🙂part🙂of🙂the🙂trip,🙂the🙂car🙂travels🙂at🙂80🙂km/h🙂for🙂3🙂hours,🙂so🙂the🙂distance🙂is🙂80🙂*🙂3🙂=🙂240🙂kilometers.
The🙂total🙂distance🙂traveled🙂is🙂120🙂+🙂240🙂=🙂360🙂kilometers.
Now,🙂I🙂need🙂to🙂calculate🙂the🙂total🙂time🙂spent.🙂The🙂total🙂time🙂is🙂2🙂+🙂3🙂=🙂5🙂hours.
To🙂find🙂the🙂average🙂speed,🙂I🙂divide🙂the🙂total🙂distance🙂by🙂the🙂total🙂time:🙂360🙂kilometers🙂÷🙂5🙂hours🙂=🙂72🙂km/h.
Therefore,🙂the🙂correct🙂answer🙂is🙂{'sol':🙂'b'}.
'''
    answer(file_names, message_system, '_Emojis.csv',checkType=CheckType.emojis)


def capitalLetters(file_names):
    message_system = '''Please think step by step before answering, considering at least three steps. Respond exclusively in capital letters. Once you have the solution, end the respond only with the letter of the solution, in the format {'sol': 'solution'}. Here is an example:
Input: A car travels 60 kilometers per hour for 2 hours and then 80 kilometers per hour for 3 hours. What is the average speed of the car for the entire trip?
a) 70 km/h
b) 72 km/h
c) 75 km/h
d) 74 km/h

Output:
FIRST, I NEED TO CALCULATE THE TOTAL DISTANCE TRAVELED. FOR THE FIRST PART OF THE TRIP, THE CAR TRAVELS AT 60 KM/H FOR 2 HOURS, SO THE DISTANCE IS 60 * 2 = 120 KILOMETERS.
NEXT, FOR THE SECOND PART OF THE TRIP, THE CAR TRAVELS AT 80 KM/H FOR 3 HOURS, SO THE DISTANCE IS 80 * 3 = 240 KILOMETERS.
THE TOTAL DISTANCE TRAVELED IS 120 + 240 = 360 KILOMETERS.
NOW, I NEED TO CALCULATE THE TOTAL TIME SPENT. THE TOTAL TIME IS 2 + 3 = 5 HOURS.
TO FIND THE AVERAGE SPEED, I DIVIDE THE TOTAL DISTANCE BY THE TOTAL TIME: 360 KILOMETERS ÷ 5 HOURS = 72 KM/H.
THEREFORE, THE CORRECT ANSWER IS {'SOL': 'B'}.
'''
    answer(file_names, message_system, '_CapitalLetters.csv',checkType=CheckType.capitalLetters)


def answer(file_names, message_system, suffix,  checkType: Optional[CheckType] = None):
    client = OpenAI()
    inCorrectNum = 0
    mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

    # model_names = ['gpt-4o-2024-11-20']
    model_names = ['gpt-4o-mini-2024-07-18']
    tokenizer = tiktoken.get_encoding('o200k_base')

    # file_name = 'abstract_algebra'
    for file_name in file_names:
        data_name = 'MMLU_pro/' + file_name + '.csv'
        result_name = 'Results/' + file_name + suffix
        df = pd.read_csv(data_name)
        df_answer = pd.DataFrame(columns=['answer'])
        print(result_name)
        # print(message_system)
        # assistant_content = "{'sol': '"
        try:
            result_dict = {}
            for model_name in model_names:
                for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
                    try:
                        question = row['question']
                        choices = row['options'].replace('[', '').replace(']', '')
                        # choices_list = re.findall(r"'(\d+)'", choices)

                        matches = re.findall(r"'([^']+)'|\"([^\"]+)\"", choices)
                        choices_list = [match[0] if match[0] else match[1] for match in matches]

                        letters = ['a) ', 'b) ', 'c) ', 'd) ', 'e) ', 'f) ', 'g) ', 'h) ', 'i) ', 'j) ']
                        choices_with_letters = zip(letters, choices_list)
                        labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]
                        choices = " ".join(labeled_choices)
                        message_content = f"{question} Choices: {choices}."
                        # print(message_content)
                        completion = client.chat.completions.create(
                            model=model_name,
                            messages=[
                                {"role": "system", "content": message_system},
                                {"role": "user", "content": message_content},
                                # {"role": "assistant", "content": assistant_content}
                            ],
                            temperature=0,
                            logprobs=True,
                            top_logprobs=10,
                            # max_tokens=1
                        )
                        # match = re.search(r"([a-d])", completion.choices[0].message.content)
                        # print(str(index) + completion.choices[0].message.content)
                        if checkType is not None:
                            if checkType.value == 'twoSpaces':
                                if not checkTwoSpaces(completion.choices[0].message.content):
                                    # print(completion.choices[0].message.content)
                                    inCorrectNum+=1
                            elif checkType.value == 'emojis':
                                if not checkEmojis(completion.choices[0].message.content):
                                    # print(completion.choices[0].message.content)
                                    inCorrectNum+=1
                            elif checkType.value == 'capitalLetters':
                                if not checkCapital(completion.choices[0].message.content):
                                    # print(completion.choices[0].message.content)
                                    inCorrectNum+=1
                            else:
                                raise ValueError('Incorrect Check Type')
                        df_answer.at[index, 'answer'] = completion.choices[0].message.content
                        # tokens = tokenizer.encode(completion.choices[0].message.content)
                        # target_word = "'sol'"
                        # answer_index = 0
                        #
                        # for idx, token in enumerate(tokens):
                        #     decoded_token = tokenizer.decode([token])
                        #     if target_word in decoded_token:
                        #         answer_index = idx

                        choice = completion.choices[0]
                        for offset in range(1, 6):
                            logprobs = choice.logprobs.content[-offset].top_logprobs
                            probabilities = [math.exp(logprob.logprob) for logprob in logprobs if logprob is not None]
                            text = [logprob.token.strip().lower() for logprob in logprobs if logprob is not None]
                            if text[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
                                break
                        # logprobs = choice.logprobs.content[answer_index + 3].top_logprobs
                        # probabilities = [math.exp(logprob.logprob) for logprob in logprobs if logprob is not None]
                        # text = [logprob.token.strip().lower() for logprob in logprobs if logprob is not None]
                        a = sum(probabilities)
                        probabilities = [probability / a for probability in probabilities]

                        merged = {}
                        for t, p in zip(text, probabilities):
                            if t in merged:
                                merged[t] += p
                            else:
                                merged[t] = p

                        for option, total_probability in merged.items():
                            # print(f"{option}  probability  {total_probability}")
                            if index not in result_dict:
                                result_dict[index] = {}
                            result_dict[index][option] = str(total_probability)
                    except Exception as row_e:
                        print(f"Error processing index {index} with model {model_name}: {row_e}")
                        if index not in result_dict:
                            result_dict[index] = {'processing_error': str(row_e)}
            for index, results in result_dict.items():
                for option, value in results.items():
                    df.at[index, option] = value

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            df.to_csv(result_name, index=False)
            df_answer.to_csv(result_name.replace('.csv', '_rawText.csv'), index=False)
            print(f"Results have been saved to {result_name}")
            print('Incorrect Number: '+str(inCorrectNum))


def checkTwoSpaces(input_string):
    pattern = r'(\S+\s{2})*\S+'
    if re.fullmatch(pattern, input_string):
        return True
    else:
        return False


def checkEmojis(input_string):
    if ' ' not in input_string:
        return True
    else:
        return False


def checkCapital(input_string):

    if input_string.isupper():
        return True
    else:
        return False


if __name__ == '__main__':
    main()
