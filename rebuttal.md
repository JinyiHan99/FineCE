| Datasets | Process | Metrics |Multi-Step |LECO | FineCE |Multi-Step | LECO |FineCE |
|----------|---------|---------|------------------------|-------------------|---------------------|------------------------|-----------------|-------------------|
| GSM8K    | para(1) | ECE     | 27.4                   | 21.1              | 15.7                | 23.6                   | 21.1            | 14.1              |
|          |         | AUROC   | 60.8                   | 62.2              | 66.2                | 64.7                   | 64.4            | 66.8              |
|          | para(z-1)| ECE    | 29.7                   | 23.7              | 17.3                | 25.2                   | 20.4            | 14.4              |
|          |         | AUROC   | 62.3                   | 64.7              | 69.4                | 63.8                   | 65.3            | 65.3              |
|          | avg     | ECE     | 28.3                   | 19.2              | 12.3                | 19.2                   | 20.1            | 10.7              |
|          |         | AUROC   | 62.4                   | 68.2              | 72.7                | 67.2                   | 64.1            | 76.4              |
| CSQA     | para(1) | ECE     | 29.4                   | 22.4              | 16.6                | 27.6                   | 19.2            | 17.3              |
|          |         | AUROC   | 61.0                   | 63.1              | 66.3                | 63.9                   | 62.0            | 68.1              |
|          | para(z-1)| ECE    | 33.0                   | 26.3              | 17.9                | 24.4                   | 20.8            | 17.1              |
|          |         | AUROC   | 57.2                   | 62.9              | 67.5                | 62.0                   | 63.9            | 68.2              |
|          | avg     | ECE     | 29.3                   | 23.1              | 13.3                | 25.0                   | 17.6            | 14.7              |
|          |         | AUROC   | 59.3                   | 65.0              | 71.1                | 65.5                   | 65.3            | 73.2              |
| TriviaQA | para(1) | ECE     | 27.9                   | 21.4              | 18.7                | 26.4                   | 22.7            | 19.3              |
|          |         | AUROC   | 63.4                   | 60.7              | 69.2                | 61.9                   | 62.1            | 67.4              |
|          | para(z-1)| ECE    | 26.3                   | 20.9              | 20.3                | 30.2                   | 23.4            | 17.5              |
|          |         | AUROC   | 62.0                   | 63.4              | 67.7                | 59.4                   | 64.4            | 71.1              |
|          | avg     | ECE     | 25.1                   | 19.3              | 14.2                | 25.3                   | 20.2            | 13.4              |
|          |         | AUROC   | 63.7                   | 62.6              | 73.3                | 63.2                   | 64.0            | 73.9              |

*(5-2) Additional Experiments Table2: The confidence estimation results for question-oriented and outcome-oriented tasks based on  LLaMA-3.1-8B and Qwen-2.5-7B across GSM8k(columns 4~6), CSQA(columns 7~9), TriviaQA(columns 10~12) three datasets.*

| Base Model | Baseline | ACC | ECE | AUROC | ACC | ECE | AUROC | ACC | ECE | AUROC |
|------------|----------|-----------|-----------|-------------|----------|----------|------------|--------------|--------------|----------------|
| Llama3.1-8B | P(IK)    | 57.4      | 17.6      | 72.8        | 71.0     | 19.4     | 68.7       | 73.3         | 20.4         | 67.7           |
|            | FineCE   | 61.7      | 13.5      | 76.4        | 77.4     | 16.0     | 68.4       | 73.9         | 15.5         | 69.8           |
|            | First-Prob | 69.4    | 26.2      | 66.2        | 76.4     | 23.5     | 66.8       | 76.1         | 24.9         | 65.1           |
|            | SuC      | 60.1      | 28.4      | 62.0        | 76.2     | 32.7     | 59.1       | 70.8         | 29.7         | 60.4           |
|            | Verb     | 72.8      | 20.4      | 72.9        | 78.3     | 28.0     | 68.4       | 74.4         | 30.1         | 69.1           |
|            | FineCE   | 61.7      | 12.7      | 77.1        | 77.4     | 14.2     | 72.8       | 73.9         | 14.6         | 70.5           |
| Qwen2.5-7B | P(IK)    | 70.7      | 17.4      | 68.3        | 77.9     | 16.3     | 68.4       | 73.0         | 21.6         | 67.9           |
|            | FineCE   | 73.4      | 11.4      | 72.3        | 81.1     | 14.7     | 70.6       | 77.0         | 15.2         | 69.2           |
|            | First-Prob | 79.4    | 25.4      | 66.4        | 80.7     | 26.6     | 65.2       | 80.2         | 25.9         | 62.3           |
|            | SuC      | 74.1      | 29.0      | 57.4        | 79.2     | 28.2     | 63.1       | 74.3         | 32.7         | 58.5           |
|            | Verb     | 83.6      | 15.3      | 72.2        | 87.3     | 12.4     | 70.3       | 79.4         | 22.0         | 68.4           |
|            | FineCE   | 73.4      | 10.2      | 75.3        | 81.1     | 13.1     | 70.8       | 77.3         | 15.4         | 72.5           |

