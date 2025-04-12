from fastapi import FastAPI, HTTPException
import pandas as pd
from pathlib import Path
import os

app = FastAPI()

# Configuração do caminho do CSV
BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "data" / "dados.csv"

@app.get("/dados")
async def get_dados():
    try:
        # Verifica se o arquivo existe
        if not CSV_PATH.exists():
            raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")
        
        # Lê o arquivo CSV
        df = pd.read_csv(CSV_PATH)
        
        # Verifica se o DataFrame está vazio
        if df.empty:
            raise HTTPException(status_code=404, detail="O arquivo CSV está vazio")
        
        # Converte para dicionário
        dados = df.to_dict(orient="records")
        
        return {"dados": dados}
    
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="O arquivo CSV está mal formatado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")