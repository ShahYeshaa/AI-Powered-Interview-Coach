# 🤖 AI-Powered Interview Coach

An end-to-end AI-based interview preparation platform that helps candidates evaluate their resume, identify skill gaps, and practice interviews with real-time AI-driven feedback.

---

## 🚀 Project Overview

The **AI-Powered Interview Coach** is designed to simulate real interview scenarios by combining NLP, Machine Learning, and Generative AI.  
It assists users in aligning their resumes with job descriptions and improving interview performance through intelligent feedback.

---

## ✨ Key Features

### 🔍 Resume & Job Description Analysis
- Upload resume (PDF/DOCX) and target Job Description
- Automatic skill extraction using NLP
- Identification of missing and matching skills
- Match percentage calculation for role suitability

### 🎤 AI Mock Interview Module
- Role/domain-based question generation
- Covers:
  - Introductory questions
  - Soft skills
  - Technical concepts
- Real-time evaluation of responses
- Model answers and summarized feedback

---

## 🧠 Technical Challenges Solved

- **Resume Parsing**: Handled multiple resume layouts and formats
- **Skill Variations**: Managed fuzzy matching and skill aliases
- **Streamlit State Management**: Maintained multi-step interview flow
- **Generative AI Integration**: Seamless interaction with Gemini API

---

## 🛠 Tech Stack

- **Programming Language**: Python
- **Framework**: Streamlit
- **Machine Learning / NLP**:
  - Transformers
  - Named Entity Recognition (NER)
- **Generative AI**: Gemini API
- **Libraries**:
  - pandas, numpy
  - scikit-learn
  - pdfplumber, python-docx

---

## ⚙️ How to Run the Project

### 1️⃣ Create Virtual Environment
In anaconda prompt run : 
- conda create -n interview_coach python=3.10
- conda activate interview_coach
- pip install -r requirements.txt
- set GEMINI_API_KEY=your_api_key_here
- streamlit run app.py
