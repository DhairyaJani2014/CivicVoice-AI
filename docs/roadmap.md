# Development Roadmap - CivicVoice AI

| Milestone | Deliverables | Status |
|-----------|--------------|--------|
| M1 Planning and design | Problem statement, architecture, workflow, tech stack, repo structure | Done |
| M2 Core prototype | Photo/text -> validation -> Gemini -> department -> draft complaint | Done |
| M3 Testing | Live runs documented, incorrect outputs analysed | Done |
| M4 Accuracy fixes | Add `problem_present` field; add real-photo check; run pothole, non-civic and text cases live | Next |
| M5 Web app | Streamlit UI, report history (SQLite), multi-language complaints, city-specific department mapping | Planned |

## Remaining work in detail
1. Update the prompt and parser so the model must state whether a real problem is visible, and skip the complaint if not.
2. Ask the model whether the image is a real photograph; reject illustrations and screenshots.
3. Replace generic department names with a per-city mapping file.
4. Build a Streamlit front end with photo upload and a copy-to-clipboard complaint.
5. Store reports in SQLite instead of a JSON file.
6. Add automated tests (pytest) for the validators and parser.
