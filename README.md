# AI Agentic Workspaces 🤖

A modular repository featuring autonomous AI Agents built with the **Agno** (formerly Phidata) framework, leveraging **Groq** (Qwen-3 32B) for rapid inference. This workspace includes structural agents handling system diagnostics, financial analytics, persistent SQLite memory tracking, and multi-agent team orchestrations.

---

## 📁 Repository Structure

```
├── .env                  # Private API credentials (GROQ_API_KEY, etc.)
├── agno.db               # SQLite database handling state and memory tracking
├── finance.py             # AI Financial Analyst leveraging YFinance and web search
├── memory.py              # Persistent travel agent utilizing user profiling and SQLite history
├── team.py                # Orchestrated Multi-Agent team systems
├── yt.py                  # Core engine for semantic YouTube video analysis
├── ui.py                  # Streamlit frontend user interface for the YouTube Analyzer
└── requirements.txt       # Engine dependency manifest
```

---

## 🚀 Features & Agents

### 1. 📺 YouTube Transcript & Video Analyzer (`yt.py` & `ui.py`)
An advanced media analyst that automatically ingests a YouTube URL, securely downloads the transcript data using `youtube-transcript-api`, and builds a structured breakdown.

- **UI:** Backed by a clean Streamlit user interface.
- **Output:** Chronological timestamp matrices, key tactical takeaways, and content profiling tags.

### 2. 📈 AI Investment Analyst (`finance.py`)
A comprehensive market analyst that evaluates equity tickers.

- **Hierarchical Routing:** Prioritizes programmatic fetching via `YFinanceTools` before falling back to semantic `DuckDuckGoTools` pipelines.
- **Capabilities:** Pulls live market valuations, computes dynamic currency pairs (e.g., USD → INR natively via currency indices), and surfaces Wall Street sentiment/recommendations.

### 3. 🧠 Persistent Memory Agent (`memory.py`)
An execution model validating cross-session conversational mapping.

- Uses a `SqliteDb` backend to catalog chat logs.
- Employs `enable_user_memories` and `agent.memory_manager` to maintain long-term user profiling across distinct execution windows.

### 4. 👥 Multi-Agent Team Orchestration (`team.py`)
Coordinates multiple specialized agents into a single collaborative workflow, routing tasks between them for combined output.

---

## 🛠️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

**2. Install dependencies**

Requires Python 3.10+.
```bash
pip install -r requirements.txt
```

**3. Configure environment variables**

Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_actual_groq_api_key_here
```

---

## 💻 Running the Applications

**Run the terminal agents:**
```bash
python finance.py
python memory.py
python team.py
```

**Launch the web UI:**
```bash
streamlit run ui.py
```

---

## 🌐 Cloud Deployment

This workspace is optimized for Streamlit Community Cloud:

1. Push your repository to GitHub (ensure `.env` is excluded via `.gitignore`).
2. Log in to [share.streamlit.io](https://share.streamlit.io).
3. Connect your repository and set the entry point file to `ui.py`.
4. Add your `GROQ_API_KEY` under **Advanced Settings → Secrets** before deploying.

---

## 📄 License

This project is open source. Add your preferred license (e.g., MIT) here.
