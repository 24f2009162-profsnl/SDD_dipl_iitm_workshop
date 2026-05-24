# 🚀 Reports API: CSV Export Feature
*An exploration of Spec-Driven Development (SDD) vs. Vibe Coding*

## 📖 Overview
This repository contains my submission for the **Future of Software Development with LLMs** workshop. The primary objective was to implement a secure, scalable CSV export feature (`GET /reports.csv`) for an existing FastAPI backend. 

More importantly, this project serves as a practical comparative study between two AI-assisted coding paradigms: unstructured "Vibe Coding" and structured "Spec-Driven Development" (SDD).

## 🌿 Branch Architecture & Methodology

To demonstrate the contrasting methodologies, this project is split into distinct branches:

### 1. The `vibe-work` Branch (Round 1)
* **Approach:** Unstructured prompting ("Vibe Coding"). The feature was requested via a raw natural language prompt with no underlying architectural constraints.
* **Result:** While the AI generated functional code quickly, it produced a naive implementation. It failed to respect data privacy boundaries (leaking `internal_id` and `owner_email`) and lacked safety constraints (no row-cap limits).

### 2. The `openspec-work` Branch (Round 3)
* **Approach:** Spec-Driven Development using the `openspec` CLI (v1.2.0). 
* **Process:** 1. Created a strict `proposal.md` defining the *Why*, *What*, and *Impact*.
  2. Defined explicit requirements in `specs/reports/spec.md` (e.g., RFC 4180 compliance).
  3. Validated and archived the specs before finalizing the implementation.
* **Result:** A bulletproof, production-ready implementation. The SDD approach forced the AI to respect a strict column allowlist, successfully mitigating data leaks, and inherently handled edge cases like the 100,000-row `HTTP 413` cap.

## 🛠️ Technical Stack
* **Backend:** Python, FastAPI
* **Tooling:** OpenSpec CLI (`@fission-ai/openspec`)
* **Workflow:** Git, Virtual Environments (`venv`)

## 🎓 Acknowledgments
A massive thank you to **Prof. Saikiran Puvvada** for designing such a brilliant and eye-opening workshop. The transition from chaotic "prompt-and-pray" generation to structured, spec-driven architecture has completely changed how I approach AI-assisted software engineering. The "trap" of Round 1 was an incredible teaching moment!

