# AI Resume Screening & ATS Analyzer
# Author: Laasya Garaga

import re
import PyPDF2

available_skills = [
    "python",
    "java",
    "c",
    "c++",
    "html",
    "css",
    "javascript",
    "react",
    "django",
    "flask",
    "mysql",
    "sql",
    "mongodb",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "nlp",
    "rest api",
    "aws",
    "docker"
]

print("======================================")
print("     AI RESUME SCREENING SYSTEM")
print("======================================\n")

# --------------------------------------
# STEP 1: Read Resume PDF
# --------------------------------------

pdf_path = "test_resume.pdf"

print("Reading resume PDF...\n")

try:
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""

except FileNotFoundError:
    print("ERROR: Resume PDF not found!")
    print("Make sure test_resume.pdf is in the same folder.")
    exit()

resume_text = resume_text.lower()

print("Resume extracted successfully!")

# --------------------------------------
# STEP 2: Enter Job Description
# --------------------------------------

print("\n--------------------------------------")
print("Paste the JOB DESCRIPTION below.")
print("When finished, press Ctrl+Z and Enter.")
print("--------------------------------------\n")

job_lines = []

while True:
    try:
        line = input()
        job_lines.append(line)
    except EOFError:
        break

job_description = " ".join(job_lines).lower()

# --------------------------------------
# STEP 3: Find Required Skills
# --------------------------------------

required_skills = []

for skill in available_skills:

    pattern = r"\b" + re.escape(skill) + r"\b"

    if re.search(pattern, job_description):
        required_skills.append(skill)

# --------------------------------------
# STEP 4: Match Resume Skills
# --------------------------------------

matched_skills = []
missing_skills = []

for skill in required_skills:

    pattern = r"\b" + re.escape(skill) + r"\b"

    if re.search(pattern, resume_text):
        matched_skills.append(skill)
    else:
        missing_skills.append(skill)

# --------------------------------------
# STEP 5: Calculate ATS Score
# --------------------------------------

total_required = len(required_skills)
matched_count = len(matched_skills)

if total_required > 0:
    match_percentage = (matched_count / total_required) * 100
else:
    match_percentage = 0

ats_score = round(match_percentage)

# --------------------------------------
# STEP 6: Recommendation
# --------------------------------------

if ats_score >= 80:
    recommendation = "Strong Match"

elif ats_score >= 60:
    recommendation = "Good Match"

elif ats_score >= 40:
    recommendation = "Needs Improvement"

else:
    recommendation = "Low Match"

# --------------------------------------
# STEP 7: Display Results
# --------------------------------------

print("\n======================================")
print("          ATS SCREENING RESULT")
print("======================================")

print("\nRequired Skills from Job Description:")

if required_skills:
    for skill in required_skills:
        print("  •", skill)
else:
    print("  No recognized skills found.")

print("\nMatched Skills:")

if matched_skills:
    for skill in matched_skills:
        print("  ✓", skill)
else:
    print("  None")

print("\nMissing Skills:")

if missing_skills:
    for skill in missing_skills:
        print("  ✗", skill)
else:
    print("  None")

print("\n--------------------------------------")

print("Skill Match Percentage:",
      round(match_percentage, 2), "%")

print("ATS Score:", ats_score, "/ 100")

print("Recommendation:", recommendation)

print("======================================")