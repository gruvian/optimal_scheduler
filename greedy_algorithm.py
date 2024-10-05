import json
from math import ceil
from operator import itemgetter


def calculate_total_available_hours(timetableJSON):
    """Calculate total available hours in a week after work hours are scheduled."""
    total_available_hours = 0
    for day in timetableJSON["hours_worked_weekly"].keys():
        total_available_hours += (7 - timetableJSON["hours_worked_weekly"][day])
    return total_available_hours


def calculate_past_performance_boost(course_name, performanceJSON):
    """
    Adjusts the study allocation based on past performance.
    If the grade was high (closer to 10), we reduce the weight.
    If the grade was low, we increase the weight.
    """
    for past_course in performanceJSON:
        if past_course['course_name'] == course_name:  # adjust for belongs in group
            grade = past_course['grade']
            # Reduce ranking for higher grades, and boost for lower grades
            return (10 - grade) / 5  # Scaling factor
    return 1  # Default factor if no previous performance exists


def allocate_study_time(timetableJSON):
    """
    Allocates study time to courses based on ECTS, difficulty ranking, and past performance.
    """
    # Load course data
    semester_courses = timetableJSON["semester_courses"]

    # Load past performance data
    with open("previous_performance.json", "r") as f:
        performanceJSON = json.load(f)

    # Calculate total available hours
    total_available_hours = calculate_total_available_hours(timetableJSON)

    # Calculate total "weight" of each course based on ECTS * difficulty ranking
    for course in semester_courses:
        # Apply performance boost/penalty
        past_performance_boost = calculate_past_performance_boost(course['course_name'], performanceJSON)
        course['ranking'] = int(course["ECTS"]) * int(course["personal_ranking"]) * past_performance_boost

    # Sort courses based on the weight in descending order
    sorted_courses = sorted(semester_courses, key=itemgetter('ranking'), reverse=True)

    # Distribute the available hours based on course weights
    total_weight = sum(course['ranking'] for course in sorted_courses)

    for course in sorted_courses:
        allocated_hours = (course['ranking'] / total_weight) * total_available_hours
        course['allocated_study_hours'] = ceil(round(allocated_hours, 2))

    # Update the timetable with the allocated study hours
    timetableJSON["semester_courses"] = sorted_courses

    # Update JSON
    with open("timetable_data.json", "w") as f:
        json.dump(timetableJSON, f, indent=4)

    return sorted_courses