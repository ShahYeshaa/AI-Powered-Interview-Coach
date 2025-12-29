import streamlit as st
from google import genai
from sentence_transformers import SentenceTransformer, util
import re
import os

def main():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it as an environment variable.")

    
    client = genai.Client(api_key=api_key)
    FILLER_WORDS = ["um", "uh", "like", "you know", "so"]

    if 'embedding_model' not in st.session_state:
        st.session_state.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

    embedding_model = st.session_state.embedding_model

    def extract_keywords(text):
        words = set(re.findall(r'\b\w{4,}\b', text.lower()))
        keywords = words - set(FILLER_WORDS)
        return list(keywords)

    def highlight_keywords(user_ans, keywords):
        highlighted = user_ans
        for kw in keywords:
            highlighted = re.sub(rf"(?i)\b({kw})\b", r"**\1**", highlighted)
        return highlighted

    def semantic_similarity(user_ans, model_ans):
        embeddings = embedding_model.encode([user_ans, model_ans], convert_to_tensor=True)
        sim_score = util.cos_sim(embeddings[0], embeddings[1]).item()
        return round(sim_score*100,2)

    def calculate_final_score(user_ans, model_ans):
        wc = len(user_ans.split())
        fillers = sum(user_ans.lower().count(f) for f in FILLER_WORDS)

        sim = semantic_similarity(user_ans, model_ans)
        score = sim * 0.8  # 80% weight

        if wc > 40:
            score += 5
        if fillers == 0:
            score += 5
        elif fillers <= 2:
            score += 2

        keywords = extract_keywords(model_ans)
        matches = sum(1 for k in keywords if k.lower() in user_ans.lower())
        score += min(10, matches)

        score = max(0, min(100, score))
        return round(score,2), matches, sim, keywords

    # Gemini API Functions
    def generate_questions(role):
        prompt = f"""
        Generate 3 mock interview questions for a {role} role.
        Include introduction, soft skills, and technical questions.
        Provide plain text questions, one per line.
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        questions_text = response.text
        questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
        return questions[:10]

    def get_feedback(answer, question, role):
        prompt = f"""
        Role: {role}
        Question: {question}
        User Answer: {answer}
        Provide concise feedback on strengths, improvements, and suggestions.
        Also provide a perfect model answer after 'Model Answer:'.
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        content = response.text.strip()
        if "Model Answer:" in content:
            feedback, model_ans = content.split("Model Answer:", 1)
        else:
            feedback, model_ans = content, "No model answer provided."
        return feedback.strip(), model_ans.strip()

    # Streamlit App
    st.title("AI-Powered Mock Interview")

    role = st.text_input("Enter the role/domain you want to practice for (e.g., Data Scientist, Web Developer):")

    if role:
        if "questions" not in st.session_state:
            st.session_state.questions = generate_questions(role)
            st.session_state.answers = [""] * len(st.session_state.questions)
            st.session_state.feedbacks = [""] * len(st.session_state.questions)
            st.session_state.model_answers = [""] * len(st.session_state.questions)
            st.session_state.show_answer_flags = [False] * len(st.session_state.questions)
            st.session_state.q_index = 0

        q_index = st.session_state.q_index

        # Answer Input
        if q_index < len(st.session_state.questions):
            question = st.session_state.questions[q_index].lstrip("1234567890. ")
            st.subheader(f"Q{q_index+1}: {question}")
            ans = st.text_area("Your Answer", value=st.session_state.answers[q_index], key=f"ans_{q_index}")

            if st.button("Submit Answer"):
                if ans.strip() == "":
                    st.warning("Answer cannot be blank! Please write something.")
                else:
                    st.session_state.answers[q_index] = ans
                    feedback, model_ans = get_feedback(ans, question, role)
                    st.session_state.feedbacks[q_index] = feedback
                    st.session_state.model_answers[q_index] = model_ans
                    st.session_state.q_index += 1
                    st.rerun()

        # Display All Answers, Feedback & Overall Summary
        else:
            st.success("✅ Interview Finished!")
            total_score = 0
            all_missing_keywords = []

            for i, question in enumerate(st.session_state.questions):
                st.write(f"**Q{i+1}: {question.lstrip('1234567890. ')}**")
                user_ans = st.session_state.answers[i]

                score, matched_keywords, sim, keywords = calculate_final_score(user_ans, st.session_state.model_answers[i])
                highlighted_ans = highlight_keywords(user_ans, keywords)
                total_score += score
                missing = [k for k in keywords if k.lower() not in user_ans.lower()]
                all_missing_keywords.extend(missing)

                st.markdown(f"**Your Answer (keywords highlighted):** {highlighted_ans}")
                st.write(f"**Score:** {score}/100")
                st.write(f"Matched Keywords: {matched_keywords}")
                st.write(f"Semantic Similarity: {sim}%")
                st.write(f"**Feedback:** {st.session_state.feedbacks[i]}")

                key_btn = f"toggle_{i}"
                state_key = f"toggle_state_{i}"
                if state_key not in st.session_state:
                    st.session_state[state_key] = False
                
                if st.button("Show Answer" if not st.session_state[state_key] else "Hide Answer", key=key_btn):
                    st.session_state[state_key] = not st.session_state[state_key]
                
                if st.session_state[state_key]:
                    st.info(f"**Model Answer:** {st.session_state.model_answers[i]}")

            # Overall Performance Summary
            st.markdown("---")
            st.subheader("📊 Overall Performance Summary")
            avg_score = round(total_score / len(st.session_state.questions), 2)
            st.write(f"**Average Score:** {avg_score}/100")
            st.write(f"**Total Questions:** {len(st.session_state.questions)}")

            # Weakest questions
            scores = []
            for i, question in enumerate(st.session_state.questions):
                score, _, _, _ = calculate_final_score(st.session_state.answers[i], st.session_state.model_answers[i])
                scores.append((score, i))
            scores.sort()  # ascending
            weakest = scores[:3]  # 3 lowest
            st.write("**Weakest Questions:**")
            for s, idx in weakest:
                st.write(f"- Q{idx+1}: {st.session_state.questions[idx].lstrip('1234567890. ')} (Score: {s}/100)")

            # Restart
            if st.button("Restart Interview"):
                for key in ["questions","answers","feedbacks","model_answers","show_answer_flags","q_index"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()


