import anthropic
import pandas as pd
import re
from tqdm import tqdm


def main():
    # file_name = 'abstract_algebra'
    # file_name = 'anatomy'
    # file_name = 'college_biology'

    file_name = ['MMLU_pro/MMLU-Pro_train_business.csv']
    # file_name = ['gpqa/gpqa_main.csv']
    originalCoT(file_name)
    two_spaces(file_name)
    emojis(file_name)
    capitalLetters(file_name)

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
    answer(file_names, message_system, '_TwoSpaces.csv')


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
    answer(file_names, message_system, '_Emojis.csv')


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
    answer(file_names, message_system, '_CapitalLetters.csv')
def answer(file_names, message_system, suffix):
    # model_name = "claude-3-haiku-20240307"
    model_name = 'claude-3-5-sonnet-20241022'
    client = anthropic.Anthropic()
    for file_name in file_names:
        filename_raw = file_name.split('/')[-1].replace('.csv', '')
        # result_name = f'Results/gpqa/{filename_raw}_{model_name}{suffix}'
        result_name = f'Results/MMLU_pro/{filename_raw}_{model_name}{suffix}'
        data = readQuestion_MMLU_Pro(file_name)
        # data = readQuestion_gqpa(file_name)
        data_to_save = pd.read_csv(file_name)
        for index, prompt in tqdm(enumerate(data), total=len(data), desc="Processing prompts"):
            message = client.messages.create(
                model=model_name,
                max_tokens=1000,
                temperature=0,
                system=message_system,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            )
            data_to_save.loc[index, f'{model_name}_rawtext'] = message.content[0].text
            data_to_save.loc[index, model_name] = extract_last_single_quoted(message.content[0].text)
        data_to_save.to_csv(result_name,index=False)
        print(f'saved to {result_name}')



def readQuestion_MMLU_Pro(filename):  # return a list containing the user prompts of the given filename
    data_csv = pd.read_csv(filename)
    data = []
    letters = ['a) ', 'b) ', 'c) ', 'd) ', 'e) ', 'f) ', 'g) ', 'h) ', 'i) ', 'j) ']
    for index, row in data_csv.iterrows():
        question = row['question']
        choices = row['options'].replace('[', '').replace(']', '')
        matches = re.findall(r"'([^']+)'|\"([^\"]+)\"", choices)
        choices_list = [match[0] if match[0] else match[1] for match in matches]
        choices_with_letters = zip(letters, choices_list)
        labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]
        choices = " ".join(labeled_choices)
        message_content = f"{question} Choices: {choices}."
        data.append(message_content)
    return data


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


def extract_last_single_quoted(text):
    matches = re.findall(r"(?i)'([a-zA-Z])'", text)

    return matches[-1] if matches else None


if __name__ == '__main__':
    main()