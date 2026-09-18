# GAIA Local Agent

A local ReAct-style agent for the Hugging Face Agents Course Unit 4 assignment.
Runs entirely on your own machine — no need to duplicate the Space.

## 1. Install dependencies

```
pip install -r requirements.txt
```

## 2. Get a free Groq API key

Hugging Face's own free tier only gives you about $0.10/month in Inference
Provider credits — enough for roughly one question. Groq's free tier is much
more usable (30 requests/minute, 1,000/day, no card required), so the agent
calls Groq instead.

- Go to https://console.groq.com and sign up
- Create an API key under Settings → API Keys
- Set it as an environment variable:

Windows (cmd):
```
set GROQ_API_KEY=your_key_here
```

Mac/Linux:
```
export GROQ_API_KEY=your_key_here
```

## 3. Put your code somewhere public

Since duplicating a Gradio Space now requires a paid plan, create a free
**Static** Space instead (huggingface.co/new-space → SDK: Static → Public)
and upload these files there. It won't run, but it gives you a public
`.../tree/main` link to use as `agent_code` when you submit.

## 4. Run it

```
python run_local_eval.py
```

This will:
1. Fetch the 20 GAIA questions
2. Download any file attached to each task
3. Run the agent (`agent.py`) on each question, using tools in `tools.py`
4. Save all answers to `local_eval_answers.json`
5. Ask if you want to submit now — if yes, it POSTs your answers along with
   your username and the Space link from step 3

## Files

- `agent.py` — the agent loop (Thought → Action → Observation → Final Answer)
- `tools.py` — web search, Wikipedia lookup, calculator, file reading
- `run_local_eval.py` — fetches questions, runs the agent, saves/submits answers
- `requirements.txt` — Python dependencies

## Notes / things to improve

- The model used is `llama-3.3-70b-versatile` via Groq's free API (override
  with the `GAIA_MODEL_ID` environment variable — Groq also hosts
  `openai/gpt-oss-120b` and others if you want to compare).
- `read_file` only handles plain text/CSV. GAIA tasks sometimes include
  Excel, PDF, or image files — you'll want to extend `tools.py` with
  `openpyxl`, `pypdf`, or an image-captioning call if you hit those.
- The agent gets 6 reasoning steps max (`MAX_STEPS` in `agent.py`) before
  giving up — raise it if questions need more tool calls.
