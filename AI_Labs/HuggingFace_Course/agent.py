"""
GAIA Agent - a simple ReAct-style agent using the Hugging Face Inference API.

The agent alternates between:
  Thought -> Action -> Observation
until it produces a Final Answer.

Set the HF_TOKEN environment variable before running (a free Hugging Face
account token works fine): https://huggingface.co/settings/tokens
"""

import os
import re
import time
from typing import Optional

import requests

from tools import TOOLS, TOOL_DESCRIPTIONS

MODEL_ID = os.environ.get("GAIA_MODEL_ID", "qwen/qwen3.8-27b")
MAX_STEPS = 8
MAX_HISTORY_CHARS = 10000
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = f"""You are a careful research assistant solving exact-answer questions.

You have access to these tools:
{TOOL_DESCRIPTIONS}

Respond using this exact format, one step at a time:

Thought: <your reasoning about what to do next>
Action: <tool_name>[<tool input>]

When you use a tool, STOP right after the Action line and wait for the Observation.

Once you know the final answer, respond with ONLY:
Thought: <brief reasoning>
Final Answer: <the answer, and nothing else>

Rules for the final answer:
- Give the shortest possible exact answer (a number, a name, a short phrase).
- No explanations, no units unless asked, no extra words, and never the phrase "FINAL ANSWER".
- If it's a number, don't use commas or currency symbols unless explicitly asked for them.
"""


class BasicAgent:
    def __init__(self, model_id: str = MODEL_ID):
        self.model_id = model_id
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "Set the GROQ_API_KEY environment variable "
                "(free key from https://console.groq.com)."
            )

    def __call__(self, question: str, file_path: Optional[str] = None) -> str:
        history = [{"role": "system", "content": SYSTEM_PROMPT}]
        user_msg = question
        if file_path:
            user_msg += f"\n\n(A file for this task was downloaded to: {file_path})"
        history.append({"role": "user", "content": user_msg})

        for _ in range(MAX_STEPS):
            self._trim_history(history)
            reply = self._chat(history)
            history.append({"role": "assistant", "content": reply})

            final = self._extract_final_answer(reply)
            if final is not None:
                return final

            action = self._extract_action(reply)
            if action is None:
                history.append({
                    "role": "user",
                    "content": "Please continue using the Thought/Action or Final Answer format.",
                })
                continue

            tool_name, tool_input = action
            observation = self._run_tool(tool_name, tool_input)
            history.append({"role": "user", "content": f"Observation: {observation}"})

        return "Unable to determine an answer within the step limit."

    @staticmethod
    def _trim_history(history):
        """Drop the oldest Thought/Observation exchanges once the conversation
        gets too large for one request, keeping the system prompt and the
        original question (indices 0 and 1) intact."""
        total = sum(len(m["content"]) for m in history)
        while total > MAX_HISTORY_CHARS and len(history) > 3:
            removed = history.pop(2)
            total -= len(removed["content"])

    def _chat(self, history) -> str:
        for attempt in range(3):
            resp = requests.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model_id,
                    "messages": history,
                    "max_completion_tokens": 1200,
                    "temperature": 0.0,
                    "stop": ["Observation:"],
                },
                timeout=60,
            )
            if resp.status_code == 429:
                wait = float(resp.headers.get("Retry-After", 10))
                if wait > 30:
                    raise RuntimeError(
                        f"Groq is asking you to wait {wait:.0f}s — that's a daily/hourly "
                        "quota, not a per-minute limit. Retrying now won't help; stop and "
                        "try again later, or switch GAIA_MODEL_ID to a different model."
                    )
                print(f"Rate limited, waiting {wait:.0f}s...")
                time.sleep(wait)
                continue
            if resp.status_code >= 400:
                try:
                    detail = resp.json().get("error", {}).get("message", resp.text)
                except Exception:
                    detail = resp.text
                raise RuntimeError(f"Groq API error {resp.status_code}: {detail}")
            time.sleep(2.5)  # this model's free tier gets rate-limited harder than gpt-oss did
            return resp.json()["choices"][0]["message"]["content"].strip()
        raise RuntimeError("Groq is rate-limiting heavily right now (likely a daily quota, not just per-minute) — try again later.")

    @staticmethod
    def _extract_final_answer(text: str):
        match = re.search(r"Final Answer:\s*(.+)", text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip().split("\n")[0].strip()
        return None

    @staticmethod
    def _extract_action(text: str):
        match = re.search(r"Action:\s*(\w+)\[(.*)\]", text, re.DOTALL)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return None

    @staticmethod
    def _run_tool(tool_name: str, tool_input: str) -> str:
        tool = TOOLS.get(tool_name)
        if tool is None:
            return f"Unknown tool '{tool_name}'. Available tools: {', '.join(TOOLS)}"
        try:
            return str(tool(tool_input))[:1000]
        except Exception as e:
            return f"Tool error: {e}"
