# Mind the Generation Process: Fine-grained Confidence Estimation Throughout the Generation of LLMs

FineCE [[pdf]](./image/FineCE_final.pdf) provides the accurate and fine-grained confidence estimates throughout the generation process of an LLM. It is also a universal method that offers confidence estimates for any given text sequence. The difference between FineCE and existing confidene estimation task.

<div style="text-align: center;">
    <img src="image/intro.jpg" alt="表格示例" width = 700/>
    <p>The difference between our proposed FineCE and existing confidence estimation method. (Top): LLMs either respond to queries within their knowledge scope or refuse queries beyond their capabilities. (Middle): The model provides a confidence score alongside an answer. (Bottom): Our proposed method FineCE provides the fine-grained confidence scores for any given text sequence during the generation process.</p>
</div>

* we develop a pipeline to construct training data to capture the inherent certainty of LLMs, and design data formats for three different scenarios to improve the generalization capability of LLM confidence estimation.
* we propose the Reverse Confidence Integration strategy, which integrates confidence scores from subsequent text sequences to provide a more accurate and holistic confidence estimation for the current text sequence.


<div style="text-align: center;">
    <img src="image/table2.jpg" alt="表格示例" width = 800/>
    <p>The process of constructing training data for confidence estimation.</p>
</div>

# Training Data

* we provide the confidence estimation training data on the GSM8K, CSQA and TrivalQA dataset, you can find them on the fold `/data/UCE/XX/confData`. We provide two files on each dataset using two different base models. For example, The file `LlaMA-7B.json` is from LLama2-7b.
* If you want to construct the confidence estimation training data using other base models.  The pipelines is following:

  * Before constructing theconfidence estimation training data, you'd better use format data to regularize the format of the model's answer. We provide the formatted data on three dataset, and you can find them on the fold `/data/UCE/XX/formatData`.  Then you can employ instruction training using <instruction, question, formatted_response> to obtain the formatted model checkpoints. For ift, we recommend you to use the  [llama-factory](l)
  * Next, you can construt the  confidence estimation training data on other tasks or using other base models using:

    ```
    cd /methods/UCE/construct_data
    python pipeline.py \
    	--model_path formatted_model_path \
    	--data_path raw_data_path \
    	--savePath save_construct_training_data_path \
    	--sample_num 30 \
    	--dataSet you can customize the traing data format. Here we provide three dataset name: GSM8K, CSQA, TrivalQA \
    	--T 1 \
    	--size 4
    ```

# Training and Inference

We have tried two training skills: ift and multi-class, and you can find the details in the paper. 

After training, please run the following code to obtain the response or the confidence estimate:

```
cd /methods/UCE/infer
python infer_answer_and_conf.py \
    --model_path model_ckp \
    --data_path test_data_path \
    --response_mode conf \ # you must choose a generation mode. "normal" mode requires the LLM to give a response for the given question, and the "conf" mode requires the LLM to provide the confidence estimate given the {question, response} pair
```

# The Baselines

We also provide the code of several popular confidence estimation methods. you can find on `/methods`

* P(IK): It trains a logistic regression with the additional value ``head" added to the model to output the confidence estimated. [[Language Models (Mostly) Know What They Know]](https://arxiv.org/abs/2207.05221)

  * Run:
    ```
    cd /methods/PIK
    python construct_data_PIK.py
    --model_path the_base_model_path
    --data_path  /data/test/CSQA_test.jsonP
    --save_path  save_data_path
    --sample_num 30
    --T 1
    --size 4 # the prompt size when using VLLM to infer
    ```
* First-Prob: It uses the logits of the first token of LLM's generated answer as the confidence estimate.  [[Whose Opinions Do Language Models Reflect?]](https://arxiv.org/abs/2303.17548)

  * Run:
    ```
    cd /methods/First-prob
    python inference_FirProb.py \
        --model_path the_base_model_path \
        --data_path  /data/test/CSQA_test.json \
        --save_path  save_data_path 
    ```
* SuC:  It first clusters the sub-questions, and use the same confidence estimate for questions in the same cluster. [[Teaching models to express their uncertainty in words]](https://arxiv.org/abs/2205.14334)

  * Run:
    ```
    cd /methods/SuC
    python construct_data_SuC.py \
        --model_path the_base_model_path \
        --data_path  /data/test/CSQA_test.json \
        --save_path  save_data_path \
        --sample_num 10 \
        --T 1 \
        --size 16
    ```
* Verb:  It is a prompt-based method. It designs the prompts to guide the model to output its confidence score alongside with the generated answer. [[Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback]](https://arxiv.org/abs/2305.14975)

  * Run:
    ```
    cd /methods/Verb
    python inference_Verb.py \
        --model_path the_base_model_path \
        --data_path  /data/test/CSQA_test.json \
        --save_path  save_data_path \
        --sample_num 10 \
        --T 1 \
        --size 16
    ```
* Fidelity: For MCQA, it decomposes the LLM confidence into the \emph{Uncertainty} about the question and the \emph{Fidelity} to the answer generated by LLMs. [[Calibrating the Confidence of Large Language Models by Eliciting Fidelity]](https://arxiv.org/abs/2404.02655)

  * Data example: ` /data/Fidelity/chains-confidence.json and /data/Fidelity/raw-10-responses.json`
  * Run:

    ```
    cd /methods/Fidelity
    python inference_chain.py \
        --model_path the_base_model_path \
        --data_path  /data/Fidelity/chains-confidence.json \
        --save_path  /data/Fidelity/raw-10-responses.json

    ```

  *PS: this method is only used for MCQA task*
* LECO: It also proposes leveraging logits to estimate step confidence. Besides, it further designs three logit-based scores that comprehensively evaluate confidence from both intra- and inter-step perspectives. [ [Learning From Correctness Without Prompting Makes LLM Efficient Reasoner]](https://arxiv.org/abs/2403.19094)

  * Run:
    ```
    cd /methods/LECO
    python inference_LECO.py \
        --model_path the_base_model_path \
        --data_path  /data/test/CSQA_test.json \
        --save_path  save_data_path 
    ```
* Multi-Step: It also uses prompts to guide the model to output the process confidence and takes the average as the final result. [[Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms]](https://arxiv.org/abs/2306.13063)

  * Run:
    ```
    cd /methods/Multistep
    python inference_MultiStep.py \
        --model_path the_base_model_path \
        --data_path  /data/test/CSQA_test.json \
        --save_path  save_data_path \
        --sample_num 10 \
        --T 1 \
        --size 16
    ```

# Results

We demonstrate that **base models provide the accurate confidence estimates for any given text sequence on three datasets after using UCE**. The overall results are shown in Table1 and Table2. The results in these two tables are the average values. Particularly, **our method consistently outperforms all baselines in terms of ECE and AUROC, and shows excellent calibration capability across all datasets.** 

![Table1](image/Table1.jpg)
![Table2](image/Table2.jpg)

