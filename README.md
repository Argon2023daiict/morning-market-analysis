---
title: Morning Market Brief
emoji: 📚
colorFrom: indigo
colorTo: gray
sdk: docker
pinned: false
---
---

# Morning Analysis Assistant

## Overview

**Morning Analysis Assistant** is a modular, open-source financial assistant that delivers concise, spoken market summaries and risk exposure updates using real-time data, document retrieval, and voice interaction. The assistant is designed for portfolio managers who need a verbal brief at the start of each trading day.

The system supports voice input, aggregates data from financial APIs and filings, uses a retrieval-augmented language model to generate insights, and returns a spoken output to the user through a lightweight interface.

---

## Use Case

Each morning at 8:00 AM, a portfolio manager asks:

**"What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"**

The system responds:

> "Asia tech allocation is currently 22%, up from 18% yesterday. TSMC beat estimates by 4%, while Samsung missed by 2%. Market sentiment remains neutral with a cautionary bias due to rising yields."

---

## Architecture

The project is structured using a multi-agent system powered by FastAPI. Each component handles a specific task in the analysis pipeline:

* **API Agent:** Pulls real-time and historical market data via Yahoo Finance.
* **Scraper Agent:** Extracts earnings and news headlines from Yahoo Finance pages.
* **Retriever Agent:** Uses Sentence Transformers to embed financial documents into FAISS for semantic search.
* **Analysis Agent:** Computes differences in stock allocation or earnings results.
* **Language Agent:** Generates a market summary using DeepSeek R1 (via Hugging Face).
* **Voice Agent:** Transcribes speech to text (Whisper) and synthesizes speech from text (gTTS).
* **Orchestrator:** A FastAPI backend that routes voice input through the agents and returns a voice/text response.
* **Frontend Interface:** Built-in web interface for uploading voice queries and hearing the result.

---

## Folder Structure

```
market_assistant/
├── data_ingestion/
│   ├── api_agent.py
│   └── scraper_agent.py
├── agents/
│   ├── retriever_agent.py
│   ├── analysis_agent.py
│   ├── language_agent.py
│   └── voice_agent.py
├── orchestrator/
│   └── orchestrator.py
├── docs/
│   └── ai_tool_usage.md
├── requirements.txt
├── Dockerfile
├── README.md
└── sample_data.txt
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/morning-analysis-assistant.git
cd morning-analysis-assistant
```

### 2. Create and Activate a Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Backend Server

```bash
uvicorn orchestrator.orchestrator:app --reload
```

---

## How It Works

1. The user uploads a `.wav` voice query via the web interface.
2. The system transcribes the audio using Whisper.
3. A retriever fetches relevant financial context using FAISS + Sentence Transformers.
4. DeepSeek R1 synthesizes a human-like narrative based on the context.
5. gTTS converts the generated summary to speech and returns it to the user.

---

## Example Input/Output

**Voice Input:**
"What’s the Asia tech risk today?"

**Generated Text Response:**
"Your exposure to Asia tech stands at 24%, up from 20% yesterday. Alibaba exceeded revenue expectations by 6%, while Baidu underperformed slightly. Regional sentiment remains stable."

**Audio Output:**
Returned as an `.mp3` file and played in the browser.

---

## Requirements

* Python 3.11
* Hugging Face Account (for DeepSeek R1)
* Internet access for APIs and Hugging Face inference
* `.wav` voice files for user input

---

## Deployment

This project is deployed using Hugging Face Spaces.

**Live Demo:**
[https://huggingface.co/spaces/rahulkumar110/morning-market-brief](https://huggingface.co/spaces/rahulkumar110/morning-market-brief)

---

