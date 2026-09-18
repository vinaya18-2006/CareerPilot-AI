import re
from pypdf import PdfReader


# ==========================================
# EXTRACT TEXT FROM PDF
# ==========================================

def extract_text_from_pdf(file):
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ==========================================
# FIND SKILLS
# ==========================================

def extract_skills(text):

    skills_database = [
        "Python",
        "Java",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "AWS",
        "Azure",
        "Docker",
        "Kubernetes",
        "Git",
        "Linux",
        "Power BI",
        "Tableau",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "FastAPI",
        "Django",
        "Flask",
        "Spark",
        "ETL"
    ]

    text_lower = text.lower()

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text_lower:
            found_skills.append(skill)

    return sorted(set(found_skills))


# ==========================================
# FIND EDUCATION
# ==========================================

def extract_education(text):

    education_keywords = [
        "B.E",
        "B.Tech",
        "Bachelor",
        "B.Sc",
        "M.E",
        "M.Tech",
        "M.Sc",
        "Master"
    ]

    found = []

    for keyword in education_keywords:

        if keyword.lower() in text.lower():
            found.append(keyword)

    return sorted(set(found))


# ==========================================
# FIND EMAIL
# ==========================================

def extract_email(text):

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return ""


# ==========================================
# FIND PHONE
# ==========================================

def extract_phone(text):

    pattern = r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return ""


# ==========================================
# COMPLETE RESUME ANALYSIS
# ==========================================

def analyze_resume(file):

    text = extract_text_from_pdf(file)

    profile = {

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text),

        "education": extract_education(text),

        "raw_text": text
    }

    return profile