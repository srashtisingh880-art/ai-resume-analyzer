import streamlit as st
from PyPDF2 import PdfReader

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

# ------------------------------
# Custom CSS
# ------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #1E3A8A;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# Skills Database
# ------------------------------
COMMON_SKILLS = [
    "python", "java", "c", "c++", "sql", "html", "css", "javascript",
    "react", "node.js", "machine learning", "data analysis", "excel",
    "power bi", "tableau", "git", "github", "aws", "azure",
    "mongodb", "pandas", "numpy", "tensorflow", "streamlit"
]

# ------------------------------
# Header
# ------------------------------
st.markdown('<div class="main-title">📄 AI Resume Analyzer & Job Matcher</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload your resume and compare it with a job description.</div>', unsafe_allow_html=True)

# ------------------------------
# Inputs
# ------------------------------
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

# ------------------------------
# Analyze Button
# ------------------------------
if st.button("🔍 Analyze Resume"):

    if uploaded_file is None:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please paste a job description.")

    else:
        # Read PDF
        pdf = PdfReader(uploaded_file)
        resume_text = ""

        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text + " "

        # Convert to lowercase
        resume_text_lower = resume_text.lower()
        job_description_lower = job_description.lower()

        # Match Score
        resume_words = set(resume_text_lower.split())
        job_words = set(job_description_lower.split())

        matched_words = resume_words.intersection(job_words)
        score = (len(matched_words) / len(job_words) * 100) if job_words else 0

        # Skill Extraction
        resume_skills = [skill for skill in COMMON_SKILLS if skill in resume_text_lower]
        jd_skills = [skill for skill in COMMON_SKILLS if skill in job_description_lower]

        missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

        # ------------------------------
        # Results
        # ------------------------------
        st.success("Analysis Completed Successfully!")

        st.subheader("📊 Match Score")
        st.progress(min(int(score), 100))
        st.metric("Overall Match", f"{score:.2f}%")

        st.subheader("✅ Skills Found in Resume")
        if resume_skills:
            st.write(", ".join(skill.title() for skill in resume_skills))
        else:
            st.write("No known skills detected.")

        st.subheader("❌ Missing Skills")
        if missing_skills:
            st.write(", ".join(skill.title() for skill in missing_skills))
        else:
            st.write("No missing skills detected. Great job!")

        st.subheader("💡 Suggestions")
        if missing_skills:
            st.info(
                "Consider adding these skills to your resume (if you have them): " +
                ", ".join(skill.title() for skill in missing_skills)
            )
        else:
            st.success("Your resume is well aligned with the job description.")

        with st.expander("📄 View Extracted Resume Text"):
            st.write(resume_text)
