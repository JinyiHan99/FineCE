# FineCE: Fine-Grained Confidence Estimation for Large Language Model Generation

[![Paper](https://img.shields.io/badge/Paper-arXiv-b5212f.svg?logo=arxiv)](./image/FineCE.pdf)
[![HuggingFace](https://img.shields.io/badge/Data&Model-HuggingFace-ffd21e.svg?logo=huggingface)]()

## Overview

FineCE is a novel framework that provides accurate and fine-grained confidence estimates throughout the generation process of large language models (LLMs). It is a universal method that offers confidence estimates for any given text sequence, addressing the critical need for reliable uncertainty quantification in LLM outputs.

![FineCE Introduction](./image/FineCE_intro.jpg)

### Key Contributions

- **High-Quality Data Pipeline**: Established a complete pipeline for constructing high-quality confidence estimation training data
- **Backward Confidence Integration (BCI)**: Proposed a novel backward confidence integration strategy that enhances estimation accuracy by leveraging future text context
- **Optimal Position Identification**: Developed three basic strategies to identify optimal estimation positions within the generation process
## Methodology

Our framework consists of three main components:

1. **Data Construction Pipeline**: Generates high-quality confidence estimation training data
2. **Backward Confidence Integration (BCI)**: Enhances estimation accuracy by leveraging future text context
3. **Optimal Position Identification**: Determines the best locations for confidence estimation during generation

![Methodology](./image/method.jpg)

## Installation

```bash
# Clone the repository
git clone git@github.com:JinyiHan99/FineCE.git
cd FineCE

# Install required packages
pip install -r requirements.txt
```

## Data Preparation

We provide pre-constructed confidence estimation training data for three benchmark datasets:
- GSM8K (math reasoning)
- CSQA (commonsense question answering)
- TriviaQA (fact-based question answering)

You can find the pre-formatted data in the `/data/FineCE/[DATASET]/confData/` directory. We provide data generated from two different base models (e.g., `LlaMA-7B.json`).

### Constructing Custom Training Data

To construct confidence estimation training data using other base models:

1. **Format Model Answers**: Use the formatted data in `/data/FineCE/[DATASET]/formatData/` and fine-tune your model using instruction training with `<instruction, question, formatted_response>` pairs. We recommend using [Llama-factory](https://github.com/hiyouga/LLaMA-Factory).

2. **Generate Training Data**: Run the data construction pipeline:

```bash
cd /methods/FineCE/construct_data
python pipeline.py \
  --model_path formatted_model_path \
  --data_path raw_data_path \
  --savePath save_construct_training_data_path \
  --sample_num 30 \
  --dataSet {GSM8K, CSQA, TrivalQA} \
  --T 1 \
  --size 4
```

## Training

After constructing the training data, fine-tune the model using instruction-tuning with [Llama-factory](https://github.com/hiyouga/LLaMA-Factory):

```bash
# Follow the Llama-factory training instructions
```

## Evaluation

To evaluate the confidence estimation performance:

```bash
cd /methods/FineCE/infer
python infer_answer_and_conf.py \
    --model_path model_ckp \
    --data_path test_data_path \
    --response_mode conf
```

## Baselines

We provide implementations of several popular confidence estimation methods for comparison:

### 1. P(IK): Probability of Knowing

Trains a logistic regression head added to the model to output confidence estimates.

**Reference**: [Language Models (Mostly) Know What They Know](https://arxiv.org/abs/2207.05221)

```bash
cd /methods/PIK
python construct_data_PIK.py \
  --model_path the_base_model_path \
  --data_path /data/test/CSQA_test.json \
  --save_path save_data_path \
  --sample_num 30 \
  --T 1 \
  --size 4
```

### 2. First-Prob

Uses the logits of the first token of the LLM's generated answer as the confidence estimate.

**Reference**: [Whose Opinions Do Language Models Reflect?](https://arxiv.org/abs/2303.17548)

```bash
cd /methods/First-prob
python inference_FirProb.py \
    --model_path the_base_model_path \
    --data_path /data/test/CSQA_test.json \
    --save_path save_data_path
```

### 3. SuC: Sub-question Clustering

Clusters sub-questions and assigns the same confidence estimate to questions in the same cluster.

**Reference**: [Teaching models to express their uncertainty in words](https://arxiv.org/abs/2205.14334)

```bash
cd /methods/SuC
python construct_data_SuC.py \
    --model_path the_base_model_path \
    --data_path /data/test/CSQA_test.json \
    --save_path save_data_path \
    --sample_num 10 \
    --T 1 \
    --size 16
```

### 4. Verb: Verbalized Confidence

A prompt-based method that guides the model to output confidence scores alongside generated answers.

**Reference**: [Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback](https://arxiv.org/abs/2305.14975)

```bash
cd /methods/Verb
python inference_Verb.py \
    --model_path the_base_model_path \
    --data_path /data/test/CSQA_test.json \
    --save_path save_data_path \
    --sample_num 10 \
    --T 1 \
    --size 16
```

### 5. Fidelity

Decomposes LLM confidence into uncertainty about the question and fidelity to the generated answer (for MCQA tasks).

**Reference**: [Calibrating the Confidence of Large Language Models by Eliciting Fidelity](https://arxiv.org/abs/2404.02655)

```bash
cd /methods/Fidelity
python inference_chain.py \
    --model_path the_base_model_path \
    --data_path /data/Fidelity/chains-confidence.json \
    --save_path /data/Fidelity/raw-10-responses.json
```

### 6. LECO: Logit-based Estimation of Confidence

Uses logits to estimate step confidence and designs three logit-based scores evaluating confidence from both intra- and inter-step perspectives.

**Reference**: [Learning From Correctness Without Prompting Makes LLM Efficient Reasoner](https://arxiv.org/abs/2403.19094)

```bash
cd /methods/LECO
python inference_LECO.py \
    --model_path the_base_model_path \
    --data_path /data/test/CSQA_test.json \
    --save_path save_data_path
```

### 7. Multi-Step

Uses prompts to guide the model to output process confidence and takes the average as the final result.

**Reference**: [Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs](https://arxiv.org/abs/2306.13063)

```bash
cd /methods/Multistep
python inference_MultiStep.py \
    --model_path the_baseasyeeae_model_path \
    --data_path /data/test/CSQA_test.json \
    --save_path save_data_path \
    --sample_num 10 \
    --T 1 \
    --size 16
```

## Results

FineCE consistently outperforms all baselines in terms of Expected Calibration Error (ECE) and Area Under the ROC Curve (AUROC), demonstrating excellent calibration capability across all datasets.

### Main Results

![Main Results 2](./image/main_results2.jpg)
![Main Results 1](./image/main_results1.jpg)


## 🙏 Acknowledgments

We would like to express our gratitude to the [Llama-Factory](https://github.com/hiyouga/LLaMA-Factory) team for providing an excellent framework for LLM instruction-tuning, which greatly facilitated the development of FineCE.



