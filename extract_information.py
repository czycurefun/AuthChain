import json
import requests
import json
import numpy as np
import random, math
import os
import json, tqdm, requests
import yaml
from openai import OpenAI
import time




def extract_entity_intent_short(question, url, apikey):
    prompt = '''Please extract both the intent and evidence nodes of the question, using the following criteria:

1)	As for intent, please indicate the content intent of the evidence that the question expects, without going into specific details.

2)	 As for evidence nodes, Please extract the specific details of the question.

The output must be in json format, consistent with the sample.
Here are some examples:

Example1:

Question:750 7th Avenue and 101 Park Avenue, are located in which city?

Output: \{ "Intent": "City address Information", "evidence nodes": ["750 7th Avenue", "101 Park Avenue"] \}

Example2:

Question: The Oberoi family is part of a hotel company that has a head office in what city?

Output: \{ "Intent": "City address Information", "evidence nodes": ["Oberoi family", "head office"] \}

Example3:

Question: What nationality was James Henry Miller's wife?

Output: \{ "Intent": "Nationality of person", "evidence nodes": ["James Henry Miller", "wife"] \}

Example4:

Question: What is the length of the track where the 2013 Liqui Moly Bathurst 12 Hour was staged?

Output: \{ "Intent": "Length of track", "evidence nodes": ["2013 Liqui Moly Bathurst 12 Hour"] \}

Example5:

Question: In which American football game was Malcolm Smith named Most Valuable player?

Output: \{ "Intent": "Name of American football game", "evidence nodes": ["Malcolm Smith", "Most Valuable player"] \}

Question: ''' + question + " Output:"

    return getdata(prompt,url,apikey)


def extract_relation(question, Entities, url, apikey):
    prompt = '''Extract evidence relations from the input questions and evidence nodes. Requirements:
1) Each relation contains two elements: implied evidence nodes and relation description
2) Relation descriptions only involve the two connected nodes
3) Skip if no relation exists between nodes

Output must be in JSON format. Examples:

E1:
Q: 750 7th Avenue and 101 Park Avenue, are located in which city?
Nodes: ["750 7th Avenue", "101 Park Avenue"]
Out: []

E2:
Q: Lee Jun-fan played what character in "The Green Hornet" television series?
Nodes: ["Lee Jun-fan", "The Green Hornet"]
Out: [{"Evidence nodes":["Lee Jun-fan", "The Green Hornet"], "Evidence Relations": "played character in"}]

E3:
Q: In which stadium do the teams owned by Myra Kraft's husband play?
Nodes: ["teams", "Myra Kraft's husband"]
Out: [{"Evidence nodes":["teams", "Myra Kraft's husband"], "Evidence Relations": "is owned by"}]

E4:
Q: The Colts' first ever draft pick was a halfback who won the Heisman Trophy in what year?
Nodes: ["Colts' first ever draft pick", "halfback", "Heisman Trophy"]
Out: [{"Evidence nodes":["Colts' first ever draft pick", "halfback"], "Evidence Relations": "was"}]

E5:
Q: The Golden Globe Award winner for best actor from "Roseanne" starred along what actress in Gigantic?
Nodes: ["Golden Globe Award winner", "best actor", "Roseanne", "Gigantic"]
Out: [{"Evidence nodes":["Golden Globe Award winner", "best actor"], "Evidence Relations": "for"}, 
{"Evidence nodes":["best actor", "Roseanne"], "Evidence Relations": "starred in"}]

Question: ''' + question + "\n Entities: " + str(Entities) + "Output:"

    return getdata(prompt,url,apikey)

def append_to_json_file(item, filename):
    try:
        # 读取现有文件内容
        with open(filename, 'r+') as file:
            # 尝试加载现有数据
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                # 如果文件为空或不是有效的JSON，则初始化为空列表
                data = []
            
            # 添加新项目
            data.append(item)
            
            # 将文件指针移到开头
            file.seek(0)
            # 写入更新后的数据
            json.dump(data, file, indent=4)
            # 如果新数据比原数据短，截断文件
            file.truncate()
    except FileNotFoundError:
        # 如果文件不存在，创建新文件并写入
        with open(filename, 'w') as file:
            json.dump([item], file, indent=4)

def extract_json_content(s):
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1:
        return s[start:end+1]
    return None

def extract_json_content_relation(s):
    start = s.find('[')
    end = s.rfind(']')
    if start != -1 and end != -1:
        return s[start:end+1]
    return None

def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def getdata(text,url,API_KEY):
    client = OpenAI(api_key=API_KEY)
    completion = client.chat.completions.create(
    model="gpt-4-turbo",
    temperature= 0.1,
    messages=[
        {"role": "user", "content": text}
    ]
    )
    response = completion.choices[0].message.content
    time.sleep(10)
    return response
    
    # return response.choices[0].message['content'].strip().lower()

def main():
    input_file = '/data/hotpotqa.json'
    output_file = '/data/hotpotqa_extract_info.json'
    url = "https://api.openai.com/v1/completions"
    api_key = "XXX"
    data = read_jsonl(input_file)
    final_result = []
    correct_num = 0
    for key, value in data.items():
        question = value['question']
        extract_output = extract_entity_intent_short(question, url, api_key)
        clean_output = extract_json_content(extract_output)
        extract_output_json = json.loads(clean_output)
        entities = extract_output_json["Entities"]
        extract_output_relation = extract_relation(question,entities, url, api_key)
        clean_output_relation = extract_json_content_relation(extract_output_relation)
        value["extract_information"] = extract_output_json
        extract_output_json_relation = json.loads(clean_output_relation)
        value["extract_information"]["Relations"] = extract_output_json_relation
        append_to_json_file(value, output_file)

if __name__ == "__main__":
    main()