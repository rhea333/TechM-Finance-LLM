# Finance LLM

This repository contains our Finance Language Model (LLM), which is a fine-tuned version of the Merlinite LLM. Our goal was to create a model that excels in finance-related tasks. Below, you’ll find details about the dataset, model fine-tuning process, deployment, and steps to replicate our work.

## Overview

We fine-tuned the Merlinite LLM using over 5.5 MB of finance-related content collected from public domains. The fine-tuning process was conducted using Instruct Lab, and we evaluated the model’s performance using Retrieval-Augmented Generation (RAG) metrics.

Additionally, we deployed a Flask app as the user interface for the model. Initially, we hosted the model on HuggingFace, but due to memory size issues, we hosted locally using Instruct Lab's serve functionality.

## Features

Fine-Tuned Model: Based on the Merlinite LLM, specifically adapted for finance-related content.
Dataset: Hosted on a MongoDB database, containing over 5.5 MB of finance-related content.
Flask App: A front-end interface for users to interact with the model.
Deployment: Initially hosted on HuggingFace, later migrated to local hosting due to memory constraints.

## Instruct Lab Workflow

To replicate our fine-tuning and deployment process using Instruct Lab, follow these steps:

1. Download the instructlab folder 
2. Open up a new terminal window and navigate to the downloaded folder (cd instructlab)
3. Create an isolated Python virtual environment by typing the command `python3 -m venv` and then `source venv/bin/activate`
4. Update the config file to the one on Github by typing in `vim config.yaml` to the terminal
5. Update the qna file to the one on Github by navigating to taxonomy/knowledge/finance/qna.yaml and then typing "vim qna.yaml" to the terminal
6. Generate the model by typing in the command `ilab generate`
7. Train the model by typing in the command `ilab train`
6. Then you can chat with the model in ilab cli by typing `ilab chat`

## How to Use

Clone the Repository:

```
git clone https://github.com/yourusername/finance-llm.git
cd finance-llm
```

Run the Flask App:

```
flask run
```

Access the app in your browser at `http://localhost:5000.`

## The Webscraping Folder 

Inside the webscraping folder you will find the data cumulated for finance. We have collected data such as investing strategies, real time stocks, finance terms, etc. We have used python scripts to webscrape this data and use it to Finetune a LLM for personal finance. 
