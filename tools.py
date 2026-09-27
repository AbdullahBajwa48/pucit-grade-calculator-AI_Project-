"""Deterministic GPA/CGPA tools for the PUCIT BS(CS) conversational agent."""

from __future__ import annotations

from pathlib import Path
from typing import Union

from langchain.tools import tool


COURSES: dict[int, list[tuple[str, str, float]]] = {
    1: [
        ("MS-251", "Probability & Statistics", 3.0),
        ("GE-160", "Applications of ICT", 3.0),
        ("GE-169", "Applied Physics", 3.0),
        ("GE-167", "Discrete Structures", 3.0),
        ("HQ-001", "Quran Translation - I", 0.5),
        ("GE-190", "Functional English", 3.0),
    ],
    2: [
        ("CC-112", "Programming Fundamentals", 3.0),
        ("CC-112-L", "Programming Fundamentals Lab", 1.0),
        ("CC-110", "Digital Logic Design", 2.0),
        ("CC-110-L", "Digital Logic Design Lab", 1.0),
        ("MS-252", "Linear Algebra", 3.0),
        ("GE-191", "Expository Writing", 3.0),
        ("GE-163", "Islamic Studies", 2.0),
        ("HQ-002", "Quran Translation - II", 0.5),
    ],
    3: [
        ("CC-211", "Object Oriented Programming", 3.0),
        ("CC-211-L", "Object Oriented Programming Lab", 1.0),
        ("CC-215", "Database Systems", 3.0),
        ("CC-215-L", "Database Systems Lab", 1.0),
        ("CC-210", "Computer Organization & Assembly Language", 3.0),
        ("GE-162", "Calculus & Analytical Geometry", 3.0),
        ("GE-192", "Introduction to Management", 2.0),
        ("HQ-003", "Quran Translation - III", 0.5),
    ],
    4: [
        ("CC-213", "Data Structures", 3.0),
        ("CC-213-L", "Data Structures Lab", 1.0),
        ("CC-312", "Information Security", 3.0),
        ("CC-214", "Computer Networks", 3.0),
        ("CC-212", "Software Engineering", 3.0),
        ("DC-220", "Advanced Database Management Systems", 3.0),
        ("HQ-004", "Quran Translation - IV", 0.5),
    ],
    5: [
        ("CC-313", "Analysis of Algorithms", 3.0),
        ("CC-310", "Artificial Intelligence", 3.0),
        ("DC-320", "Theory of Automata and Formal Languages", 3.0),
        ("DC-321", "Human Computer Interaction", 3.0),
        ("DC-322", "Computer Architecture", 3.0),
        ("EC-330", "Web Technologies / Elective", 3.0),
        ("HQ-005", "Quran Translation - V", 0.5),
    ],
    6: [
        ("CC-311", "Operating Systems", 3.0),
        ("EC-333", "Mobile Application Development / Elective", 3.0),
        ("EC-324", "Software Construction & Development / Elective", 3.0),
        ("EC-335", "Machine Learning / Elective", 3.0),
        ("EC-334", "Game Design and Development / Elective", 3.0),
        ("MS-253", "Multivariable Calculus", 3.0),
        ("HQ-006", "Quran Translation - VI", 0.5),
    ],
    7: [
        ("CC-411", "Final Year Project - I", 2.0),
        ("DC-328", "Parallel & Distributed Computing", 3.0),
        ("EC-345", "Computer Vision / Elective", 3.0),
        ("EC-425", "Software Quality Engineering / Elective", 3.0),
        ("MS-254", "Technical and Business Writing", 3.0),
        ("GE-263", "Entrepreneurship", 2.0),
        ("GE-262", "Professional Practices", 2.0),
        ("HQ-007", "Quran Translation - VII", 0.5),
    ],
    8: [
        ("CC-412", "Final Year Project - II", 4.0),
        ("DC-421", "Compiler Construction", 3.0),
        ("UE-272", "Introduction to Marketing", 3.0),
        ("GE-168", "Ideology and Constitution of Pakistan", 2.0),
        ("GE-363", "Civics and Community Engagement", 2.0),
        ("HQ-008", "Quran Translation - VIII", 0.5),
    ],
}

GRADE_BANDS: tuple[tuple[int, float, str], ...] = (
    (85, 4.0, "A"),
    (80, 3.7, "A-"),
    (75, 3.3, "B+"),
    (70, 3.0, "B"),
    (65, 2.7, "B-"),
    (61, 2.3, "C+"),
    (58, 2.0, "C"),
    (55, 1.7, "C-"),
    (50, 1.0, "D"),
    (0, 0.0, "F"),
)


def _valid_marks(marks: int) -> bool:
    return isinstance(marks, int) and 0 <= marks <= 100


def _valid_nonnegative(value: float) -> bool:
    return isinstance(value, (int, float)) and value >= 0


@tool
def marks_to_grade_points(marks: int) -> float:
    """Use when a student's marks must be converted to PUCIT grade points; return an error for marks outside the valid range."""
    if not _valid_marks(marks):
        return "Error: marks must be an integer between 0 and 100"
    for minimum, points, _grade in GRADE_BANDS:
        if marks >= minimum:
            return points
    return 0.0


