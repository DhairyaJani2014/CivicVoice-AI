# CivicVoice AI

An AI assistant that helps citizens report civic issues (potholes, garbage, broken streetlights, drainage problems) to the right municipal department. The user provides a photo or a text description; CivicVoice AI classifies the issue, identifies the responsible department, and drafts a formal complaint that the user **reviews and submits manually**.

> Built as the Week 10 capstone blueprint for the Generative AI Internship at Davine Technologies.

## Problem
Many civic issues go unreported because citizens do not know which department is responsible or how to phrase a formal complaint.

## How It Works
```
User -> Input Handler -> Prompt Builder -> Gemini API -> Response Parser -> Department Mapper -> Draft Complaint -> Human Review -> Log
```

## Features
- Accepts a photo path **or** a text description
- Input validation before any API call (empty, missing file, fake/corrupt image, too-short text)
- Classifies into a fixed set of issue types, so department mapping is deterministic
- Drafts a formal complaint using placeholders (`[LOCATION]`, `[DATE]`, `[YOUR NAME]`) instead of inventing facts
- Automatic retry for temporary API errors (503 / 429)
- Human review checkpoint: nothing is ever auto-submitted
- Every run is saved to `outputs/civic_reports_log.json`

## Project Structure
```
CivicVoice-AI/
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── src/
│   ├── civicvoice.py          # main entry point
│   ├── input_handler.py       # validates image/text input
│   ├── prompt_builder.py      # reusable prompt template
│   ├── department_mapper.py   # issue type -> department
│   └── response_parser.py     # parses/validates AI JSON
├── sample_inputs/             # test images
├── outputs/                   # run log (git-ignored)
├── docs/                      # diagrams, roadmap, summary
└── tests/                     # documented test cases
```

## Setup
1. Clone the repository and open the folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your own Gemini API key (never commit `.env`).
4. Run: `python src/civicvoice.py` (from the project root)

## Usage
```
Photo path / description: sample_inputs/pothole.jpg
Photo path / description: Garbage pile overflowing near the market for a week
Photo path / description: exit
```

## Known Limitations
- Department names are generic; real municipal bodies use city-specific names.
- Classification quality depends on photo clarity; blurry or multi-issue photos may be misclassified.
- Complaint drafts need the user to add location, date and name.
- Command-line only; no web UI, database or multi-language support yet.

## Tech Stack
Python 3.13, Google Gemini API (`gemini-3.6-flash`), Pillow, python-dotenv.

## Author
Dhairya Jani - Generative AI Intern, Davine Technologies