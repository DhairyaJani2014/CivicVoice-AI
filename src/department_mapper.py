"""
department_mapper.py
Maps the AI-identified issue type to the municipal department that
usually handles it. Kept as plain, editable data so it can be adapted
to any city's department names.
"""

DEPARTMENT_MAP = {
    "Pothole": "Roads & Infrastructure Department",
    "Garbage": "Solid Waste Management / Sanitation Department",
    "Streetlight": "Electrical & Street Lighting Department",
    "Drainage": "Drainage & Sewerage Department",
    "Water Leakage": "Water Supply Department",
    "Other Civic Issue": "General Grievance Cell (Municipal Corporation)",
}


def map_department(issue_type: str) -> str:
    """Returns the responsible department, or a clear message if not applicable."""
    if issue_type == "Not a Civic Issue":
        return "Not applicable - no civic issue detected"
    return DEPARTMENT_MAP.get(issue_type, "General Grievance Cell (Municipal Corporation)")