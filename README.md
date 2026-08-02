# Autonomous Self-Correcting Code Agent

An agentic system that generates Python code from natural-language tasks, executes it in an isolated sandbox, parses failures, retrieves relevant docs and past error-fix pairs via RAG, and iteratively repairs the code until tests pass — benchmarked on HumanEval/MBPP.

Runs entirely locally and free of cost: [Ollama](https://ollama.com) (`qwen2.5-coder:7b`) for code generation instead of a paid LLM API, with everything else (vector DB, embeddings, sandbox, dataset) already free by design.

## Architecture

```
task (natural language)
      |
      v
 [RAG retrieval]  --  docs corpus + past error-fix memory
      |
      v
 [LLM code generation]  --  Ollama, structured JSON output (pydantic)
      |
      v
 [sandboxed execution]  --  subprocess (Phase 1) -> Docker (Phase 3)
      |
      v
 [test evaluation]  --  pytest-based pass/fail signal
      |
      v
   pass? --yes--> done
      |
      no
      |
      v
 [error parsing] -> retrieve similar past fixes -> regenerate (retry, capped)
      |
      v
 successful fix stored back into vector DB as error-fix memory
```

## Tech stack

| Layer | Tech |
|---|---|
| Language | Python 3.12 |
| LLM | Ollama, `qwen2.5-coder:7b` (local, OpenAI-compatible endpoint) |
| Sandbox | `subprocess` (Phase 1) → Docker SDK for Python (Phase 3) |
| Testing | pytest |
| Vector DB | ChromaDB |
| Embeddings | sentence-transformers (local) |
| Data validation | pydantic |
| Benchmark dataset | HumanEval / MBPP (HuggingFace `datasets`) |
| Dependency management | `uv` |

## Project structure

```
agent/          # orchestrator: PLAN -> GENERATE -> EXECUTE -> EVALUATE -> RETRY/DONE state machine
sandbox/        # isolated code execution — the only module allowed to run untrusted code
retriever/      # RAG: chunking, embedding, retrieval logic
vector_store/   # ChromaDB persistence (gitignored)
eval/           # benchmarking harness (HumanEval/MBPP runner)
logs/           # structured JSON run logs (gitignored)
```

## Setup

```powershell
# Install dependencies
pip install uv
uv sync

# Install Ollama (https://ollama.com) and pull the model
ollama pull qwen2.5-coder:7b

# Copy environment config
Copy-Item .env.example .env
```

## Status

Building phase by phase — see [autonomous-code-agent-project-plan.md](../autonomous-code-agent-project-plan%20%282%29.md) for the full breakdown.

- [x] Phase 0 — repo scaffolding & environment setup
- [ ] Phase 1 — core agent loop (in progress: schemas and subprocess executor written; LLM client and Agent state machine next)
- [ ] Phase 2 — error parsing layer
- [ ] Phase 3 — sandboxed execution (Docker)
- [ ] Phase 4 — evaluation layer (pytest)
- [ ] Phase 5 — RAG: documentation grounding
- [ ] Phase 6 — RAG: error-fix memory
- [ ] Phase 7 — benchmarking harness (HumanEval/MBPP)
- [ ] Phase 8 — observability & polish
- [ ] Phase 9 (optional) — FastAPI service wrapper
