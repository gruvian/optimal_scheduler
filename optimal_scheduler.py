import json
import os
import sys
import subprocess

import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from math import ceil
from operator import itemgetter

import sys
import os


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


def resource_path(relative_path):
    """ PyInstaller paths """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)

previous_performance_path = resource_path('previous_performance.json')

def get_default_schedule():
    """Creates default timetable JSON when new template creation
    is requested"""
    return {
        "wake_up_time": "08:00:00",
        "hours_worked_weekly": {
            "monday": 4, "tuesday": 4, "wednesday": 4,
            "thursday": 4, "friday": 4
        },
        "start_work_hours_weekly": {
            "monday": 9, "tuesday": 9, "wednesday": 9,
            "thursday": 9, "friday": 9
        },
        "semester_courses": [
            {"course_name": f"Course {i + 1}", "ECTS": "5 ECTS", "group": "",
             "personal_ranking": "1", "ranking": 0} for i in range(6)
        ]
    }


def create_course_optimized_schedule():
    """Allocates study time using the greedy algorithm and updates the schedule."""
    with open(resource_path("timetable_data.json"), "r") as f:
        timetable_json = json.load(f)

    # Allocate study time using the greedy algorithm
    allocated_courses = allocate_study_time(timetable_json)
    return allocated_courses


def show_time_distribution(filename: str):
    """Displays a bar chart showing the study hours needed for each course over 3 months"""

    # Load the timetable data from the JSON file
    with open(filename, "r") as f:
        timetable_json = json.load(f)

    # Extract course names and study hours from the data
    courses = [course["course_name"] for course in timetable_json["semester_courses"]]
    allocated_hours = [course["allocated_study_hours"] for course in timetable_json["semester_courses"]]
    total_hours = [x * 17 for x in allocated_hours]
    # Create a bar plot
    fig, ax = plt.subplots()
    ax.bar(courses, total_hours, color='skyblue')

    # Customize the plot
    ax.set_title("Total study time over 3 months for each course")
    ax.set_xlabel("courses")
    ax.set_ylabel("total hours")
    plt.xticks(rotation=45, ha='right')

    # Display the plot
    plt.tight_layout()
    plt.show()


