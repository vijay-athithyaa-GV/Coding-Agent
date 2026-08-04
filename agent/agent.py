from agent.llm_client import get_client, generate_code
from agent.logger import log_attempt
from agent.models import AgentState,AttemptRecord
from sandbox.executor import execute_code

MAX_RETRIES = 5

class Agent:
    def __init__(self,task_id:str,task:str,model:str):
        self.task_id = task_id
        self.task = task
        self.model = model
        self.client = get_client()
        self.messages = [{"role": "user", "content": task}]
        self.history: list[AttemptRecord] = []
        self.state = AgentState.PLAN    

    def run(self)-> AttemptRecord | None:
        for attempt in range(1,MAX_RETRIES+1):
            self.state = AgentState.GENERATE
            generation = generate_code(self.client,self.model,self.messages)

            self.state = AgentState.EXECUTE
            result = execute_code(generation.code)

            self.state = AgentState.EVALUTE
            record = AttemptRecord(
                attempt_number=attempt,
                code=generation.code,
                result=result
            )   
            self.history.append(record)
            log_attempt(self.task_id,record)

            if result.success:
                self.state = AgentState.DONE
                return record

            self.state = AgentState.RETRY
            self.messages.append({"role":"assistant","content":generation.code})
            self.messages.append({
                "role":"user",
                "content":f"Execution failed with exit code {result.exit_code}. Please provide a corrected version of the code."
            })
        return None
    
            