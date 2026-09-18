"""
Fetches the GAIA evaluation questions, runs the agent on each one,
saves the answers locally, and (optionally) submits them for scoring.

Usage:
    Windows:      set HF_TOKEN=your_hf_token
    Mac/Linux:    export HF_TOKEN=your_hf_token
    Then:         python run_local_eval.py
"""

import json
import os
from typing import Optional

import requests

from agent import BasicAgent

API_URL = "https://agents-course-unit4-scoring.hf.space"
DOWNLOAD_DIR = "task_files"


def download_task_file(task_id: str) -> Optional[str]:
    """Downloads the file for a task, if one exists, and returns its local path."""
    url = f"{API_URL}/files/{task_id}"
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    path = os.path.join(DOWNLOAD_DIR, task_id)
    with open(path, "wb") as f:
        f.write(resp.content)
    return path


def fetch_questions():
    resp = requests.get(f"{API_URL}/questions", timeout=15)
    resp.raise_for_status()
    return resp.json()


def load_existing_answers(path="local_eval_answers.json"):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return {a["task_id"]: a for a in json.load(f)}
    except Exception:
        return {}


def _is_real_answer(answer: str) -> bool:
    if not answer:
        return False
    bad_markers = ("AGENT ERROR", "Unable to determine an answer")
    return not any(answer.startswith(m) for m in bad_markers)


def run_agent_on_questions(questions):
    agent = BasicAgent()
    existing = load_existing_answers()
    results = []

    for item in questions:
        task_id = item["task_id"]
        prior = existing.get(task_id)

        if prior and _is_real_answer(prior["submitted_answer"]):
            print(f"\n--- Task {task_id} already answered, skipping ---")
            results.append(prior)
            continue

        question = item["question"]
        print(f"\n--- Task {task_id} ---\n{question}")

        file_path = download_task_file(task_id)
        try:
            answer = agent(question, file_path=file_path)
        except Exception as e:
            answer = f"AGENT ERROR: {e}"
        print(f"Answer: {answer}")

        results.append({"task_id": task_id, "submitted_answer": answer})
        save_answers(results)  # save after every question, not just at the end
    return results


def save_answers(results, path="local_eval_answers.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(results)} answers to {path}")


def submit_answers(username: str, agent_code: str, results):
    payload = {"username": username, "agent_code": agent_code, "answers": results}
    resp = requests.post(f"{API_URL}/submit", json=payload, timeout=120)
    if resp.status_code >= 400:
        print(f"\nServer responded {resp.status_code}:")
        print(resp.text[:2000])
        resp.raise_for_status()
    return resp.json()


def main():
    questions = fetch_questions()
    print(f"Fetched {len(questions)} questions.")

    results = run_agent_on_questions(questions)
    save_answers(results)

    do_submit = input("\nSubmit these answers now? [y/N]: ").strip().lower()
    if do_submit == "y":
        username = input("Your Hugging Face username: ").strip()
        agent_code = input("Public URL to your code (Space tree/main link): ").strip()
        result = submit_answers(username, agent_code, results)
        print("\nSubmission result:")
        print(json.dumps(result, indent=2))
    else:
        print(
            "Skipped submission. Re-run and choose 'y', "
            "or submit local_eval_answers.json manually later."
        )


if __name__ == "__main__":
    main()
