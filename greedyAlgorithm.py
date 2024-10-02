import json
from math import ceil
from operator import itemgetter


def calculateTotalAvailableHours(timetableJSON):
    """Calculate total available hours in a week after work hours are scheduled."""
    total_available_hours = 0
    for day in timetableJSON["hoursWorkedWeekly"].keys():
        total_available_hours += (8 - timetableJSON["hoursWorkedWeekly"][day])
    return total_available_hours

def allocateStudyTime(timetableJSON):
    """
    Allocates study time to courses based on ECTS and difficulty ranking.
    Prioritizes courses with higher `ECTS * ranking`.
    """
    # Load course data
    semester_courses = timetableJSON["semesterCourses"]
    
    # Calculate total available hours
    total_available_hours = calculateTotalAvailableHours(timetableJSON)
    
    # Calculate total "weight" of each course based on ECTS * difficulty ranking
    for course in semester_courses:
        course['ranking'] = int(course["ECTS"]) * int(course["personalRanking"])

    # Sort courses based on the weight in descending order
    sorted_courses = sorted(semester_courses, key=itemgetter('ranking'), reverse=True)
    
    # Distribute the available hours based on course weights
    total_weight = sum(course['ranking'] for course in sorted_courses)
    
    for course in sorted_courses:
        allocated_hours = (course['ranking'] / total_weight) * total_available_hours
        course['allocatedStudyHours'] = ceil(round(allocated_hours, 2))
        
    # Update the timetable with the allocated study hours
    timetableJSON["semesterCourses"] = sorted_courses
    
    #update JSON
    with open("timetableData.json", "w") as f:
        json.dump(timetableJSON, f, indent=4)
    
    return sorted_courses  