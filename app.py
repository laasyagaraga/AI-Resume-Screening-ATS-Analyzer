import streamlit as st
import PyPDF2
import re

# --------------------------------------
# Page Configuration
# --------------------------------------

st.set_page_config(
    page_title="AI Resume ATS Analyzer",
    page_icon="📄",
    layout="wide"
)

# --------------------------------------
# Skills Database
# --------------------------------------

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

# --------------------------------------
# Title
# --------------------------------------

st.title("📄 AI Resume Screening & ATS Analyzer")

st.write(
    "Upload your resume and compare it with a job description "
    "to analyze skill matching and ATS compatibility."
)

st.divider()

# --------------------------------------
# Resume Upload
# --------------------------------------

st.subheader("📄 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)

# --------------------------------------
# Job Description
# --------------------------------------

st.subheader("📝 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=200,
    placeholder="Paste the complete job description..."
)

# --------------------------------------
# Analyze Button
# --------------------------------------

if st.button("🔍 Analyze Resume", use_container_width=True):

    if uploaded_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:

        # --------------------------------------
        # Extract Resume Text
        # --------------------------------------

        reader = PyPDF2.PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""

        resume_text = resume_text.lower()
        job_description = job_description.lower()

        # --------------------------------------
        # Find Required Skills
        # --------------------------------------

        required_skills = []

        for skill in available_skills:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, job_description):
                required_skills.append(skill)

        # --------------------------------------
        # Match Skills
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
        # Calculate Score
        # --------------------------------------

        total_required = len(required_skills)
        matched_count = len(matched_skills)

        if total_required > 0:
            match_percentage = (
                matched_count / total_required
            ) * 100
        else:
            match_percentage = 0

        ats_score = round(match_percentage)

        # --------------------------------------
        # Recommendation
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
        # Results
        # --------------------------------------

        st.divider()

        st.header("📊 ATS Screening Results")
        
                # --------------------------------------
        # Resume Section Analysis
        # --------------------------------------

        st.subheader("📋 Resume Section Analysis")

        resume_sections = {
            "Education": ["education", "academic background"],
            "Skills": ["skills", "technical skills", "core competencies"],
            "Projects": ["projects", "personal projects", "academic projects"],
            "Experience": ["experience", "work experience", "internship"],
            "Certifications": ["certifications", "certificates"],
            "Summary": ["professional summary", "career objective", "profile summary"]
        }

        present_sections = []
        missing_sections = []

        for section, keywords in resume_sections.items():
            found = any(
                re.search(r"\b" + re.escape(keyword) + r"\b", resume_text)
                for keyword in keywords
            )

            if found:
                present_sections.append(section)
            else:
                missing_sections.append(section)

        total_sections = len(resume_sections)
        completeness = round(
            len(present_sections) / total_sections * 100
        )

        st.metric("Resume Section Coverage", f"{completeness}%")

        st.progress(completeness / 100)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**✅ Sections Detected**")
            for section in present_sections:
                st.write(f"✓ {section}")

        with col2:
            st.markdown("**📝 Sections Not Detected**")
            for section in missing_sections:
                st.write(f"• {section}")

        if missing_sections:
            st.info(
                "Review the sections not detected and add them "
                "if they are relevant to your experience."
            )
        else:
            st.success("All checked resume sections were detected.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "ATS Score",
                f"{ats_score}/100"
            )

        with col2:
            st.metric(
                "Skills Matched",
                f"{matched_count}/{total_required}"
            )

        with col3:
            st.metric(
                "Match Percentage",
                f"{match_percentage:.2f}%"
            )

        st.subheader("🎯 Recommendation")

        if ats_score >= 80:
            st.success(recommendation)
        elif ats_score >= 60:
            st.info(recommendation)
        elif ats_score >= 40:
            st.warning(recommendation)
        else:
            st.error(recommendation)

        # --------------------------------------
        # Skills
        # --------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matched Skills")

            if matched_skills:

                for skill in matched_skills:
                    st.write(f"✓ {skill}")

            else:
                st.write("No matching skills found.")

        with col2:

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:
                    st.write(f"✗ {skill}")

            else:
                st.write("No missing skills!")
        
        # -------------------------------------- 
        #  Skill Gap Analysis & Suggestions 
        # --------------------------------------     
        st.divider()  
        st.header("💡 Personalized Improvement Suggestions")
        
        # --------------------------------------
        # Skill Gap Analysis & Suggestions
        # --------------------------------------

        st.divider()
        st.header("💡 Personalized Improvement Suggestions")

        if missing_skills:
            st.write(
                "Consider developing and demonstrating "
                "experience in these skills:"
            )

            for skill in missing_skills:
                st.info(
                f"📌 **{skill.title()}**: "
                f"Add relevant projects, coursework, "
                f"or practical experience to your resume "
                f"if you have this skill."
                )
        else:
            st.success(
                "All recognized skills in this job "
                "description were found in your resume."
            )


        


        # --------------------------------------
        # Required Skills
        # --------------------------------------

        st.subheader("🔎 Skills Detected in Job Description")

        if required_skills:
            st.write(", ".join(required_skills))
        else:
            st.write("No recognized skills detected.")
        
        # --------------------------------------
        # Downloadable PDF Report
        # --------------------------------------

        from io import BytesIO
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer
        )
        from reportlab.lib.styles import getSampleStyleSheet
        from xml.sax.saxutils import escape

        st.divider()
        st.header("📥 Download ATS Report")

        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        content = []

        content.append(
            Paragraph("AI Resume Screening &amp; ATS Analyzer",
                      styles["Title"])
        )
        content.append(Spacer(1, 20))

        content.append(Paragraph(
            f"ATS Score: {ats_score}/100", styles["Heading2"]
        ))
        content.append(Paragraph(
            f"Match Percentage: {match_percentage:.2f}%",
            styles["Normal"]
        ))
        content.append(Paragraph(
            f"Recommendation: {escape(recommendation)}",
            styles["Normal"]
        ))
        content.append(Spacer(1, 15))

        content.append(Paragraph(
            "Matched Skills", styles["Heading2"]
        ))
        for skill in matched_skills:
            content.append(Paragraph(
                f"- {escape(skill.title())}", styles["Normal"]
            ))

        content.append(Spacer(1, 10))
        content.append(Paragraph(
            "Missing Skills", styles["Heading2"]
        ))
        for skill in missing_skills:
            content.append(Paragraph(
                f"- {escape(skill.title())}", styles["Normal"]
            ))

        content.append(Spacer(1, 10))
        content.append(Paragraph(
            "Improvement Suggestions", styles["Heading2"]
        ))
        for skill in missing_skills:
            content.append(Paragraph(
                f"Develop and demonstrate practical experience "
                f"in {escape(skill.title())}, if applicable.",
                styles["Normal"]
            ))

        pdf.build(content)
    
        # Resume Section Analysis in PDF

        content.append(Spacer(1, 15))
        content.append(Paragraph(
            "Resume Section Analysis", styles["Heading2"]
        ))

        content.append(Paragraph(
            f"Section Coverage: {completeness}%",
            styles["Normal"]
        ))

        content.append(Spacer(1, 8))
        content.append(Paragraph(
            "Sections Detected", styles["Heading3"]
        ))

        for section in present_sections:
            content.append(Paragraph(
                f"- {escape(section)}", styles["Normal"]
            ))

        content.append(Spacer(1, 8))
        content.append(Paragraph(
            "Sections Not Detected", styles["Heading3"]
        ))

        for section in missing_sections:
            content.append(Paragraph(
                f"- {escape(section)}", styles["Normal"]
            ))


        buffer.seek(0)

        st.download_button(
            label="📄 Download ATS Report",
            data=buffer.getvalue(),
            file_name="ATS_Screening_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )

