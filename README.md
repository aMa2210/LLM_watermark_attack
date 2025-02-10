# LLM_watermark_attack

This repository contains the data and scripts used for analyzing the impact of various watermark removal attacks on LLM performance.

Repository Contents
- gpqa/Global_MMLU/MMLU_pro: Datasets used in the experiments.
- Results:
  - Contains the results of the experiments. The '{model name}_rawText' column contains the original responses from the model, while the '{model_name}' column includes the options extracted from these responses. 
- figure: Outputs and visualizations derived from the analysis.

- The Python script in the root directory is used for analyzing and plotting the data in the Results folder.
- The prompts used in the experiment can be found in System_Message.py.
