# Deploying to Streamlit Community Cloud

Since you want to deploy directly to **Streamlit Community Cloud**, you do **not** need Docker or the FastAPI backend. Streamlit Cloud can run the entire application natively! 

We have refactored the app into a single file at the root: `streamlit_app.py`.

## Step-by-Step Deployment Guide

1. **Push your code to GitHub**
   Streamlit Cloud deploys directly from a public (or private) GitHub repository. 
   - Initialize git in this folder: `git init`
   - Add files: `git add streamlit_app.py requirements.txt data/titanic.csv`
   - Commit: `git commit -m "init titanic bot"`
   - Create a repository on GitHub and push these files to it.

2. **Log into Streamlit Community Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with your GitHub account.

3. **Deploy the App**
   - Click **New app** -> **Deploy a public app from GitHub**.
   - **Repository:** Select the repository you just created.
   - **Branch:** `main` (or `master`)
   - **Main file path:** `streamlit_app.py`
   - Click **Deploy!**

4. **Wait for Build**
   Streamlit's servers will automatically read your `requirements.txt`, install LangChain, Pandas, and the other dependencies, and then boot up your application. This usually takes about 1-2 minutes the first time.

5. **Share!**
   Once it's running, you'll have a public `https://your-app-name.streamlit.app` URL that you can share on your portfolio or with your friends! Just make sure to drop in your Gemini API key in the sidebar when you want to use it.
