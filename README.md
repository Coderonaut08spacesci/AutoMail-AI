# 🚀 AutoMail-AI: Cold Application Engine

An automated cold-emailing tool powered by **Google Gemini 2.5 Flash**, **SQLite**, and **Python**. Built for low-overhead, lightweight execution (fully compatible with mobile environments like Android Termux and GitHub Codespaces) to generate personalized internship applications for technical roles.

---

## 📌 Core Features

- **AI Personalization:** Leverages the official `google-genai` SDK to draft tailored cover letter bodies based on target company tech stacks and contact names.
- **Zero-Dependency Data Engine:** Uses Python's native `csv` module for fast parsing without native C-compilation overhead (no `pandas` or `numpy` build bloat).
- **Duplicate Prevention:** SQLite relational database tracks sent applications to ensure contacts are never emailed twice.
- **MIME Resume Attachment:** Automatically encodes and attaches PDF resumes to outgoing emails.
- **Interactive Dry-Run Mode:** Displays email previews in the terminal with user approval prompts before dispatching.
- **Docker Ready:** Includes a lightweight `Dockerfile` for containerized cloud deployment.

---

## 🛠️ Architecture & Tech Stack

- **Language:** Python 3.10+
- **AI Model:** Google Gemini 2.5 Flash (`google-genai`)
- **Database:** SQLite3 (`sqlite3`)
- **Mail Transport:** SMTP with TLS (`smtplib`, `email.mime`)
- **Configuration:** `python-dotenv`

---

## 📂 Project Structure

```text
auto-internship-apply/
├── .env.example           # Environment variables blueprint
├── .gitignore             # Git ignore file for secrets and virtualenvs
├── Dockerfile             # Container configuration blueprint
├── README.md              # Project documentation
├── main.py                # Main CLI application runner
├── requirements.txt       # Lightweight Python dependencies
├── data/
│   ├── internships.csv    # Target company lead sheet
│   └── applications.db    # SQLite tracking database (auto-generated)
├── src/
│   ├── __init__.py        # Python package marker
│   ├── database.py        # SQLite storage and duplicate checking
│   ├── llm_client.py     # Gemini API integration wrapper
│   └── mailer.py          # SMTP mail transmission & PDF attachment
└── assets/
    └── resume.pdf         # Attached resume file

🚀 Quickstart Guide
Step 1: Clone & Environment Setup

# Clone the repository
git clone [https://github.com/YOUR_USERNAME/auto-internship-apply.git](https://github.com/YOUR_USERNAME/auto-internship-apply.git)
cd auto-internship-apply

# Initialize virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac/Termux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install lightweight dependencies
pip install -r requirements.txt

Step 2: Configure Environment Variables
Copy .env.example to .env and fill in your details:
cp .env.example .env

Open .env and add your keys:
GEMINI_API_KEY: Obtain from Google AI Studio.
EMAIL_USER: Your Gmail address.
EMAIL_PASS: Your 16-character Gmail App Password.

Step 3: Add Your Leads & Resume
1. Populate data/internships.csv with your target companies:
email,hr_name,company,role,tech_stack
hr@example.com,Sarah,TechCorp,Backend Developer Intern,Python and PostgreSQL
            
2. Place your resume PDF at assets/resume.pdf

💻 Usage
Interactive Preview Mode (Default / Dry-Run)
Previews generated emails in the console and prompts for interactive approval before sending:
python main.py

Automated Batch Mode
Runs continuously without interactive approval prompts:
python main.py --send

🗄️ Database & Duplicate Mitigation
Every sent application is automatically logged in data/applications.db. On each run, main.py checks SQLite before invoking Gemini or sending an email. If an email address already exists in the database, it is automatically skipped.
To inspect recorded applications manually:
sqlite3 data/applications.db "SELECT * FROM sent_emails;"

🐳 Running with Docker
Build and execute the project inside an isolated container:
# Build Docker image
docker build -t automail-ai .

# Run container with environment file
docker run -it --env-file .env automail-ai