From these results, we observe that our method consistently outperforms all baselines in terms of ECE and AUROC, and shows excellent calibration capability.


**1. About the lack of some Related Work:** The related works you mentioned employed the models' internal parameters or structural information to assess their capability to address specific questions. In contrast, our paper focuses on providing fine-grained and accurate confidence estimates throughout the entire model generation process. Due to space limitations and rationality, we only discuss the work that is closest to our method.
**2. Compare with the Token-level baselines:** To the best of our knowledge, existing work rarely considers confidence estimation at the token-level, particularly for general tasks (which is the focus of our work). The inherent difficulty in evaluating confidence score at the token level. Besides, it is uncessary to estimate confidence after each token, as detailed in Section 3.2.2. Therefore, we provide several potential calibration positions.
**3. Compare with uncertainty-aware decoding method:** Our method is independent of the decoding strategy. We repeatedly mention in the main paper that our method provides accurate confidence estimates for any text.

For not using self-consistency as a baseline, because it is fundamentally unsuitable for confidence estimation tasks. Specifically, for the generation task, the self-consistency method identifies the answer with the highest frequency as the best answer. However, for the confidence estimation task, using the frequency of the most common answer as a proxy for confidence score can be misleading, especially during the testing stage without ground truth. Confidence estimation aims to measure the probability of generating the correct answer, which may not align with the frequency-based approach of self-consistency.


Including more LLMs, such as Llama 3, would strengthen the study's scope.
The term 'paragraph' in Table 1 is unclear, especially since the question pertains to only one paragrap

**1. Fig improvement:** We actually had previously attempted to use specific examples to illustrate the data construction process and BCI strategy. However, since our method involves multiple rounds of sampling, we found that using concrete examples made the figure less clear and concise. Therefore, we use formalized diagrams to represent. We appreciate your suggestion and plan to add examples in the appendix for better understanding.

**2. Detailed description about paragraph** Thank you again for reading our paper! *para(1)* means performs confidence estimation after the first paragraph text generation. Moreover, if the generated answer is only one paragraph, it means that the confidence check is performed after the entire generated answer at this time. FineCE can provide accurate confidence estimation for any given text in the generation process.