@tool
def calculate_semester_gpa(
    grade_points: list[float], credit_hours: list[float]
) -> float:
    """Use after grade points and matching credit hours are known to calculate one semester's credit-weighted GPA."""
    if len(grade_points) != len(credit_hours):
        return "Error: grade_points and credit_hours must have the same length"
    if not grade_points:
        return "Error: at least one course is required"
    if any(not isinstance(g, (int, float)) or not 0.0 <= g <= 4.0 for g in grade_points):
        return "Error: grade points must be between 0.0 and 4.0"
    if any(not _valid_nonnegative(c) for c in credit_hours):
        return "Error: credit hours must be non-negative numbers"
    total_hours = sum(credit_hours)
    if total_hours <= 0:
        return "Error: total credit hours must be greater than 0"
    return sum(g * c for g, c in zip(grade_points, credit_hours)) / total_hours


@tool
def calculate_new_cgpa(
    current_cgpa: float,
    completed_credit_hours: float,
    semester_gpa: float,
    semester_credit_hours: float,
) -> float:
    """Use when projecting a student's cumulative GPA after adding one completed semester."""
    if not isinstance(current_cgpa, (int, float)) or not 0.0 <= current_cgpa <= 4.0:
        return "Error: current_cgpa must be between 0.0 and 4.0"
    if not _valid_nonnegative(completed_credit_hours):
        return "Error: completed_credit_hours must be non-negative"
    if not isinstance(semester_gpa, (int, float)) or not 0.0 <= semester_gpa <= 4.0:
        return "Error: semester_gpa must be between 0.0 and 4.0"
    if not isinstance(semester_credit_hours, (int, float)) or semester_credit_hours <= 0:
        return "Error: semester_credit_hours must be greater than 0"
    denominator = completed_credit_hours + semester_credit_hours
    if denominator <= 0:
        return "Error: total credit hours must be greater than 0"
    return (
        current_cgpa * completed_credit_hours
        + semester_gpa * semester_credit_hours
    ) / denominator


@tool
def required_gpa_for_target(
    target_cgpa: float,
    current_cgpa: float,
    completed_credit_hours: float,
    remaining_credit_hours: float,
) -> float:
    """Use when calculating the GPA required over a specified remaining-credit-hour horizon to reach a target CGPA."""
    for name, value in (
        ("target_cgpa", target_cgpa),
        ("current_cgpa", current_cgpa),
    ):
        if not isinstance(value, (int, float)) or not 0.0 <= value <= 4.0:
            return f"Error: {name} must be between 0.0 and 4.0"
    if not _valid_nonnegative(completed_credit_hours):
        return "Error: completed_credit_hours must be non-negative"
    if not isinstance(remaining_credit_hours, (int, float)) or remaining_credit_hours <= 0:
        return "Error: remaining_credit_hours must be greater than 0"
    return (
        target_cgpa * (completed_credit_hours + remaining_credit_hours)
        - current_cgpa * completed_credit_hours
    ) / remaining_credit_hours


@tool
def get_semester_courses(semester: int) -> str:
    """Use when a student gives a semester number and you need that semester's official courses and credit hours."""
    if not isinstance(semester, int) or not 1 <= semester <= 8:
        return "Error: semester must be between 1 and 8"
    # Asking for the official current-semester scheme establishes a fresh
    # target-planning context for the current conversation.
    global _planning_start_semester
    _planning_start_semester = semester
    lines = [f"Semester {semester} courses:"]
    for code, name, credits in COURSES[semester]:
        lines.append(f"{code} | {name} | {credits} credit hours")
    return "\n".join(lines)


@tool
def get_remaining_credit_hours(current_semester: int) -> float:
    """Use for target-GPA planning to total graded credit hours from the planning-start semester through the supplied horizon semester."""
    if not isinstance(current_semester, int) or not 1 <= current_semester <= 8:
        return "Error: semester must be between 1 and 8"
    start = globals().get("_planning_start_semester")
    if start is None:
        start = current_semester
        globals()["_planning_start_semester"] = start
    if current_semester < start:
        return "Error: planning horizon cannot move backward"
    return sum(
        credits
        for semester in range(start, current_semester + 1)
        for _code, _name, credits in COURSES[semester]
    )


@tool
def save_report(filename: str, content: str) -> str:
    """Use only after the student explicitly asks to save a useful GPA/CGPA result or plan; never save automatically."""
    if not isinstance(filename, str) or not filename.strip():
        return "Error: filename must not be empty"
    if not isinstance(content, str) or not content.strip():
        return "Error: content must not be empty"
    safe_name = Path(filename).name
    if safe_name != filename or safe_name in {".", ".."}:
        return "Error: filename must be a simple filename without directories"
    if not safe_name.lower().endswith(".txt"):
        safe_name += ".txt"
    reports_dir = Path(__file__).resolve().parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    destination = reports_dir / safe_name
    try:
        destination.write_text(content, encoding="utf-8")
    except OSError as exc:
        return f"Error: could not save report: {exc}"
    return f"Report saved successfully as {destination.name}"


TOOLS = [
    marks_to_grade_points,
    calculate_semester_gpa,
    calculate_new_cgpa,
    required_gpa_for_target,
    get_semester_courses,
    get_remaining_credit_hours,
    save_report,
]
