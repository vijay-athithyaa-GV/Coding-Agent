import subprocess
import tempfile
from pathlib import Path

from agent.models import ExecutionResult

TIMEOUT_SECONDS = 10
def execute_code(code: str) -> ExecutionResult:
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp_file:
        temp_file.write(code)
        script_path = Path(temp_file.name)

    try:
        result = subprocess.run(
            ["python", str(script_path)],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS
        )
        return ExecutionResult(
            stdout=result.stdout,
            strerr=result.stderr,
            exit_code=result.returncode,
            timed_out=False,
            success=result.returncode == 0
        )
    except subprocess.TimeoutExpired as e:
        return ExecutionResult(
            stdout=e.stdout or "",
            strerr=e.stderr or "",
            exit_code=-1,
            timed_out=True,
            success=False
        )
    finally:
        script_path.unlink(missing_ok=True)  # Clean up the temporary file