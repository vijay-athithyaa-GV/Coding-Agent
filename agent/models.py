from enum import Enum
from pydantic import BaseModel, Field

class AgentState(str, Enum):
    PLAN = "plan"
    GENERATE = "generate"
    EXECUTE = "execute"
    EVALUTE = "evaluate"
    RETRY = "retry"
    DONE = "done"  

class CodeGeneration(BaseModel):
    reasoning:str
    code:str

class ExecutionResult(BaseModel):
    stdout:str
    strerr:str
    exit_code:int
    timed_out:bool
    success:bool

class AttemptRecord(BaseModel):
    attempt_number:int
    code:str
    result:ExecutionResult