**3. More base models:** Thanks for your suggestion, we recently added another two popular and commonly used llms, including LLaMA-3.1-8B and Qwen-2.5-7B, to verify the effectiveness of our proposed method. The experimental results are as follows:
*(3-1)Additional Experiments Table 1: Confidence estimation results throughout the generation process based on  LLaMA-3.1-8B (columns 4～6) and Qwen-2.5-7B(columns 7~9 ).*
| Datasets | Process | Metrics |Multi-Step |LECO | FineCE |Multi-Step | LECO |FineCE |
|----------|---------|---------|------------------------|-------------------|---------------------|------------------------|-----------------|-------------------|
| GSM8K    | para(1) | ECE     | 27.4                   | 21.1              | 15.7                | 23.6                   | 21.1            | 14.1              |
|          |         | AUROC   | 60.8                   | 62.2              | 66.2                | 64.7                   | 64.4            | 66.8              |
|          | para(z-1)| ECE    | 29.7                   | 23.7              | 17.3                | 25.2                   | 20.4            | 14.4              |
|          |         | AUROC   | 62.3                   | 64.7              | 69.4                | 63.8                   | 65.3            | 65.3              |
|          | avg     | ECE     | 28.3                   | 19.2              | 12.3                | 19.2                   | 20.1            | 10.7              |
|          |         | AUROC   | 62.4                   | 68.2              | 72.7                | 67.2                   | 64.1            | 76.4              |
| CSQA     | para(1) | ECE     | 29.4                   | 22.4              | 16.6                | 27.6                   | 19.2            | 17.3              |
|          |         | AUROC   | 61.0                   | 63.1              | 66.3                | 63.9                   | 62.0            | 68.1              |
|          | para(z-1)| ECE    | 33.0                   | 26.3              | 17.9                | 24.4                   | 20.8            | 17.1              |
|          |         | AUROC   | 57.2                   | 62.9              | 67.5                | 62.0                   | 63.9            | 68.2              |
|          | avg     | ECE     | 29.3                   | 23.1              | 13.3                | 25.0                   | 17.6            | 14.7              |
|          |         | AUROC   | 59.3                   | 65.0              | 71.1                | 65.5                   | 65.3            | 73.2              |
| TriviaQA | para(1) | ECE     | 27.9                   | 21.4              | 18.7                | 26.4                   | 22.7            | 19.3              |
|          |         | AUROC   | 63.4                   | 60.7              | 69.2                | 61.9                   | 62.1            | 67.4              |
|          | para(z-1)| ECE    | 26.3                   | 20.9              | 20.3                | 30.2                   | 23.4            | 17.5              |
|          |         | AUROC   | 62.0                   | 63.4              | 67.7                | 59.4                   | 64.4            | 71.1              |
|          | avg     | ECE     | 25.1                   | 19.3              | 14.2                | 25.3                   | 20.2            | 13.4              |
|          |         | AUROC   | 63.7                   | 62.6              | 73.3                | 63.2                   | 64.0            | 73.9              |

*(3-2)Additional Experiments Table2: The confidence estimation results for question-oriented and outcome-oriented tasks based on  LLaMA-3.1-8B and Qwen-2.5-7B across GSM8K (columns 4\~6) , CSQA(columns 7\~9) , TriviaQA(columns 10\~12) three datasets.*

| Base Model | Baseline | ACC | ECE | AUROC | ACC | ECE | AUROC | ACC | ECE | AUROC |
|------------|----------|-----------|-----------|-------------|----------|----------|------------|--------------|--------------|----------------|
| Llama3.1-8B | P(IK)    | 57.4      | 17.6      | 72.8        | 71.0     | 19.4     | 68.7       | 73.3         | 20.4         | 67.7           |
|            | FineCE   | 61.7      | 13.5      | 76.4        | 77.4     | 16.0     | 68.4       | 73.9         | 15.5         | 69.8           |
|            | First-Prob | 69.4    | 26.2      | 66.2        | 76.4     | 23.5     | 66.8       | 76.1         | 24.9         | 65.1           |
|            | SuC      | 60.1      | 28.4      | 62.0        | 76.2     | 32.7     | 59.1       | 70.8         | 29.7         | 60.4           |
|            | Verb     | 72.8      | 20.4      | 72.9        | 78.3     | 28.0     | 68.4       | 74.4         | 30.1         | 69.1           |
|            | FineCE   | 61.7      | 12.7      | 77.1        | 77.4     | 14.2     | 72.8       | 73.9         | 14.6         | 70.5           |
| Qwen2.5-7B | P(IK)    | 70.7      | 17.4      | 68.3        | 77.9     | 16.3     | 68.4       | 73.0         | 21.6         | 67.9           |
|            | FineCE   | 73.4      | 11.4      | 72.3        | 81.1     | 14.7     | 70.6       | 77.0         | 15.2         | 69.2           |
|            | First-Prob | 79.4    | 25.4      | 66.4        | 80.7     | 26.6     | 65.2       | 80.2         | 25.9         | 62.3           |
|            | SuC      | 74.1      | 29.0      | 57.4        | 79.2     | 28.2     | 63.1       | 74.3         | 32.7         | 58.5           |
|            | Verb     | 83.6      | 15.3      | 72.2        | 87.3     | 12.4     | 70.3       | 79.4         | 22.0         | 68.4           |
|            | FineCE   | 73.4      | 10.2      | 75.3        | 81.1     | 13.1     | 70.8       | 77.3         | 15.4         | 72.5           |

From these results, we observe that our method consistently outperforms all baselines in terms of ECE and AUROC, and shows excellent calibration capability.



# 3/31 补充实验