class Gui(QtWidgets.QWidget):
    """Optimal Scheduler GUI Main Page"""

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Optimal Scheduler")
        self.dark_mode_flag = self.detect_dark_mode_gnome()
        theme = 'night_theme.css' if self.dark_mode_flag else 'day_theme.css'
        self.setStyleSheet(open(resource_path("night_theme.css")).read())
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)
        self.init_gui()

    def detect_dark_mode_gnome(self):
        """Detects dark mode in GNOME"""
        if not hasattr(self, '_dark_mode_detected'):
            get_args = ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme']
            current_theme = subprocess.run(get_args, capture_output=True).stdout.decode("utf-8").strip().strip("'")
            dark_indicator = '-dark'
            self._dark_mode_detected = current_theme.endswith(dark_indicator)
        return self._dark_mode_detected

    def display_logo(self):
        """Displays logo on grid"""
        self.logo = QtWidgets.QLabel()
        if self.dark_mode_flag:
            self.pixmap = QPixmap(resource_path("logoDark.png"))
        else:
            self.pixmap = QPixmap(resource_path("logoLight.png"))
        self.logo.setPixmap(self.pixmap)
        self.grid.addWidget(self.logo, 0, 0)

    def add_label(self, text: str, row: int, col: int, style=""):
        """Adds QLabel on grid"""
        label = QtWidgets.QLabel(text)
        label.setWordWrap(True)
        if style != "":
            label.setStyleSheet(style)
        self.grid.addWidget(label, row, col)

    def add_line_edit(self, text: str, row: int, col: int):
        """Adds QLineEdit on grid"""
        line_edit = QtWidgets.QLineEdit(text)
        self.grid.addWidget(line_edit, row, col)
        return line_edit

    def add_button(self, text: str, row: int, col: int, func):
        """Adds QPushButton on grid"""
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(func)
        self.grid.addWidget(button, row, col)

    def add_course_inputs(self, row: int, ranking_grade_flag: bool):
        """Adds course inputs on grid to get user data on current
        semester courses, ECTS and perceived difficulty ranking when
        ranking_grade_flag = True and previous courses, ECTS and previous
        grades inputs when ranking_grade_flag = False"""
        label = self.add_line_edit(f"Course {row - 1}", row, 0)
        ects = self.add_line_edit("5", row, 1)
        self.add_label("ECTS", row, 2)
        if ranking_grade_flag:
            ranking = self.add_line_edit("1", row, 3)
            return label, ects, ranking
        else:
            grade = self.add_line_edit("5.00", row, 4)
            return label, ects, grade

    def init_gui(self):
        """Initializes the GUI"""
        self.clear_layout()
        self.display_logo()

        self.add_label("Welcome! What would you like to do today?", 1, 0)
        self.add_button("Create new weekly schedule", 2, 0, self.create_new_schedule)
        self.add_button("Open existing schedule", 3, 0, self.view_old_schedule)

        if not os.path.exists(resource_path("timetable_data.json")):
            with open(resource_path("timetable_data.json"), "w") as f:
                f.write(json.dumps(get_default_schedule()))
        self.show()

    def clear_layout(self):
        """Clears the main layout so the same window can be used with
        updated information"""
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def create_new_schedule(self):
        """Wake-up time Menu"""
        self.clear_layout()
        self.display_logo()
        self.add_label("When would you like to start the day?", 1, 0)
        self.time_edit = QtWidgets.QTimeEdit()
        self.time_edit.setTime(QtCore.QTime(8, 0))
        self.grid.addWidget(self.time_edit, 2, 0, QtCore.Qt.AlignVCenter)
        self.add_button("Proceed", 2, 2, self.work_hours)
        self.add_button("Back", 2, 1, self.init_gui)
        self.show()

    def work_hours(self):

        self.clear_layout()
        # Update JSON with wake-up time
        with open(resource_path("timetable_data.json"), "r") as f:
            timetable_json = json.load(f)
        timetable_json["wake_up_time"] = self.time_edit.time().toString()
        with open(resource_path("timetable_data.json"), "w") as f:
            json.dump(timetable_json, f)

        self.display_logo()
        self.add_label("How many hours do you work each day?", 1, 0)
        self.add_label("Monday", 2, 0)
        self.add_label("Tuesday", 3, 0)
        self.add_label("Wednesday", 4, 0)
        self.add_label("Thursday", 5, 0)
        self.add_label("Friday", 6, 0)

        self.hours_worked_m = QtWidgets.QSpinBox()
        self.hours_worked_m.setRange(0, 8)
        self.hours_worked_m.setValue(4)
        self.hours_worked_tu = QtWidgets.QSpinBox()
        self.hours_worked_tu.setRange(0, 8)
        self.hours_worked_tu.setValue(4)
        self.hours_worked_w = QtWidgets.QSpinBox()
        self.hours_worked_w.setRange(0, 8)
        self.hours_worked_w.setValue(4)
        self.hours_worked_th = QtWidgets.QSpinBox()
        self.hours_worked_th.setRange(0, 8)
        self.hours_worked_th.setValue(4)
        self.hours_worked_f = QtWidgets.QSpinBox()
        self.hours_worked_f.setRange(0, 8)
        self.hours_worked_f.setValue(4)

        self.w_hours = [
            self.hours_worked_m, self.hours_worked_tu,
            self.hours_worked_w, self.hours_worked_th,
            self.hours_worked_f
        ]
        for i in range(2, 7):
            self.grid.addWidget(self.w_hours[i - 2], i, 2, QtCore.Qt.AlignVCenter)

        self.add_button("Proceed", 7, 5, self.university_course_input)
        self.add_button("Back", 7, 4, self.create_new_schedule)
        self.show()

    def university_course_input(self):
        # Update JSON with hours worked each day
        with open(resource_path("timetable_data.json"), "r") as f:
            timetable_json = json.load(f)
        hours = [x.value() for x in self.w_hours]
        i = 0
        for day in timetable_json["hours_worked_weekly"].keys():
            timetable_json["hours_worked_weekly"][day] = hours[i]
            time_str = timetable_json["wake_up_time"]
            time = QtCore.QTime.fromString(time_str, "HH:mm:ss").addSecs(3600)
            time_str = time.toString()
            timetable_json["start_work_hours_weekly"][day] = time_str
            i += 1
        with open(resource_path("timetable_data.json"), "w") as f:
            json.dump(timetable_json, f)

        self.clear_layout()

        self.display_logo()
        self.add_label("Please input class names, respective ECTS and perceived difficulty ranking from 1 to 10.", 1, 0)

        self.courses = []
        self.ects = []
        self.ranking = []

        for row in range(2, 8):
            label, ects, ranking = self.add_course_inputs(row, True)
            self.courses.append(label)
            self.ects.append(ects)
            self.ranking.append(ranking)

        self.add_button("Proceed", 8, 4, self.previous_courses)
        self.show()

    def previous_courses(self):
        """Handles saving previous semester's course information and updating the JSON file."""
        # Get previous data
        for row in range(0, 6):
            self.courses[row] = self.courses[row].text()
            self.ects[row] = self.ects[row].text()
            self.ranking[row] = self.ranking[row].text()

        # Update JSON with the semester data
        with open(resource_path("timetable_data.json"), "r") as f:
            timetable_json = json.load(f)
        semester_courses = timetable_json["semester_courses"]
        for i in range(6):
            semester_courses[i]["course_name"] = self.courses[i]
            semester_courses[i]["ECTS"] = int(self.ects[i])
            semester_courses[i]["personal_ranking"] = self.ranking[i]
        timetable_json["semester_courses"] = semester_courses
        with open(resource_path("timetable_data.json"), "w") as f:
            json.dump(timetable_json, f)

        # Load the input interface for previous courses
        self.clear_layout()

        self.display_logo()
        self.add_label("Please input 5 previous courses, their ECTS, and your grade", 1, 0)

        self.courses = []
        self.ects = []
        self.grades = []
        for row in range(2, 7):
            label, ects, grade = self.add_course_inputs(row, False)
            self.courses.append(label)
            self.ects.append(ects)
            self.grades.append(grade)

        self.add_button("Proceed", 7, 4, self.create_new_schedule_timetable)

        self.show()

    def save_schedule(self):
        """Opens a dialog to save the timetable as a JSON file."""
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Timetable", "",
                                                            "JSON Files (*.json);;All Files (*)", options=options)
        if filename:
            with open(resource_path("timetable_data.json"), "r") as f:
                timetable_json = json.load(f)
            with open(filename + ".json", "w") as f:
                json.dump(timetable_json, f)
            QtWidgets.QMessageBox.information(self, "Success", "Timetable saved successfully.")

    def display_schedule(self, path: str):
        """Displays the saved schedule from the given JSON file path."""
        with open(path, "r") as f:
            timetable_json = json.load(f)
        wake_up_time = QtCore.QTime.fromString(timetable_json["wake_up_time"], "hh:mm:ss")

        self.clear_layout()

        # Create the timetable layout   
        days = ["monday", "tuesday", "wednesday", "thursday", "friday"]

        for i in range(1, 12):
            self.add_label(wake_up_time.toString("HH:mm"), i, 0)
            wake_up_time = wake_up_time.addSecs(3600)  # Add one hour per row

        end_of_work = []
        for j, day in enumerate(days, start=1):
            self.add_label(day.capitalize(), 0, j)  # Day labels

            start_work_time = QtCore.QTime.fromString(timetable_json["start_work_hours_weekly"][day], "HH:mm:ss")
            hours_worked = timetable_json["hours_worked_weekly"][day]
            row_index = 0  # Initialization for safe assignment
            # Populate work hours
            for k in range(hours_worked):
                work_time_slot = start_work_time.addSecs(k * 3600)  # Add each hour
                row_index = work_time_slot.hour() - int(
                    timetable_json["wake_up_time"].split(":")[0]) + 1  # Row index for the time
                self.add_label("Work", row_index, j, "background-color: #B4D6CD;")
            end_of_work.append(row_index)

        # Add end of work for weekend (starting first thing in the morning)
        end_of_work.append(1)
        end_of_work.append(1)
        self.add_label("Saturday", 0, 6)
        self.add_label("Sunday", 0, 7)

        # Schedule study sessions after the break
        study_courses = timetable_json["semester_courses"]
        i = 1  # Start on Monday
        k = 0
        colors_iterator = 0
        colors = ["#FFDA76", "#FF8C9E", "#FF4E88", "#E9FF97", "#C3FF93", "#FFDB5C"]
        for course in study_courses:
            allocated_time = course["allocated_study_hours"]
            remaining_time = 0
            if i in [6, 7]:  # For weekends
                slot = 2
            else:
                slot = end_of_work[k] + 2
            while remaining_time < allocated_time:
                if slot > 11:
                    i += 1
                    k += 1
                    slot = end_of_work[k] + 2
                self.add_label(course["course_name"], slot, i, "background-color:" + colors[colors_iterator] + ";")
                remaining_time += 1
                slot += 1
            # Move to the next day to avoid mixing subjects each day
            i += 1
            k += 1
            colors_iterator += 1
        self.add_button("View graph", 12, 7, lambda: show_time_distribution(path))
        self.add_button("Save timetable", 12, 6, self.save_schedule)
        self.add_button("Back", 0, 0, self.init_gui)
        self.show()

    def create_new_schedule_timetable(self):
        """Saves previous course performance and generates a new optimized schedule."""
        performance_json = []
        for row in range(0, 5):
            ects = self.ects[row].text()
            performance_json.append(
                {"course_name": self.courses[row].text(), "ECTS": int(ects), "grade": float(self.grades[row].text())})

        with open(previous_performance_path, "w") as f:
            json.dump(performance_json, f)

        create_course_optimized_schedule()

        self.display_schedule(resource_path("timetable_data.json"))

    def display_old_schedule(self):
        """Loads and displays an old schedule from the provided JSON file path."""
        path = self.path_to_json.text()
        self.display_schedule(path)

    def view_old_schedule(self):
        """Prompts the user to input a JSON file path and then displays the old schedule."""
        self.clear_layout()

        self.display_logo()
        self.add_label(
            "Please input the path to the .JSON file automatically created after you've saved your timetable.", 1, 0)
        self.add_label("PATH:", 2, 0)
        self.path_to_json = self.add_line_edit(resource_path("timetable_data.json"), 3, 0)
        self.path_to_json.setFixedWidth(500)
        self.add_button("View", 3, 2, self.display_old_schedule)
        self.add_button("Back", 3, 1, self.init_gui)
        self.show()

    def error_message(self):
        """Displays an error message for a missing JSON file."""
        self.dark_mode_flag = self.detect_dark_mode_gnome()
        if self.dark_mode_flag:
            self.setStyleSheet(open(resource_path("night_theme.css")).read())
        else:
            self.setStyleSheet(open(resource_path("light_theme.css")).read())

        alert = QtWidgets.QMessageBox()
        alert.setWindowTitle("Oops!")
        alert.setText("The file doesn't exist.")
        alert.exec_()


app = QtWidgets.QApplication([])
window = Gui()
app.exec_()
