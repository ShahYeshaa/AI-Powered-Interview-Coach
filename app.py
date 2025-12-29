import streamlit as st
import pdfplumber
import docx
from skill_extractor import extract_skills
from generative_mock_test import main as mock_interview_main

st.title("AI Interview Coach")
st.write("Welcome! This will be your smart interview preparation tool.")


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Resume + JD Analysis", "Mock Interview"])

if page == "Resume + JD Analysis":

    def read_pdf(file):
        """Extract text from a PDF file."""
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def read_docx(file):
        """Extract text from a DOCX file."""
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    def process_resume(uploaded_file):
        """Read resume based on file type and extract text."""
        if uploaded_file.type == "application/pdf":
            return read_pdf(uploaded_file)
        elif uploaded_file.type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            return read_docx(uploaded_file)
        else:
            return None
        
    def process_file(uploaded_file):
        """Read file based on type (PDF/DOCX/TXT)."""
        if uploaded_file.type == "application/pdf":
            return read_pdf(uploaded_file)
        elif uploaded_file.type in [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]:
            return read_docx(uploaded_file)
        elif uploaded_file.type == "text/plain":
            return uploaded_file.read().decode("utf-8")
        else:
            return None
        
    # Variable Initialization
    resume_text = ""
    resume_skills = []
    job_description_text = ""
    jd_skills = []

    # Resume Upload
    uploaded_file = st.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf", "docx"])

    if uploaded_file:
        # Extract text
        resume_text = process_resume(uploaded_file)

        if resume_text:
            st.subheader("📄 Resume Text (Preview)")
            st.text_area("Extracted Text", resume_text + "...", height=200)

            # Extract skills
            # found_skills = extract_skills(resume_text)
            resume_skills = extract_skills(resume_text)

            st.subheader("✅ Extracted Skills")
            if resume_skills:
                st.success(", ".join(resume_skills))
            else:
                st.warning("No skills detected. Try refining your resume.")

        else:
            st.error("Unsupported file format. Please upload PDF or DOCX only.")


    # Job Description Upload
    st.subheader("📌 Upload Job Description")


    jd_input_method = st.radio(
        "How would you like to provide the Job Description?",
        ("Upload a file", "Paste text")
    )

    if jd_input_method == "Upload a file":
        jd_file = st.file_uploader("Upload JD (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], key="jd")
        if jd_file:
            job_description_text = process_file(jd_file)
            if job_description_text:
                st.subheader("📄 Job Description Text (Preview)")
                st.text_area("Extracted JD", job_description_text, height=200)
                jd_skills = extract_skills(job_description_text)

    elif jd_input_method == "Paste text":
        job_description_text = st.text_area("Paste the Job Description here", height=200)
        jd_skills = extract_skills(job_description_text)


    if resume_text and job_description_text:
        st.subheader("📊 Skill Gap Analysis")
        st.write("✅ Skills you already have:", resume_skills)
        st.write("📌 Skills required in JD:", jd_skills)

        missing_skills = set(jd_skills) - set(resume_skills)
        if missing_skills:
            st.error("❌ Missing skills: " + ", ".join(missing_skills))
        else:
            st.success("🎉 Great! No missing skills found.")
        
    if jd_skills and resume_skills:
            match_percentage = (len(set(jd_skills) & set(resume_skills)) / len(set(jd_skills))) * 100
            st.subheader("📈 Match Percentage")
            st.progress(int(match_percentage))
            st.info(f"Your resume matches **{match_percentage:.2f}%** of the required skills.")
else:
    mock_interview_main()
