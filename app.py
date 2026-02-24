import streamlit as st
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI

matplotlib.use("Agg")

st.set_page_config(
    page_title="TitanicGPT",
    layout="centered"
)

st.title("TitanicGPT Bot")
st.write("Ask questions about the Titanic dataset and I will try to answer.")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if not api_key:
    st.sidebar.warning("API key is needed.")
    
st.sidebar.write("Try asking:")
st.sidebar.write("- What percentage were male?")
st.sidebar.write("- Show me a histogram of passenger ages.")

@st.cache_resource
def get_agent(key: str):
    os.environ["GEMINI_API_KEY"] = key
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    # Path is relative to the root when deployed on Streamlit Cloud
    df = pd.read_csv("data/titanic.csv")
    
    system_prompt = """
    You are an expert data analyst working with the Titanic dataset. 
    You have a pandas DataFrame 'df' containing the data.
    
    1. For text questions, answer clearly.
    2. For chart questions:
       - Write code to create the plot.
       - Save the plot to exactly `temp_plot.png`.
       - Clear the figure.
       - Return exactly: `[IMAGE: temp_plot.png]`
    """
    return create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True, prefix=system_prompt)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_path" in message and message["image_path"]:
            try:
                st.image(message["image_path"])
            except Exception:
                pass

if prompt := st.chat_input("Ask a question about the Titanic dataset..."):
    
    if not api_key:
        st.error("Please provide an API key in the sidebar first.")
        st.stop()
        
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Analyzing data..."):
        try:
            agent = get_agent(api_key)
            result = agent.invoke({"input": prompt})
            output = result.get("output", "")
            
            bot_response = output
            image_path = None
            
            if "[IMAGE:" in output:
                import re
                match = re.search(r'\[IMAGE:\s*(.*?)\]', output)
                if match:
                    image_path = match.group(1).strip()
                    bot_response = "Here is the visualization you requested:"
                    
            with st.chat_message("assistant"):
                st.markdown(bot_response)
                if image_path and os.path.exists(image_path):
                    st.image(image_path)
                        
            st.session_state.messages.append({
                "role": "assistant", 
                "content": bot_response,
                "image_path": image_path if (image_path and os.path.exists(image_path)) else None
            })
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
