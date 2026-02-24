import os
import uuid
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

def setup_agent(api_key: str):
    os.environ["GEMINI_API_KEY"] = api_key
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
    )

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "titanic.csv")
    df = pd.read_csv(data_path)

    system_prompt = """
    You are an expert data analyst working with the Titanic dataset. 
    You have a pandas DataFrame 'df' containing the data.
    
    Follow these EXTREMELY IMPORTANT rules:
    1. If the user asks a text-based question (e.g., "What percentage...", "How many..."), answer clearly with text.
    2. If the user asks for a chart, graph, visualization, or plot:
       - DO NOT use `plt.show()`.
       - Write pandas/matplotlib/seaborn code to create the plot.
       - Save the plot to exactly `static/temp_plot.png` using `plt.savefig("static/temp_plot.png", bbox_inches="tight")`.
       - Clear the current figure with `plt.clf()` and `plt.close()`.
       - After writing the code, your final response MUST exactly be the string: `[IMAGE: static/temp_plot.png]`. Do not add any conversational text before or after this string.
       
    Be completely precise and execute the user's plan accurately.
    """

    agent = create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=True, 
        allow_dangerous_code=True,
        prefix=system_prompt
    )

    return agent

def process_query(agent, query: str) -> dict:
    """
    Given the initialized agent and a natural language query, run the agent.
    If the agent generates an image, it will return the IMAGE tag.
    Returns a dict with 'response' and/or 'image_url'.
    """
    try:
        # We ensure static directory exists just in case
        os.makedirs("static", exist_ok=True)
        
        result = agent.invoke({"input": query})
        output = result.get("output", "")
        
        if "[IMAGE: " in output:
            unique_filename = f"plot_{uuid.uuid4().hex}.png"
            old_path = "static/temp_plot.png"
            new_path = os.path.join("static", unique_filename)
            
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                return {
                    "response": "Here is the visualization you requested:",
                    "image_url": new_path
                }
            else:
                return {
                    "response": "I tried to generate a plot, but the image file was not created properly. Please try again.",
                    "image_url": None
                }
        
        return {
            "response": output,
            "image_url": None
        }

    except Exception as e:
        return {
            "response": f"An error occurred while processing your request: {str(e)}",
            "image_url": None
        }
