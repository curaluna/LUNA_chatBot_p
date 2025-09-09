# Installation Instructions

## 1. Install Python 3

Make sure Python 3 is installed on your system.

**Windows (using Chocolatey):**
```sh
choco install python
```

**macOS (using Homebrew):**
```sh
brew install python
```

**Ubuntu/Debian:**
```sh
sudo apt update
sudo apt install python3 python3-venv
```

**Fedora:**
```sh
sudo dnf install python3
```

## 2. Create a Virtual Environment

Run the following command in your project directory:

```sh
python3 -m venv .venv
```

## 3. Activate the Virtual Environment

**Linux/macOS:**
```sh
source .venv/bin/activate
```

**Windows:**
```sh
.\venv\Scripts\activate
```

## 4. Install Dependencies

```sh
pip install -r requirements.txt
```

## 5. Set Up Environment Variables

Before running the project, copy the `.env.template` file to `.env`. This is where you will store your environment-specific settings.

**Linux/macOS:**
```sh
cp .env.template .env
```

**Windows (Command Prompt):**
```cmd
copy .env.template .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.template .env
```

Add your OpenAI API key and any other required secrets to the newly created `.env` file.

> ⚠️ **Warning:** Never add your OpenAI API key or other sensitive information to the `.env.template` file. The `.env.template` is meant only as a reference for required variables and should not contain actual secrets.

## 6. Run in Development Mode

To start the project in development mode, use the following command:

```sh
chainlit run app.py -w
```
