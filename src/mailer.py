import os
import glob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def find_resume_file() -> str | None:
    """Scans the assets directory and returns the path to the first PDF found."""
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    if not os.path.exists(assets_dir):
        assets_dir = "assets"

    pdfs = glob.glob(os.path.join(assets_dir, "*.pdf"))
    if pdfs:
        return pdfs[0]  # Returns first found PDF (e.g. Grace.pdf)
    return None

def send_email_with_resume(to_email: str, subject: str, body: str, resume_path: str, email_user: str, email_pass: str):
    """Constructs and sends an email with auto-detected PDF attachment."""
    
    # Auto-detect PDF if specified path doesn't exist directly
    if not resume_path or not os.path.exists(resume_path):
        auto_path = find_resume_file()
        if auto_path:
            print(f"📎 Auto-detected resume: {auto_path}")
            resume_path = auto_path
        else:
            print("⚠️ Warning: No PDF found in assets/. Sending without attachment.")
            resume_path = None

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach PDF resume if available
    if resume_path and os.path.exists(resume_path):
        with open(resume_path, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(resume_path)
        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
        msg.attach(part)

    # Dispatch using TLS (port 587) or SSL (port 465)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)
