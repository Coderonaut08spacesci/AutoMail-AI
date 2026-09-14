import os
import sys
import time
import argparse
import csv
from dotenv import load_dotenv

from src.llm_client import generate_cold_email
from src.database import init_db, is_email_sent, log_sent_email
from src.mailer import send_email_with_resume

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RESUME_PATH = os.path.join("assets", "resume.pdf")
CSV_PATH = os.path.join("data", "internships.csv")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Automated Cold Email Application Engine"
    )
    parser.add_argument(
        "--send", 
        action="store_true", 
        help="Run in automated live mode without interactive prompts"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    dry_run = not args.send
    
    # 1. Initialize Database
    init_db()
    
    # 2. Check credentials for live mode
    if not dry_run and (not EMAIL_USER or not EMAIL_PASS):
        print("❌ Error: EMAIL_USER and EMAIL_PASS must be set in .env to send emails.")
        sys.exit(1)
        
    # 3. Load dataset using built-in CSV module
    if not os.path.exists(CSV_PATH):
        print(f"❌ Error: Lead dataset not found at '{CSV_PATH}'.")
        sys.exit(1)
        
    leads = []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
            
    total_leads = len(leads)
    print(f"📋 Loaded {total_leads} target lead(s) from {CSV_PATH}.\n")

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
            
        print("🧠 Requesting customized email from Gemini...")
        try:
            body = generate_cold_email(hr_name, company, role, tech_stack)
        except Exception as e:
            print(f"⚠️ Failed to generate email content for {company}: {e}\n")
            continue
            
        subject = f"Application for {role} - {company}"
        
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
    