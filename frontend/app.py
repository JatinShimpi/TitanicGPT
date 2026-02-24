import streamlit as st
import requests
import os

st.set_page_config(
    page_title="TitanicGPT",
    layout="centered"
)

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.title("TitanicGPT Bot")
st.write("Ask questions about the Titanic dataset and I will try to answer.")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if not api_key:
    st.sidebar.warning("API key is needed.")
    
st.sidebar.write("Try asking:")
st.sidebar.write("- What percentage were male?")
st.sidebar.write("- Show me a histogram of passenger ages.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_url" in message and message["image_url"]:
            full_img_url = f"{API_URL}/{message['image_url']}"
            st.image(full_img_url)

if prompt := st.chat_input("Ask a question about the Titanic dataset..."):
    
    if not api_key:
        st.error("Please provide an API key in the sidebar first.")
        st.stop()
        
    st.chat_message("user").markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Analyzing data..."):
        try:
            response = requests.post(
                f"{API_URL}/api/chat",
                json={
                    "query": prompt,
                    "api_key": api_key
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("response", "No response text.")
                image_url = data.get("image_url")
                
                with st.chat_message("assistant"):
                    st.markdown(bot_response)
                    if image_url:
                        full_img_url = f"{API_URL}/{image_url}"
                        st.image(full_img_url)
                        
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": bot_response,
                    "image_url": image_url
                })
                
            else:
                error_msg = f"Error: {response.json().get('detail', 'Unknown error')}"
                st.error(error_msg)
                
        except requests.exceptions.ConnectionError:
            st.error("Failed to connect to the backend server. Is FastAPI running?")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
