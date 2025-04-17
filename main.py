import streamlit as st
from auth import login_page
from post_generator import generate_post
from few_shot import FewShotPosts
from user_data import init_user_data
from llm_helper import llm
import toml  # For reading secrets.toml

# Load credentials from .streamlit/secrets.toml
secrets = toml.load(".streamlit/secrets.toml")
ADMIN_USERNAME=secrets["ADMIN_USERNAME"]


# Initialize user data
init_user_data()

st.set_page_config(page_title="Orien Ai App", page_icon="🤖", layout="wide")

def get_length_str(length): 
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def post_generator():
    st.title("LinkedIn Post Generator")

    fs = FewShotPosts()

    tab1, tab2 = st.tabs(["Generate with Few-Shot Examples", "Generate with Your Own Style"])

    # Tab 1: Based on stored posts
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_tag = st.selectbox("Title", options=fs.get_tags(), key="fewshot_tag")
        with col2:
            selected_length = st.selectbox("Length", options=["Short", "Medium", "Long"], key="fewshot_length")
        with col3:
            selected_language = st.selectbox("Language", options=["English", "Hinglish"], key="fewshot_language")

        if st.button("Generate Post (Few-Shot)", key="fewshot_btn"):
            post = generate_post(selected_length, selected_language, selected_tag)
            st.subheader("Generated Post:")
            st.write(post)

    # Tab 2: Based on user-provided writing style
    with tab2:
        user_text = st.text_area("✍️ Paste your writing style (example post)", height=200)
        user_topic = st.text_input("🏷️ Enter the topic or tag for the new post")
        user_language = st.selectbox("🗣️ Language", options=["English", "Hinglish"], key="custom_lang")
        user_length = st.selectbox("📏 Length", options=["Short", "Medium", "Long"], key="custom_len")

        if st.button("Generate Post (Your Style)", key="custom_btn"):
            if not user_text or not user_topic:
                st.warning("Please provide both writing style and topic.")
            else:
                prompt = f'''
Generate a LinkedIn post using the following information. No preamble.

1) Topic: {user_topic}
2) Length: {get_length_str(user_length)}
3) Language: {user_language}
4) Mimic the writing style of the following text (use tone , style):

"{user_text}"
'''
                response = llm.invoke(prompt)
                st.subheader("Generated Post:")
                st.write(response.content)

# Authentication check
if "authenticated" in st.session_state and st.session_state["authenticated"]:
    if st.session_state.get("username") == ADMIN_USERNAME:
        login_page()
    else:
        post_generator()
else:
    login_page()
