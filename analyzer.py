import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_job_description(job_text: str):
    prompt = f"""
You are an expert HR and AI Job Analyst.
Analyze the following Job Description and extract structured information. 
You MUST output ONLY a valid JSON object with these exact keys:
- "job_title" (string)
- "required_skills" (array of strings)
- "experience_level" (string: Junior, Mid, Senior, or Not Specified)
- "key_responsibilities" (array of strings)
- "summary" (string: brief 2-sentence overview)

Do NOT include any markdown code blocks, backticks, or extra text. Only raw JSON.

Job Description:
{job_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
    clean_text = raw_text.strip()
    
    return json.loads(clean_text)


if __name__ == "__main__":
    sample_jd = """
    We are looking for a Python Developer with 3+ years of experience in FastAPI and PostgreSQL. 
    Responsibilities include building REST APIs, writing unit tests, and optimizing database queries.
    Must have strong communication skills and experience with Docker.
    """
    
    print("Analyzing sample job description...")
    result = analyze_job_description(sample_jd)
    print(json.dumps(result, indent=2))