| Baseline    | AIME24       |              |                |MMLU          |              |              | nq_open        |               |               | 
|-------------|--------------|--------------|----------------|--------------|--------------|--------------|----------------|---------------|---------------|
|             | ACC          | ECE          | AUROC          | ACC          | ECE          | AUROC          | ACC          | ECE          | AUROC          |
| **Llama3.1-8B** |          |              |                |              |              |                |              |              |                |
| P(IK)       | 10.0         | 33.1         | 67.9           | 48.4         | 18.3         | 72.1           | 46.1         | **22.4**         | 68.2           |
| FineCE      | **13.3**         | **18.5**         | **73.1**           | **54.8**         | **14.3**         | **76.2**           | 48.2         | 20.9         | **73.1**           |
| First-Prob  | **13.3**         | 40.3         | 65.0           | 53.1         | 21.4         | 68.4           | 49.3         | 29.4         | 66.5           |
| SuC         | 10.0         | 42.7         | 62.2           | 50.9         | 24.7         | 66.3           | 45.6         | 27.3         | 61.4           |
| Verb        | **13.3**        | 73.4         | 6.1            | **55.6**         | 31.2         | 62.7           | **50.4**         | 34.0         | 65.2           |
| SE          | **13.3**         | 20.9         | 68.5           | 54.2         | 17.2         | 71.2           | 47.7         | 22.3         | 70.4           |
| FineCE      | **13.3**         | **20.7**         | **70.4**           | 54.8        | **12.1**         | **74.1**           | 48.2         | **17.1**         | **75.1**           |
| **Qwen2.5-7B** |            |              |                |              |             |                |              |              |                |
| P(IK)       | 13.3         | 27.9         | 66.3           | 54.1         | 16.1         | 69.8           | 40.3         | 20.8         | 72.3           |
| FineCE      | **20.0**         | **21.2**         | **76.2**           | **60.6**         | **15.6**        | **73.1**          | **43.6**         | **17.4**         | **76.2**           |
| First-Prob  | 16.7         | 35.8         | 57.4           | 60.2         | 30.3         | 68.0           | 41.4         | 24.5         | 68.5           |
| SuC         | 16.7         | 38.4         | 60.4           | 58.3         | 27.0         | 62.4           | 40.0         | 24.1         | 63.1           |
| Verb        | 13.3         | 78.7         | 11.3           | 60.2         | 29.4         | 63.3           | 42.9         | 33.6         | 62.4           |
| SE          | **20.0**         | 25.1         | 73.5           | **60.6**        | 22.4         | 68.3           | 41.7         | 23.8         | 71.8           |
| FineCE      | **20.0**         | **17.7**         | **81.3**           | **60.6**         | **16.3**         | **75.7**           | **43.6**         | **15.3**         | **77.8**           |
| **Llama2-13B** |            |              |               |             |              |                |              |               |                |
| P(IK)       | 0           | 31.4         | 72.1           | 38.4         | 17.3         | 67.6           | 35.2         | 18.3         | 70.7           |
| FineCE      | **3.3**         | **24.8**         | **78.4**           | **43.1**         | **15.0**         | **72.6**          | **40.6**         | **13.9**         | **74.3**           |
| First-Prob  | **3.3**         | 42.0         | 61.2           | 39.3         | 19.4         | 64.3           | 39.2         | 22.1         | 65.1           |
| SuC         | 0           | 37.3         | 57.3           | 40.3         | 22.1         | 65.2           | 37.1         | 24.6         | 66.4           |
| Verb        | **3.3**         | 82.3         | 14.9           | 43.9         | 32.6         | 61.1           | 41.5         | 29.8         | 62.4           |
| SE          | **3.3**         | 32.7         | 65.1           | 42.5         | 20.3         | 69.4           | 40.0         | 24.1         | 70.2           |
| FineCE      | **3.3**         | **16.2**         | **75.3**           | **43.1**         | **14.8**         | **75.4**         | **40.6**         | **14.2**         | **74.6**           |







