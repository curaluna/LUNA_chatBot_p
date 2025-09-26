# luna-chatbot-p · Quickstart

---

## 1) Create & activate a virtual environment (venv)

### Windows

1. **Create**

   ```powershell
   py -m venv .venv
   ```
2. **Activate (PowerShell)**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   *CMD variant*: `\.venv\Scripts\activate.bat`

### macOS · Fedora

1. **Create**

   ```bash
   python3 -m venv .venv
   ```
2. **Activate**

   ```bash
   source .venv/bin/activate
   ```

> **Optional (recommended):** update pip

```bash
python -m pip install --upgrade pip
```

---

## 2) Install dependencies

Run these inside the activated venv:

```bash
pip install -r requirements/core.txt
pip install -r requirements/ui.txt
```

---

## 3) Setup environment file (.env) & API Key

1. **Copy template**

   * **Windows (PowerShell)**

     ```powershell
     Copy-Item .env.template .env
     ```

   * **macOS · Fedora**

     ```bash
     cp .env.template .env
     ```

2. **Insert AI API Key**
   Open `.env` in your editor and add your key:

   ```dotenv
   AI_API_KEY=your_api_key_here
   ```

> ⚠️ **IMPORTANT:** Never write secrets into the template file (`.env.template`). Only use **`.env`** – and make sure it’s listed in `.gitignore`.

---

## 4) Provide PDFs for ingestion

Place all PDF files that should be considered in the RAG process into:

```
data/pdfs/
```

---

## 5) Ingest the VectorStore

### macOS · Fedora

```bash
python -m src.app.rag.ingest
```

### Windows (PowerShell)

```powershell
py -m src.app.rag.ingest
```

> Always run ingest **after** activating the venv.

---

## 6) Start the app

Run the Chainlit app with:

```bash
chainlit run app-chainlit-app.py -w
```

---

## 7) Handy commands

* **Leave venv**: `deactivate`
* **Update packages**: `pip install --upgrade <package>`
* **Check Python path**: `which python` (macOS/Fedora) · `where python` (Windows)
