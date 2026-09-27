"""Small deterministic smoke tests for the required tools."""

from tools import (
    calculate_new_cgpa,
    calculate_semester_gpa,
    get_remaining_credit_hours,
    get_semester_courses,
    marks_to_grade_points,
    required_gpa_for_target,
)


def test_grade_bands() -> None:
    expected = {
        85: 4.0, 84: 3.7, 79: 3.3, 74: 3.0, 69: 2.7,
        64: 2.3, 60: 2.0, 57: 1.7, 54: 1.0, 49: 0.0,
    }
    for marks, points in expected.items():
        assert marks_to_grade_points.invoke({"marks": marks}) == points


def test_semester_gpa() -> None:
    result = calculate_semester_gpa.invoke({
        "grade_points": [4.0, 3.7, 2.3],
        "credit_hours": [3.0, 3.0, 3.0],
    })
    assert abs(result - (10.0 / 3.0)) < 1e-12


def test_new_cgpa() -> None:
    result = calculate_new_cgpa.invoke({
        "current_cgpa": 3.0,
        "completed_credit_hours": 64.0,
        "semester_gpa": 3.6,
        "semester_credit_hours": 18.5,
    })
    expected = (3.0 * 64.0 + 3.6 * 18.5) / (64.0 + 18.5)
    assert abs(result - expected) < 1e-12


def test_target_horizons() -> None:
    get_semester_courses.invoke({"semester": 5})
    h5 = get_remaining_credit_hours.invoke({"current_semester": 5})
    h6 = get_remaining_credit_hours.invoke({"current_semester": 6})
    h7 = get_remaining_credit_hours.invoke({"current_semester": 7})
    assert h5 == 18.5
    assert h6 == 37.0
    assert h7 == 55.5

    first = required_gpa_for_target.invoke({
        "target_cgpa": 3.4,
        "current_cgpa": 3.0,
        "completed_credit_hours": 64.0,
        "remaining_credit_hours": 18.5,
    })
    second = required_gpa_for_target.invoke({
        "target_cgpa": 3.4,
        "current_cgpa": 3.0,
        "completed_credit_hours": 64.0,
        "remaining_credit_hours": 37.0,
    })
    third = required_gpa_for_target.invoke({
        "target_cgpa": 3.4,
        "current_cgpa": 3.0,
        "completed_credit_hours": 64.0,
        "remaining_credit_hours": 55.5,
    })
    assert abs(first - 4.783783783783784) < 1e-12
    assert abs(second - 4.091891891891892) < 1e-12
    assert abs(third - 3.861261261261261) < 1e-12


def test_invalid_inputs_are_errors() -> None:
    assert str(get_semester_courses.invoke({"semester": 9})).startswith("Error:")
    assert str(get_remaining_credit_hours.invoke({"current_semester": 0})).startswith("Error:")
    assert str(marks_to_grade_points.invoke({"marks": 101})).startswith("Error:")


if __name__ == "__main__":
    test_grade_bands()
    test_semester_gpa()
    test_new_cgpa()
    test_target_horizons()
    test_invalid_inputs_are_errors()
    print("All deterministic tool tests passed.")
