from pathlib import Path

from agent.models import AttemptRecord

def log_attempt(task_id:str, record:AttemptRecord)-> None:
    log_path = Path("logs")/f"{task_id}.jsonl"
    with log_path.open("a") as f:
        f.write(record.model_dump_json() + "\n")

    