## table2
| Process  | Metrics| Llama2-13B        | |    |Llama3.1-8B     |           |  |Qwen2.5-7B|||
| ---------  |---------|------- |-----    |------   |--------|---------|-------  |-----   |------   |---------|
|            |         | MS     | LECO    | FineCE  | MS     | LECO    | FineCE  | MS     | LECO    | FineCE  |
| **AIME24**       |         |        |  |     ||| |   |  ||
| para(1)    | ECE     | 57.4   | 37.4    | **19.3**    | 60.3   | 31.2    | **21.5**    | 64.3   | 33.7    | **22.4**    |
|            | AUROC   | 21.4   | 56.3    | **68.4**    | 16.2   | 63.4    | **69.8**    | 25.3   | 64.1    | **74.1**    |
| para(z-1)  | ECE     | 64.3   | 34.3    | **22.4**    | 57.2   | 29.4    | **23.5**    | 76.8   | 30.2    | **21.3**    |
|            | AUROC   | 25.4   | 59.4    | **71.3**   | 25.3   | 66.3    | **68.4**    | 11.6   | 65.2    | **76.2**    |
| avg        | ECE     | 59.2   | 33.8    | **16.5**    | 55.4   | 30.8    | **20.4**   | 72.3   | 29.6    | **18.3**    |
|            | AUROC   | 22.7   | 56.3    | **76.0**    | 19.5   | 64.1    | **71.3**    | 30.3   | 64.0    | **79.2**    |
|**MMLU**        |         |        |  |     ||| |   |  ||
| para(1)    | ECE     | 27.6   | 26.2    | **20.0**    | 30.3   | 27.8    | **20.2**    | 32.9   | 30.3    | **22.4**    |
|            | AUROC   | 57.4   | 61.3    | **74.3**    | 53.1   | 59.2    | **70.3**    | 54.1   | 60.3    | **70.2**    |
| para(z-1)  | ECE     | 29.4   | 28.1    | **18.9**    | 33.6   | 29.3    | **17.3**    | 33.4   | 28.7    | **19.3**    |
|            | AUROC   | 59.3   | 62.5    | **71.8**    | 56.4   | 61.3    | **73.1**    | 52.6   | 57.4    | **71.3**    |
| avg        | ECE     | 28.3   | 27.3    | **15.3**    | 28.9   | 26.9    | **14.1**    | 31.1   | 28.4    | **15.7**    |
|            | AUROC   | 58.9   | 60.5    | **74.6**    | 57.2   | 63..4   | **74.6**    | 58.4   | 61.2    | **74.2**    |
|**nq_open**     |         |        |  |     ||| |   |  ||
| para(1)    | ECE     | 30.1   | 26.0    | **17.8**    | 34.9   | 28.7    | **23.7**    | 35.1   | 29.4    | **17.5**    |
|            | AUROC   | 59.4   | 62.1    | **72.3**    | 55.8   | 61.0    | **72.3**    | 55.3   | 62.8    | **72.0**    |
| para(z-1)  | ECE     | 29.6   | 27.0    | **20.3**    | 29.2   | 26.3    | **18.1**    | 30.4   | 30.5    | **20.5**    |
|            | AUROC   | 60.4   | 57.3    | **70.9**    | 57.3   | 59.4    | **67.5**    | 58.1   | 61.3    | **70.3**    |
| avg        | ECE     | 27.4   | 25.7    | **14.2**    | 32.3   | 26.1    | **18.2**    | 32.8   | 28.6    | **16.4**    |
|            | AUROC   | 60.7   | 59.1    | **75.5**    | 57.9   | 62.3    | **74.7**    | 58.8   | 64.2    | **76.9**    |


Dear AC chair,

Thank you again for your insightful feedback on our manuscript. We have carefully addressed the reviewrs concerns by:

-Providing detailed responses
-Conducting additional experiments
-Supplementing relative references


谢谢您的时间以及审阅我们的论文，在过去的几天，我们对每一个人审稿人的担忧做出了详细的回复、并且添加了额外的数据集以及baseline来进一步说明我们方法的性能，但是均没有收到回复。更为重要的是，对于审稿人KfLT，我认为他并没有认真审阅我们的论文，主要基于以下几点：
1. 对我们的论文总结并不准确。
2. weakness中第一条提到的对于指标的担忧。在confidence estimation任务中AUROC是常用的一个指标，在很多论文中都有使用这个指标来评估方法的有效性[1][2][3][4]，但他提出了质疑，并且建议使用PRR，据我所知，这个指标在从这个任务中没有其他方法使用过这个指标
3. weakness中对于提到FineCE需要额外的训练：这个问题非常可笑，如果这也算是一个弱点，那么在大模型根本不存在各种各样后训练技术。
   
我曾尝试和审稿人KfLT沟通交流，并且希望他能够重新阅读我们的论文，但是均没有收到任何的回复。我希望你能够给基于我们提交的论文以及回复重新评估我们的工作。再次感谢您的时间。


