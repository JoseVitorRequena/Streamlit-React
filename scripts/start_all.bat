@echo off
start cmd /k "cd ..\frontend\meu-app-react && npm start"
start cmd /k "cd ..\backend && venv\Scripts\activate && uvicorn main:app --reload"
start cmd /k "cd ..\streamlit && streamlit run app.py"