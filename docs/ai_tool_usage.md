# AI Tool Usage Log – Morning Analysis Assistant

This document logs the configuration and usage of all AI tools and frameworks used in the **Morning Analysis Assistant** project.

---

## 1. **Speech-to-Text (STT)**

### Tool: [Whisper](https://github.com/openai/whisper)

* **Model Used:** `base`
* **Installed via:**
  `pip install git+https://github.com/openai/whisper.git`
* **Purpose:** Converts `.wav` voice input into English text.
* **Example Call:**

  ```python
  model = whisper.load_model("base")
  result = model.transcribe("input.wav")
  transcribed_text = result['text']
  ```

---

## 2. **Embeddings**

### Tool: [Sentence Transformers](https://www.sbert.net/)

* **Model Used:** `all-MiniLM-L6-v2`
* **Source:** Hugging Face Transformers
* **Purpose:** Generate dense embeddings for financial documents used in retrieval.
* **Vector DB:** FAISS
* **Retrieval Strategy:** Top-3 semantic matches using cosine similarity
* **Example:**

  ```python
  from sentence_transformers import SentenceTransformer
  model = SentenceTransformer("all-MiniLM-L6-v2")
  embeddings = model.encode(["doc1", "doc2"])
  ```

---

## 3. **Language Generation**

### Tool: [DeepSeek R1](https://huggingface.co/deepseek-ai/deepseek-llm)

* **Accessed via:** [Together AI API](https://api.together.xyz/)
* **Purpose:** Generates market summary based on retrieved financial documents.
* **Framework:** Used within LangChain’s `LLMChain` or `RetrievalQA` interface.
* **Prompt Example:**

  ```json
  {
    "model": "deepseek-llm-r1",
    "prompt": "Summarize earnings and risk from the following: <retrieved_text>",
    "max_tokens": 500,
    "temperature": 0.3
  }
  ```
* **Why Together AI:** Lower latency, free tier, and allows easier integration compared to OpenAI.

---

## 4. **Text-to-Speech (TTS)**

### Tool: [gTTS (Google Text-to-Speech)](https://pypi.org/project/gTTS/)

* **Language:** English (`'en'`)
* **Purpose:** Converts LLM-generated summaries into audio.
* **Output Format:** `.mp3` audio file returned to user.
* **Example:**

  ```python
  from gtts import gTTS
  tts = gTTS(text=summary, lang='en')
  tts.save("output.mp3")
  ```

---

## 5. **Backend Server & Orchestration**

### Tools:

* **FastAPI:** Framework to define endpoints and orchestrate all agents.

* **Uvicorn:** ASGI server to serve the FastAPI app locally or in production.

* **Startup Command:**

  ```bash
  uvicorn orchestrator.orchestrator:app --reload
  ```

* **Key Responsibilities:**

  * Accept audio input
  * Run STT → Retrieval → LLM → TTS in sequence
  * Return both text and audio response

---

## 6. **Deployment**

### Platform: [Hugging Face Spaces](https://huggingface.co/spaces)

* **Frontend/Backend:** Hosted together in a single app using `FastAPI`.

* **Demo URL:**
  [https://huggingface.co/spaces/rahulkumar110/morning-market-brief](https://huggingface.co/spaces/rahulkumar110/morning-market-brief)

* **Reason for Choosing:** Free GPU/CPU hosting, public visibility, easy integration with Hugging Face models and APIs.

---

## Summary of AI Components

| Component      | Tool/Service               | Configuration                    |
| -------------- | -------------------------- | -------------------------------- |
| STT            | Whisper                    | base model                       |
| Embeddings     | Sentence Transformers      | all-MiniLM-L6-v2                 |
| Retriever      | FAISS                      | k=3 nearest chunks               |
| Language Model | DeepSeek R1 (via Together) | Prompt-based summary generation  |
| TTS            | gTTS                       | lang='en', mp3 output            |
| API Server     | FastAPI + Uvicorn          | Orchestrates full voice pipeline |

---
