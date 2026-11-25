# CoT-replication

Replication, then extension, of hint-based chain-of-thought (CoT) faithfulness evaluations.
Baseline paper: Chen et al. 2025, "Reasoning Models Don't Always Say What They Think" (Anthropic).
Earlier related work: Turpin et al. 2023, "Language Models Don't Always Say What They Think"
(its code is cloned next door in `../cot-unfaithfulness`, reference only).

Read `NOTES.md` first for current status, results and next steps. Update it at the end of a session.

## The experiment

Each multiple-choice question is run twice: plain (baseline) and with a hint pointing at a wrong answer.
Two measurements:

- followed: the answer moves to the hinted letter (compared with the baseline answer for the same question)
- mentioned: the model's reasoning acknowledges the hint (judged by a grader model)

Faithfulness = mentioned, among the cases where the hint was followed.

Later phase: interpretability on the same open-weight model, so keep the model under test
open-weight and small enough to load on one rented GPU.

## Stack

- Python project managed with uv (`pyproject.toml`, `uv.lock`)
- Inspect (`inspect_ai`, UK AI Security Institute's eval framework)
- Dataset: MMLU via `hf_dataset("cais/mmlu", name="all", split="test")`, shuffled with seed 0, limit 100
- Model under test: `openrouter/qwen/qwen3-14b`, temperature 0
- Grader model: `openrouter/qwen/qwen3.8-27b`
- `OPENROUTER_API_KEY` lives in `.env` (Inspect loads it automatically). Never print or commit it.

## Commands

```
uv run inspect eval cot_hints.py@baseline --model openrouter/qwen/qwen3-14b --temperature 0
uv run inspect eval cot_hints.py@hinted   --model openrouter/qwen/qwen3-14b --temperature 0
uv run inspect view
uv run inspect eval-retry logs/<file>.eval      # finish samples that hung or errored
```

Use `--limit 5` for a quick check before a full run.
Local Ollama models are too slow for full runs (about 3 minutes per question on this laptop); use them only for tiny tests.

## Layout

- `cot_hints.py`: tasks (`baseline`, `hinted`), hint templates (`HINTS`), `add_hint`, `record_to_hinted_sample`, `hint_scorer`
- `logs/`: Inspect `.eval` logs, git-ignored. Copy logs that back a reported number into `results/` and commit those.
- `Modelfile`: Ollama variant of qwen3:4b with an 8192-token context (local tests only)

## Working agreements

- The author writes the experiment logic himself (hint construction, sample building, the followed/mentioned analysis). Review and explain; don't write those parts unprompted.
- For small fixes show only the changed lines and say which line numbers they replace. For new code end with one complete runnable block.
- Check `git status` before suggesting commit commands; only suggest commits for what is uncommitted.
- Take hint wording from the paper's own tables, and say so when something is from memory and unverified.
- Define acronyms on first use.
