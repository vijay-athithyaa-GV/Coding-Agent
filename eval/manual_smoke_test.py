from dotenv import load_dotenv
from agent.agent import Agent
import os   
load_dotenv()  # Load environment variables from .env file  

TASKS = {
    "reverse_string": "Write a Python function reverse_string(s: str) -> str that returns s reversed. Include a __main__ block with 2 example calls printed.",
    "is_palindrome": "Write a Python function is_palindrome(s: str) -> bool that checks if s reads the same backward. Include a __main__ block with 2 example calls printed.",
    "fizzbuzz": "Write a Python function fizzbuzz(n: int) -> list[str] implementing FizzBuzz from 1 to n. Include a __main__ block that prints fizzbuzz(15).",
}

if __name__ == "__main__":
    model = os.environ["OLLAMA_MODEL"]
    for task_id, task in TASKS.items():
        print(f"\n==={task_id}===")
        agent = Agent(task_id=task_id, task=task, model=model)
        result = agent.run()
        if result:
            print(f"Task {task_id} completed successfully on attempt {result.attempt_number},code executed with code {result.code}.")
        else:
            print(f"Task {task_id} failed after {len(agent.history)} attempts.")