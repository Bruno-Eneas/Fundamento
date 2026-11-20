import json,os,sqlite3,uuid
from datetime import datetime,timezone
from pathlib import Path

def connect():
    url=os.environ.get('DATABASE_URL','')
    if url:
        import psycopg
        return psycopg.connect(url), '%s'
    path=Path(os.environ.get('FUNDAMENTO_DB',str(Path(__file__).resolve().parents[1]/'runtime/feedback.sqlite')))
    path.parent.mkdir(parents=True,exist_ok=True)
    return sqlite3.connect(path), '?'

def save_feedback(result,rating,comment):
    if rating not in ['Concordo','Discordo','Não consigo avaliar']:
        raise ValueError('Avaliação inválida.')
    if len(comment)>500: raise ValueError('Comentário excede 500 caracteres.')
    conn,p=connect();rid=str(uuid.uuid4())
    try:
        with conn:
            conn.execute('CREATE TABLE IF NOT EXISTS feedback (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, payload TEXT NOT NULL, rating TEXT NOT NULL, comment TEXT NOT NULL)')
            conn.execute(f'INSERT INTO feedback VALUES ({p},{p},{p},{p},{p})',(rid,datetime.now(timezone.utc).isoformat(),json.dumps(result,ensure_ascii=False),rating,comment))
    finally:conn.close()
    return rid
