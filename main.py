import os
import sys
import time
import argparse
import csv
from dotenv import load_dotenv, set_key

ENV_PATH = ".env"
load_dotenv(ENV_PATH)

try:
    from src.llm_client import generate_cold_email
except ImportError:
    generate_cold_email = None

from src.database import init_db, is_email_sent, log_sent_email
from src.mailer import send_email_with_resume

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RESUME_PATH = os.path.join("assets", "resume.pdf")
CSV_PATH = os.path.join("data", "internships.csv")
TEMPLATE_PATH = os.path.join("data", "template.txt")

def get_or_prompt_sender_profile():
    profile_keys = {
        "SENDER_NAME": "Enter your full name",
        "SENDER_COLLEGE": "Enter your college name",
        "SENDER_PHONE": "Enter your phone number",
        "SENDER_GITHUB": "Enter your GitHub profile URL",
#        "SENDER_LINKEDIN": "Enter your #LinkedIn profile URL"
    }
    profile = {}
    env_updated = False
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, 'w').close()
    print("👤 Checking Sender Profile Configuration...")
    for key, prompt_msg in profile_keys.items():
        value = os.getenv(key)
        if not value:
            value = input(f"👉 {prompt_msg}: ").strip()
            set_key(ENV_PATH, key, value)
            env_updated = True
        profile[key] = value
    if env_updated:
        print("✅ Sender profile saved to.env file!\n")
    else:
        print(f"✅ Loaded profile for: {profile.get('SENDER_NAME','Unknown')}\n")
    return profile

def parse_args():
    parser = argparse.ArgumentParser(description="Automated Cold Email Engine")
    parser.add_argument("--send", action="store_true", help="Live send")
    parser.add_argument("--use-ai", action="store_true", help="Use Gemini")
    return parser.parse_args()