Dear AC chair,
I hope this email finds you well. First, I would like to express my sincere gratitude for your time and guidance throughout the review process. Over the past few days, we have addressed each concern raised by the reviewers, providing point-by-point responses and supplementing our submission with additional datasets and baselines to further validate the advantages of our method. However, despite our efforts, we have not yet received follow-up feedback from the reviewers.

More importantly, after careful consideration, we believe that the reviewer KfLT may lack sufficient understanding of our manuscript, as evidenced by the following points:

- **Inaccurate Summary of Our Work**: In his/her Paper Summary, he/she mentioned that _FineCE is a method for real-time token-level confidence estimation._ This is inaccurate. FineCE introduces fine-grained confidence estimation for LLMs, but it's not a token-level confidence estimation method. To the best of our knowledge, existing work rarely considers confidence estimation at the token level, particularly for general tasks (which is the focus of our work). On the one hand, there is inherent difficulty in evaluating confidence scores at the token level. Besides, it is unnecessary to perform confidence calibration after each token generation due to the cost considerations. Therefore, we propose three strategies to identify optimal positions for confidence estimation during the generation process. We specifically discussed these points in Section 3.2.2. 
- **Concerns about evaluation metrics**: The reviewer first questioned the use of AUROC, yet this metric is widely adopted in confidence estimation research (e.g., [1][2][3][4]). Their suggested alternative, PRR, lacks precedent in related literature. 
  [1] Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs. 2024, ICLR
  [2] Detecting Hallucinations in Large Language Models Using Semantic Entropy. 2024, Nature
  [3] Large Language Models Must Be Taught to Know What They Don't Know. 2024, NeurIPS
  [4] Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation. 2023, ICLR
- **Post-training as a limitation**: Reviewer KfLT criticized our method for requiring additional training, labeling this as a weakness. However, post-training is a common practice in LLM research. And most of the existing work based on LLM is exploring the post-training techniques to enhance the capabilities of LLMs. Besides, in the Introduction section ("Task Learning: How to teach LLMs to express their confidence?" lines 80–91), we explicitly state that relying solely on the model's inherent capabilities is insufficient for accurate confidence estimation, and additional training is necessary. In fact, many works, such as [3][5], also adopt training-based method.
 [5]Language Models (Mostly) Know What They Know. Anthropic(2022)

We attempted to clarify these points with Reviewer KfLT and kindly requested a re-examination of our manuscript but received no response. Thank you again for your consideration. We deeply appreciate your efforts to ensure a fair review process and would be happy to provide further clarification if needed.

Best Regards,



## MI5 Author Response

**The meta-reviewer did not thoroughly evaluate our manuscript or consider the detailed responses we provided during the author rebuttal phase to address the reviewers' concerns. Instead, he/she appears to have merely reiterated the weaknesses raised by the reviewers without acknowledging our clarifications.​​** ​For each of these concerns, we had already provided comprehensive clarifications in the author response stage, which effectively address the issues raised. The reasoing is as follows: 

1. Meta-reviewer states "The computation cost seems high. Monte Carlo sampling and BCI seem to be increasing training/inference costs when the iteration and depth are high. (3KLR)”. But in the author response phase, we have replied:
> **Computation cost explanation:**
**During Inference:**  
In the main results (RQ1), we only require FineCE to generate outputs once to ensure a fair comparison with other baseline methods. Even so, our method still achieves the best performance on the confidence estimation task. Only in RQ3, to validate the effectiveness of the BCI method, do we investigate the impact of multiple inference runs on confidence estimation. The results demonstrate that using the BCI method significantly enhances the performance of confidence estimation. Furthermore, we observe that the performance improvement becomes more pronounced as the fusion width and depth increase. For further details and discussion, please refer to RQ3.
**During Training:** 
Compared to methods that rely solely on Monte Carlo sampling for questions, our approach does require a higher number of sampling operations. However, to mitigate this computational overhead, we have implemented a series of optimization strategies. Specifically, we first perform an initial sampling of the question and semantically cluster the multiple generated answers. Then, we select representative samples (i.e., centroids) from each cluster to continue sampling, while randomly setting a truncation position to further reduce computational costs. Additionally, since the model has already completed clustering during the early stages of answering, the subsequently generated texts tend to exhibit high similarity. So, we reduce the frequency of multi-branch sampling operations in the latter half of the response generation process.
Through these optimizations, the sampling complexity is reduced from the original exponential level $k \cdot \sum_{i=1}^{z} m^{i}$ to a linear complexity of $k \cdot (1 + m + m \cdot (z-1))$, significantly decreasing the computational overhead.  
Here, $z$ represents the average truncation count per question, $m$ denotes the number of clusters, and $k$ indicates the number of Monte Carlo sampling iterations.  

