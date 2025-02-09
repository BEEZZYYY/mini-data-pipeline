from fastapi import FastAPI, HTTPException
from utils.db import get_db_connection
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Mini Data Pipeline API")

class LogEntry(BaseModel):
    id: int
    content: str
    created_at: str

@app.get("/logs", response_model=List[LogEntry])
def get_logs():
    """
    Получает список логов из базы данных.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, content, created_at FROM logs ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении логов: {e}")
    
    # Преобразуем к списку словарей
    logs = [{"id": row[0], "content": row[1], "created_at": str(row[2])} for row in rows]
    return logs

@app.get("/stats")
def get_stats():
    """
    Предоставляет статистику по логам (например, общее количество записей).
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM logs")
        total = cur.fetchone()[0]
        cur.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении статистики: {e}")
    return {"total_logs": total}

# Для запуска API-сервера выполните команду:
# uvicorn api.main:app --reload