def load_template(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Template file not found at {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def fill_template(template_str: str, hr_name: str, company: str, tech_stack: str, profile: dict, email_user: str) -> str:
    greeting_name = hr_name if hr_name and hr_name.lower()!= "nan" and hr_name!= "" else "Hiring Team"
    filled = template_str.replace("{{hr_name}}", greeting_name)
    filled = filled.replace("{{company}}", company)
    filled = filled.replace("{{tech_stack}}", tech_stack)
    filled = filled.replace("{{sender_name}}", profile.get("SENDER_NAME", ""))
    filled = filled.replace("{{sender_college}}", profile.get("SENDER_COLLEGE", ""))
    filled = filled.replace("{{sender_phone}}", profile.get("SENDER_PHONE", ""))
    filled = filled.replace("{{sender_github}}", profile.get("SENDER_GITHUB", ""))
#    filled = #filled.replace("{{sender_linkedin}}", #profile.get("SENDER_LINKEDIN", ""))
    filled = filled.replace("{{sender_email}}", email_user or "")
    return filled

def main():
    args = parse_args()
    dry_run = not args.send
    use_ai = args.use_ai
    profile = get_or_prompt_sender_profile()
    init_db()
    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: Lead dataset not found at '{CSV_PATH}'.")
        sys.exit(1)
    leads = []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    total_leads = len(leads)
    print(f"📋 Loaded {total_leads} lead(s) from {CSV_PATH}.")
    print(f"⚙️ Mode: {'Gemini AI' if use_ai else 'Static Template (NO API CALL)'}\n")
    raw_template = ""
    if not use_ai:
        try:
            raw_template = load_template(TEMPLATE_PATH)
        except Exception as e:
            print(f"❌ Template Error: {e}")
            sys.exit(1)
    for index, row in enumerate(leads):
        email = str(row.get('email', '')).strip()
        hr_name = str(row.get('hr_name', '')).strip()
        company = str(row.get('company', '')).strip()
        role = str(row.get('role', '')).strip()
        tech_stack = str(row.get('tech_stack', '')).strip()
        print(f"[{index + 1}/{total_leads}] Processing: {company} ({email})")
        if is_email_sent(email):
            print(f"⏭️ Skipping {email} — already sent.\n")
            continue
        if use_ai:
            if generate_cold_email is None:
                print("❌ google-genai not installed. Install or run without --use-ai")
                sys.exit(1)
            print("🧠 Requesting Gemini...")
            try:
                body = generate_cold_email(hr_name, company, role, tech_stack)
            except Exception as e:
                print(f"⚠️ Failed: {e}\n")
                continue
        else:
            print("📄 Filling template...")
            body = fill_template(raw_template, hr_name, company, tech_stack, profile, EMAIL_USER)
        subject = f"Application for {role} | S.Y.B.Sc. CS Student - {profile['SENDER_NAME']}"
        print("\n" + "="*60)
        print(f"TO: {email}")
        print(f"SUBJECT: {subject}")
        print("-" * 60)
        print(body)
        print("="*60 + "\n")
        should_send = False
        if dry_run:
            user_choice = input(f"Send email to {company}? [y/n/quit]: ").strip().lower()
            if user_choice == 'y':
                should_send = True
            elif user_choice == 'quit':
                break
            else:
                print("Skipped.\n")
                continue
        else:
            should_send = True
        if should_send:
            try:
                print(f"🚀 Sending to {email}...")
                send_email_with_resume(email, subject, body, RESUME_PATH, EMAIL_USER, EMAIL_PASS)
                log_sent_email(email, company, role)
                print(f"✅ Logged for {company}.\n")
                time.sleep(3)
            except Exception as e:
                print(f"❌ Failed to send: {e}\n")

if __name__ == "__main__":
    main()


#version 1.0
"""
import os
import sys
import time
import argparse
import csv
from dotenv import load_dotenv, set_key

# Path setup
ENV_PATH = ".env"
load_dotenv(ENV_PATH)

from src.llm_client import generate_cold_email
from src.database import init_db, is_email_sent, log_sent_email
from src.mailer import send_email_with_resume

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RESUME_PATH = os.path.join("assets", "resume.pdf")
CSV_PATH = os.path.join("data", "internships.csv")
TEMPLATE_PATH = os.path.join("data", "template.txt")

def get_or_prompt_sender_profile():
    ""Retrieves sender profile from .env or interactively prompts the user on first run.""
    profile_keys = {
        "SENDER_NAME": "Enter your full name",
        "SENDER_COLLEGE": "Enter your college name",
        "SENDER_PHONE": "Enter your phone number",
        "SENDER_GITHUB": "Enter your GitHub profile URL",
#        "SENDER_LINKEDIN": "Enter your #LinkedIn profile URL"
    }
    
    profile = {}
    env_updated = False
    
    # Ensure .env file exists
    if not os.path.exists(ENV_PATH):
        open(ENV_PATH, 'w').close()

    print("👤 Checking Sender Profile Configuration...")
    for key, prompt_msg in profile_keys.items():
        value = os.getenv(key)
        if not value:
            value = input(f"👉 {prompt_msg}: ").strip()
            set_key(ENV_PATH, key, value)
            env_updated = True
        profile[key] = value

    if env_updated:
        print("✅ Sender profile saved to .env file!\n")
    else:
        print(f"✅ Loaded profile for: {profile['SENDER_NAME']}\n")

    return profile

def parse_args():
    parser = argparse.ArgumentParser(
        description="Automated Cold Email Application Engine"
    )
    parser.add_argument(
        "--send", 
        action="store_true", 
        help="Run in automated live mode without interactive prompts"
    )
    parser.add_argument(
        "--use-ai", 
        action="store_true", 
        help="Use Gemini API to generate custom emails instead of static template"
    )
    return parser.parse_args()

def load_template(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Template file not found at {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def fill_template(template_str: str, hr_name: str, company: str, tech_stack: str, profile: dict, email_user: str) -> str:
    greeting_name = hr_name if hr_name and hr_name.lower() != "nan" else "Hiring Team"
    
    # Recipient Replacements
    filled = template_str.replace("{{hr_name}}", greeting_name)
    filled = filled.replace("{{company}}", company)
    filled = filled.replace("{{tech_stack}}", tech_stack)
    
    # Sender Profile Replacements
    filled = filled.replace("{{sender_name}}", profile.get("SENDER_NAME", ""))
    filled = filled.replace("{{sender_college}}", profile.get("SENDER_COLLEGE", ""))
    filled = filled.replace("{{sender_phone}}", profile.get("SENDER_PHONE", ""))
    filled = filled.replace("{{sender_github}}", profile.get("SENDER_GITHUB", ""))
    filled = filled.replace("{{sender_linkedin}}", profile.get("SENDER_LINKEDIN", ""))
    filled = filled.replace("{{sender_email}}", email_user or "")
    
    return filled

def main():
    args = parse_args()
    dry_run = not args.send
    use_ai = args.use_ai
    
    # Get or prompt user profile setup
    profile = get_or_prompt_sender_profile()
    
    # 1. Initialize SQLite DB
    init_db()
    
    # 2. Check credentials for live mode
    if not dry_run and (not EMAIL_USER or not EMAIL_PASS):
        print("❌ Error: EMAIL_USER and EMAIL_PASS must be set in .env to send emails.")
        sys.exit(1)
        
    # 3. Load dataset
    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: Lead dataset not found at '{CSV_PATH}'.")
        sys.exit(1)
        
    leads = []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
            
    total_leads = len(leads)
    print(f"📋 Loaded {total_leads} target lead(s) from {CSV_PATH}.")
    print(f"⚙️ Mode: {'Gemini AI' if use_ai else 'Static Template'}\n")

    raw_template = ""
    if not use_ai:
        try:
            raw_template = load_template(TEMPLATE_PATH)
        except Exception as e:
            print(f"❌ Template Error: {e}")
            sys.exit(1)

    # 4. Iterate over dataset
    for index, row in enumerate(leads):
        email = str(row.get('email', '')).strip()
        hr_name = str(row.get('hr_name', '')).strip()
        company = str(row.get('company', '')).strip()
        role = str(row.get('role', '')).strip()
        tech_stack = str(row.get('tech_stack', '')).strip()
        
        print(f"[{index + 1}/{total_leads}] Processing: {company} ({email})")
        
        if is_email_sent(email):
            print(f"⏭️ Skipping {email} — already recorded in database.\n")
            continue
            
        if use_ai:
            print("🧠 Requesting customized email from Gemini...")
            try:
                body = generate_cold_email(hr_name, company, role, tech_stack)
            except Exception as e:
                print(f"⚠️ Failed to generate email content for {company}: {e}\n")
                continue
        else:
            print("📄 Filling email template...")
            body = fill_template(raw_template, hr_name, company, tech_stack, profile, EMAIL_USER)
            
        subject = f"Application for {role} | S.Y.B.Sc. CS Student - {profile['SENDER_NAME']}"
        
        # Terminal Preview
        print("\n" + "="*60)
        print(f"TO: {email}")
        print(f"SUBJECT: {subject}")
        print("-" * 60)
        print(body)
        print("="*60 + "\n")
        
        # Interactive Approval
        should_send = False
        if dry_run:
            user_choice = input(f"Send email to {company}? [y/n/quit]: ").strip().lower()
            if user_choice == 'y':
                should_send = True
            elif user_choice == 'quit':
                print("Exiting pipeline.")
                break
            else:
                print("Skipped.")
                continue
        else:
            should_send = True

        if should_send:
            try:
                print(f"🚀 Sending email to {email}...")
                send_email_with_resume(
                    to_email=email,
                    subject=subject,
                    body=body,
                    resume_path=RESUME_PATH,
                    email_user=EMAIL_USER,
                    email_pass=EMAIL_PASS
                )
                
                log_sent_email(email, company, role)
                print(f"✅ Application logged for {company}.\n")
                
                time.sleep(5)
            except Exception as e:
                print(f"❌ Failed to send email to {email}: {e}\n")

if __name__ == "__main__":
    main()
"""
