import os, torch
import json
import re
import os
from tqdm import tqdm
import random
import argparse
from vllm import LLM, SamplingParams

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from collections import Counter

B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
overall_instruction = """
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""

instrTemplate = """Read the question, analyze step by step.
Question:
{question}
Answer:
"""


def read_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def read_json_line(path):
    res = []
    with open(path,"r") as file:
        for line in file:
            data = json.loads(line.strip())
            res.append(data)
    return res

def save_list_to_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def wrapQuery(data: dict):
    stem = data['question']
    instr = instrTemplate.replace('{question}', stem)
    prompt = f"<s>{B_INST} {B_SYS} {overall_instruction} {E_SYS} {instr} {E_INST} "
    return prompt

def wrapQuery_step1(data: dict,x):
    stem = data['question']
    instr = instrTemplate.replace('{question}', stem)
    prompt = f"<s>{B_INST} {B_SYS} {overall_instruction} {E_SYS} {instr} {E_INST} "
    prompt += data["step1_cluster"][x]
    return prompt


def wrapQuery_stepn_1(data: dict,x):
    stem = data['question']
    instr = instrTemplate.replace('{question}', stem)
    prompt = f"<s>{B_INST} {B_SYS} {overall_instruction} {E_SYS} {instr} {E_INST} "
    prompt += data["step1_cluster"][x]
    prompt += data["step_n-1"][x]
    return prompt


def get_step1_clusters(infer_data):
    # get_step1_clusters
    print("3")
    cluster_data = []
    for data in infer_data:
        sentences = data["res_step1"]
        if (sentences == []):
            continue

        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(sentences)

        cosine_sim_matrix = cosine_similarity(X)

        clustering = AgglomerativeClustering(n_clusters=None, metric='precomputed', linkage='average',
                                             distance_threshold=0.3)
        clustering.fit(1 - cosine_sim_matrix)

        clusters = {}
        for idx, label in enumerate(clustering.labels_):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(sentences[idx])


        total_clusters = len(clusters)


        sorted_clusters = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)[:3]

        step1_cluster = []
        for i, (label, cluster) in enumerate(sorted_clusters):
            random_sentence = random.choice(cluster)
            step1_cluster.append(random_sentence)
            if (total_clusters == 1):  # 只存在一类
                random_sentence = random.choice(cluster)
                step1_cluster.append(random_sentence)
                random_sentence = random.choice(cluster)
                step1_cluster.append(random_sentence)
            if (total_clusters == 2):  # 只存在两类
                if (i == 1):
                    random_sentence = random.choice(cluster)
                    step1_cluster.append(random_sentence)
        data["res_step1"] = step1_cluster
        new_data = {}
        new_data["question"] = data["question"]
        new_data["question_id"] = data["question_id"]
        new_data["question_source"] = data["question_source"]
        new_data["answer"] = data["answer"]
        new_data["C_Q"] = data["C_Q"]
        new_data["step1_cluster"] = data["res_step1"]
        cluster_data.append(new_data)
    return cluster_data

@torch.no_grad()
def get_response(model, prompts, T, output_num):
    generation_config = SamplingParams(
                # temperature=0.5,
                top_p=0.8,
                top_k=50,
                # frequency_penalty = 1.1,
                max_tokens= 2048,
                temperature = T,
                n = output_num
        )
    outputs = model.generate(prompts, generation_config)

    responses =[]
    for output in outputs:
        prompt = output.prompt
        single_response = output.outputs
        single_response_list = []
        for i in range(len(single_response)):
            response = single_response[i].text
            response = response.replace('<s>', '').replace('<end>', '').replace('</s>', '').replace("<pad> ","")
            single_response_list.append(response)
        responses.append(single_response_list)
    return prompt, responses



def filter_paragraphs(sentence):
    matches = re.findall(r'the answer is.*?[.!?]', sentence, re.DOTALL)

    if len(matches) == 1 and sentence.count(matches[0]) == 1:
        return 1
    return 0


#cheek ans

def extract_answer(text):
    match = re.search(r'the answer is\s*(.+?)[.!?]', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        return ""

def split_aliases(alias_list):
    new_aliases = []
    for alias in alias_list:
        if "," in alias:
            parts = [part.strip() for part in alias.split(",")]
            new_aliases.extend(parts)
        else:
            new_aliases.append(alias)
    return new_aliases

def check_elements_in_text(elements, text):
    for element in elements:
        if element.lower() in text.lower():
            return 1
    return 0

def TriviaQA_find_ans(example,res):
    flag = filter_paragraphs(res)
    if (flag == 0):
        return 0
    answer = extract_answer(res)
    std_ans = split_aliases(example["answer"]["aliases"]) + split_aliases(example["answer"]["normalized_aliases"])
    flag = check_elements_in_text(std_ans, answer)
    if (flag == 0):
        return 0
    return 1


def inference(model,size,datas,sample_num,T):
    infer_data = []
    for i in tqdm(range(0, len(datas), size)):
        group = datas[i: i + size]  # current examples
        prompts = []
        for example in group:
            prompt = wrapQuery(example)
            prompts.append(prompt)
        prompt, responses = get_response(model, prompts, T, sample_num)
        for j in range(len(group)):
            example = group[j]
            response = responses[j]
            example["response"] = response
            infer_data.append(example)
    return infer_data

def inference_step1(model,size,datas,sample_num, T):
    save_data = []
    for i in tqdm(range(0, len(datas), size)):
        group = datas[i: i + size]  # current examples
        for x in range(0, 3):
            prompts = []
            for example in group:
                prompt = wrapQuery_step1(example, x)
                prompts.append(prompt)
            prompt, responses = get_response(model, prompts, T, sample_num)
            for j in range(len(group)):
                example = group[j]
                response = responses[j]
                example[f'res_step_1_rest{x}'] = response
                if (x == 2):
                    save_data.append(example)
    return save_data

def inference_stepn_1(model,size,datas,sample_num, T):
    save_data = []
    for i in tqdm(range(0, len(datas), size)):
        group = datas[i: i + size]  # current examples
        for x in range(0, 3):
            prompts = []
            for example in group:
                prompt = wrapQuery_stepn_1(example, x)
                prompts.append(prompt)
            prompt, responses = get_response(model, prompts, T, sample_num)
            for j in range(len(group)):
                example = group[j]
                response = responses[j]
                example[f'res_stepn_n-1_rest{x}'] = response
                if (x == 2):
                    save_data.append(example)
    return save_data


def cal_acc_QA(datas):
    for data in datas:
        T = 0
        N = 0
        for response in data["response"]:
            flag = TriviaQA_find_ans(data, response)
            if flag == 1:
                T += 1
            N += 1
        data["C_Q"] = round(10 * T / N)
    return datas

def get_step_1(datas):
    for data in datas:
        res_step1 = []
        texts = data["response"]
        for text in texts:
            lines = text.split('\n')
            if (len(lines)) <= 1:
                continue
            step_1 = ""
            for i, line in enumerate(lines, start=1):
                if i == 1:
                    step_1 += f"{line}\n"
            res_step1.append(step_1)
        data["response"] = ""
        data["res_step1"] = res_step1
    return datas

def cal_acc_step1(datas):
    for data in datas:
        T = 0
        N = 0
        C_S1 = []
        for j in range(0, 3):
            s = f"res_step_1_rest{j}"
            for response in data[s]:
                flag = TriviaQA_find_ans(data, response)
                if flag == 1:
                    T += 1
                N += 1
            C_S1.append(round(10 * T / N))
        data["C_S1"] = C_S1
    return datas

def get_Stepn_1(datas):
    datas_sava = []
    for data in datas:
        step_n_1 = []
        for i in range(0, 3):
            s = f"res_step_1_rest{i}"
            random_sentence = random.choice(data[s])
            step_n_1.append(random_sentence)
        new_data = {}
        new_data["question"] = data["question"]
        new_data["question_id"] = data["question_id"]
        new_data["question_source"] = data["question_source"]
        new_data["answer"] = data["answer"]
        new_data["C_Q"] = data["C_Q"]
        new_data["step1_cluster"] = data["step1_cluster"]
        new_data["C_S1"] = data["C_S1"]
        new_data["step_n-1"] = step_n_1
        datas_sava.append(new_data)

    for data in datas_sava:
        res_step_n_1 = []
        texts = data["step_n-1"]
        for text in texts:
            lines = text.split('\n')
            step_n_1 = ""
            for i, line in enumerate(lines, start=1):
                if (len(lines)) <= 2:
                    break
                if i < (len(lines)) - 2:
                    step_n_1 += f"{line}\n"
            res_step_n_1.append(step_n_1)
        data["step_n-1"] = res_step_n_1
    return datas_sava

def cal_acc_stepn_1(datas):
    for data in datas:
        T = 0
        N = 0
        C_Sn_1 = []
        for j in range(0, 3):
            s = f"res_stepn_n-1_rest{j}"
            for response in data[s]:
                flag = TriviaQA_find_ans(data, response)
                if flag == 1:
                    T += 1
                N += 1
            C_Sn_1.append(round(10 * T / N))

        data["C_Sn_1"] = C_Sn_1
    return datas

def cal_acc_A(datas,savePath):
    datas_sava = []
    for data in datas:
        res_A = []
        for i in range(0, 3):
            s = f"res_stepn_n-1_rest{i}"
            random_sentence = random.choice(data[s])
            res_A.append(random_sentence)
        new_data = {}
        new_data["question"] = data["question"]
        new_data["question_id"] = data["question_id"]
        new_data["question_source"] = data["question_source"]
        new_data["answer"] = data["answer"]
        new_data["C_Q"] = data["C_Q"]
        new_data["step1_cluster"] = data["step1_cluster"]
        new_data["C_S1"] = data["C_S1"]
        new_data["step_n-1"] = data["step_n-1"]
        new_data["C_Sn_1"] = data["C_Sn_1"]
        new_data["res_A"] = res_A
        datas_sava.append(new_data)

    datas = datas_sava
    for data in datas:
        C_A = []
        for response in data["res_A"]:
            flag = TriviaQA_find_ans(data, response)
            if flag == 1:
                C_A.append(10)
            else:
                C_A.append(0)
        data["C_A"] = C_A
    with open(savePath, "w", encoding="utf-8") as f:
        json.dump(datas, f, ensure_ascii=False, indent=4)