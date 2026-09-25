# 🚀 AutoMail-AI: Cold Application Engine

An automated cold-emailing tool powered by **Google Gemini 2.5 Flash**, **SQLite**, and **Python**. Built for low-overhead, lightweight execution (fully compatible with mobile environments like Android Termux and GitHub Codespaces) to generate personalized internship applications for technical roles.

---

## 📌 Core Features

- **📄 Dynamic Resume Auto-Detection:** Automatically locates and attaches any `.pdf` resume file inside the `assets/` directory (e.g., `Grace.pdf`, `Resume.pdf`).
- **🤖 Dual Generation Modes:**
  - **Static Mode (Default):** Fast, zero-cost execution filling local text templates (`data/template.txt`).
  - **AI Mode (`--use-ai`):** Leverages Google Gemini via `google-genai` to write personalized cold emails tailored to company tech stacks and roles.
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

## 📁 Directory Structure

```text
AutoMail-AI/
├── assets/
│   └── Resume.pdf  # Auto-detected resume attachment (.pdf)
├── data/
│   ├── internships.csv  # Target leads dataset
│   └── template.txt # Cold email template
├── src/
│   ├── database.py   # SQLite database logger
│   ├── llm_client.py  # Google Gemini client
│   └── mailer.py # SMTP email sender & attachment handler
├── .env       # Configuration & Sender Profile
├── .gitignore 
├── main.py             # Main CLI entry point
└── requirements.txt       # Dependencies


🚀 Quickstart Guide
Step 1: Clone & Environment Setup

# Clone the repository
git clone [https://github.com/Coderonaut08spacesci/AutoMail-AI.git](https://github.com/Coderonaut08spacesci/AutoMail-AI.git)
cd AutoMail-AI

# Initialize virtual environment
#python -m venv venv

# Activate virtual environment
# On Linux/Mac/Termux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

2. Install Dependencies

# Install lightweight dependencies
pip install -r requirements.txt

or 

For standard static usage:
pip install python-dotenv

For AI generation support using Gemini:
pip install google-genai


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
1. Interactive Preview Mode (Default / Dry-Run)
Previews generated emails in the console and prompts for interactive approval before sending:
python main.py

2. Gemini AI Mode
Generates customized email content using Google Gemini:
python main.py --use-ai

3. Automated Batch Mode
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

🔐 Security Notice
Never commit your .env file or emails_sent.db to source control.
Use an App Password for Gmail SMTP authentication instead of your account password

