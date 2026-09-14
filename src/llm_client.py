import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

client = genai.Client(api_key=api_key)

def generate_cold_email(hr_name: str, company: str, role: str, tech_stack: str) -> str:
    prompt = f"""
    Write a concise, highly professional cold email (under 150 words) applying for the {role} role at {company}.
    Recipient HR name: {hr_name}.
    Company tech stack: {tech_stack}.

    Context: I am a Computer Science student with strong foundations in software development.
    Mention my enthusiasm for their tech stack and state that my resume is attached.
    Do not include a subject line, preamble, or placeholders—return ONLY the raw email body text.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    
    return response.text.strip()

if __name__ == "__main__":
    test_email = generate_cold_email(
        hr_name="Sarah",
        company="TechCorp",
        role="Software Developer Intern",
        tech_stack="Python, PostgreSQL, Docker"
    )
    print("--- GENERATED TEST EMAIL ---")
    print(test_email)