2. Meta-reviewer states "he authors adopted Monte-Carlo like methods to generate data, but I do not see a MC-like baseline for comparison.(Qesy)". In the response stage, we have provided additional clarification regarding the selected baseline and the differences of our proposed method:
> In the baseline we used, **both P(IK) and SuC employ the Monte Carlo method to construct training datasets**. These methods repeatedly sample a given question to generate multiple answers, subsequently estimating the probability of correct responses or performing clustering analysis based on semantic similarity among the generated answers. In contrast, FineCE introduces an additional step by applying Monte Carlo sampling to partial answers during the construction of the training data (lines 332–341). This innovation ensures that even when the model generates incomplete answers during inference, FineCE can still deliver accurate confidence estimates, thereby significantly enhancing its robustness and reliability.(lines 332–341)

3. Meta-reviewer states "The authors could include some experimental results on open questions, such as those presented in the rebuttal experiments." But in the author response phase, we have replied:
> As with other related works, FineCE's confidence estimation performance may be challenged on such highly opened tasks. Thus, we designed a dedicated set of experiments, detailed in **RQ8** of the Appendix. Specifically, we curated 300 representative highly open-ended questions from the ShareGPT dataset to evaluate FineCE's performance. We compared FineCE's output confidence scores against GPT-4’s evaluation of answer correctness. The experimental results demonstrate that FineCE achieves a relatively high  ECE on this task. This is because we did not use GPT4's evaluation to assist in constructing training data, resulting in a large difference between the confidence provided by the model and the GPT4 scoring results.
Furthermore, to further validate and demonstrate the effectiveness of FineCE, we add the experiments using the challenging mathematical problem AIME24[1], and two open-ended tasks: MMLU[2] and the question-answering nq_open[3]. We also add SE[3] as a baseline. It measures uncertainty according to the semantic equivalence of the generated answer. 



## MI7 Score Mismatch
1. The meta-review states "The current version is a little bit unclear. My suggestion is to add an overview or a flow chart of the whole pipeline to make readers understand the whole process. (3KLR)" Although this issue was pointed out, Reviewer 3KLR still gave us a score of 3. This indicates that the concern is likely subjective in nature and should be viewed as a suggestion for improvement rather than a critical weakness.


2. Furthermore, the meta-reviewer appears to have recognized some potential unreasonableness in the review provided by KfLT. However, the remaining two reviewers both gave scores of 3. Besides, the meta-reviewer also states:
>This paper introduces a new way to refine confidence scores by leveraging future context, while the accompanying data generation pipeline and exploration of optimal estimation positions further strengthen the approach. The improvement of the result is significant.

This indicates that the meta-reviewer also acknowledged the merit of our proposed method and the exciting results we achieved. Given these aspects, what's particularly puzzling is that the reviewer provided the final score was lowered to 2.5.





<!-- which doesn't meet the minimum requirement for the 'findings' classification."

基于上面的这些，令人很困惑的是审稿人给了一个连“findings” 都没机会中的2.5分 -->


<!-- We acknowledge that without accompanying manuscript explanations, the figure might be somewhat challenging for readers to follow. However, the Reviewer 3KLR assigned us a score of 3. Meanwhile, we explicitly stated our willingness to further revise this aspect in the author response stage.  -->

<!-- meta-review说“Unclear Pipeline: "The current version is a little bit unclear. My suggestion is to add an overview or a flow chart of the whole pipeline to make readers understand the whole process." (3KLR)” 我们也承认如果不结合正文文字说明来看图的话，对于读者来说有一点难懂。我们也表明了，我们会进一步的修改。但是，尽管这样的。 Reviewer 3KLR 还是给了我们3分。
此外，两个审稿人都给了3分，meta似乎也考虑了reviewer 给的分数的不太合理。但是我不能理解，为什么给出的分数是2.5。 和其他两个审稿人的差异很大。 -->

