# Test Cases - CivicVoice AI

## A. Live runs (real Gemini API calls, `gemini-3.6-flash`)

| # | Input | AI Output | Verdict |
|---|-------|-----------|---------|
| 1 | `sample_inputs/streetlight.jpeg` | Streetlight, confidence 95%, urgency Medium, routed to Electrical & Street Lighting Department | Correct |
| 2 | `sample_inputs/drainage.jpg` | Drainage, confidence 95%, urgency High, routed to Drainage & Sewerage Department | Correct |
| 3 | `sample_inputs/garbage.jpg` | Garbage, confidence 90%, urgency Low. The photo shows sanitation workers collecting waste normally; there is no real problem. | **Incorrect** - the draft complaint is vague and unnecessary |
| 4 | `sample_inputs/not_civic.png` | Garbage, confidence 95%, urgency Medium. The AI itself described the image as an illustration, yet still drafted a complaint. | **Incorrect** - an illustration was treated as a real issue |

### Incorrect / unsafe outputs identified
- **Problem presence is not checked.** The prompt asks for the *type* of scene, not whether a problem actually exists. Confidence reflects the category, not the problem.
- **Real-photo check is missing.** Illustrations and cartoons are accepted as genuine photos.

## B. Input validation (verified offline during development, no API call)

| Input | Expected result |
|-------|-----------------|
| Empty input | Rejected: "Input is empty..." |
| `hole` (too short) | Rejected: description too short |
| `sample_inputs/missing.jpg` (file absent) | Rejected: file not found |
| A text file renamed to `.jpg` | Rejected: not a valid image |
| Valid image / valid text | Accepted and sent to the AI |

Failure paths were also checked with a mocked AI layer: API error, malformed JSON and missing JSON fields each return a clean error status instead of crashing.

## C. Not yet run live
Pothole image, a true non-civic photo and a text description were planned but not captured as live runs. They are listed in the roadmap (M4).
