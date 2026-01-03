# Data Roaster 🥩🔥

### AI-Powered Data Profiling & Quality Assurance Platform

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED)
![AI](https://img.shields.io/badge/AI-Llama%203.1%208B-purple)

**Data Roaster** is a production-ready ETL utility designed to automate data integrity validation for industrial and ERP datasets. It solves the "garbage in, garbage out" problem by combining hard statistical profiling with Generative AI to "roast" (critique) low-quality extracts from legacy systems like JD Edwards, Oracle, or SAP.

---

## 🎯 The Problem

In industrial environments, data engineers often receive raw extracts (Excel/CSV) full of inconsistencies, nulls, and duplicates. Validating this manually is slow, error-prone, and tedious.

## 💡 The Solution

Data Roaster acts as an intelligent gatekeeper. It uses a **Hybrid Architecture**:

1.  **Deterministic Layer (Pandas):** Calculates exact metrics (memory usage, sparsity, cardinality, duplicate detection).
2.  **Semantic Layer (GenAI):** Uses **Llama 3.3 70B** (via Groq API) to interpret these metrics and provide a sarcastic, human-like critique of the dataset's quality.

---

## 🛠️ Tech Stack & Architecture

* **Core:** Python 3.10+
* **ETL Engine:** Pandas & NumPy (Vectorized operations for performance).
* **Artificial Intelligence:** Groq API (Llama 3.1 8B Instant) for high-speed inference.
* **Web Framework:** Flask (Modular Blueprint Architecture).
* **Containerization:** Docker.
* **Reporting:** ReportLab (Dynamic, multi-page PDF generation with auto-paging).
* **Security:** Environment variable management via `python-dotenv`.

---

## ✨ Key Features

* **Format Agnostic:** Seamless ingestion of `.csv` and `.xlsx` files.
* **AI-Driven Insights:** The system "talks" to you, explaining *why* the data is bad, not just showing numbers.
* **Robust PDF Reporting:** Generates a professional PDF report that handles text wrapping, auto-pagination, and detailed integrity breakdowns (nulls per column).
* **Fallback Mechanism:** Robust design—if the AI API is unreachable, the system automatically degrades to rule-based validation without crashing.
* **Deep Profiling:** Memory footprint analysis to prevent server crashes on large loads.

---

## 🚀 How to Run

### Option A: Using Docker (Recommended)

Ensure you have Docker installed.

1.  **Build the Image:**
    ```bash
    docker build -t data-roaster .
    ```

2.  **Run the Container:**
    (This mounts the `reports` volume so you can access the generated PDFs on your host machine).
    ```bash
    # Linux/Mac
    docker run -p 5000:5000 --env-file .env -v $(pwd)/reports:/app/reports data-roaster

    # Windows (PowerShell)
    docker run -p 5000:5000 --env-file .env -v ${PWD}/reports:/app/reports data-roaster
    ```

### Option B: Local Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/LuizMartinsz/data-roaster.git](https://github.com/LuizMartinsz/data-roaster.git)
    cd data-roaster
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration (.env)**
    Create a `.env` file in the root directory and add your Groq API Key:
    ```env
    GROQ_API_KEY=gsk_your_key_here
    ```

5.  **Run the Application**
    ```bash
    python run.py
    ```
    Access the dashboard at `http://127.0.0.1:5000`

---

## 📊 Example Output

**Input:** A CSV with 20% duplicate rows and missing cost centers.

**Output (AI Roast):**

> **🤖 [AI OPINION]:**
> "Listen to me: you have 20% duplicate rows and the 'Cost_Center' column is 40% null. This isn't a dataset, it's a piece of swiss cheese. Do not load this into the Data Warehouse unless you want to break the nightly build."

---

## 📂 Project Structure

```text
data-roaster/
├── app/
│   ├── templates/      # HTML Dashboard
│   ├── routes.py       # Flask Blueprints
│   └── __init__.py     # App Factory
├── etl/
│   ├── ai_roaster.py   # AI Integration (Llama 3.3)
│   ├── pdf_gen.py      # PDF Engine (ReportLab)
│   └── roaster.py      # Core Logic (Pandas + Rules)
├── reports/            # Generated PDFs
├── .dockerignore
├── Dockerfile
├── requirements.txt
├── run.py              # Entry Point
└── README.md
```

## 👨‍💻 About the Author

**Luiz Martins**
*Senior Data Analyst & Automation Specialist*

I build tools that bridge the gap between legacy industrial systems (JD Edwards, OpenEdge) and modern data engineering pipelines. Focus on Process Automation, Python, and IoT.


*Built for portfolio demonstration. Clean Code | OOP | Secure.*

