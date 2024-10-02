from math import ceil
from operator import itemgetter
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import json, subprocess, os, greedyAlgorithm


class Gui(QtWidgets.QWidget):
    '''Optimal Scheduler GUI Main Page'''

    def __init__(self):
        super().__init__()
        self.initGui()


    def detectDarkModeGnome(self):
        '''Detects dark mode in GNOME'''
        if not hasattr(self, '_darkModeDetected'):
            getArgs = ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme']
            currentTheme = subprocess.run(getArgs, capture_output=True).stdout.decode("utf-8").strip().strip("'")
            darkIndicator = '-dark'
            self._darkModeDetected = currentTheme.endswith(darkIndicator)
        return self._darkModeDetected

    def displayLogo(self):
        '''Displays logo on grid'''
        self.logo = QtWidgets.QLabel()
        if self.darkModeFlag:
            self.pixmap = QPixmap('logoDark.png')
        else:
            self.pixmap = QPixmap('logoLight.png')
        self.logo.setPixmap(self.pixmap)
        self.grid.addWidget(self.logo, 0, 0)


    def add_label(self, text: str, row: int, col: int, style=""):
        '''Adds Qlabel on grid'''
        label = QtWidgets.QLabel(text)
        label.setWordWrap(True)
        if style != "":
            label.setStyleSheet(style)
        self.grid.addWidget(label, row, col)


    def add_lineEdit(self, text: str, row: int, col: int):
        '''Adds QLineEdit on grid'''
        lineEdit = QtWidgets.QLineEdit(text)
        self.grid.addWidget(lineEdit, row, col)
        return lineEdit
    

    def add_button(self, text: str, row: int, col: int, func):
        '''Adds QPushButton on grid'''
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(func)
        self.grid.addWidget(button, row, col)


    def add_course_inputs(self, row: int, rankingGradeFlag: bool):
        '''Adds course inputs on grid to get user data on current
        semester courses, ECTS and perceived difficulty ranking when 
        rankingGradeFlag = True and previous courses, ECTS and previous
        grades inputs when rankingGradeFlag = False'''
        label = self.add_lineEdit(f"Course {row-1}", row, 0)
        ects = self.add_lineEdit("5 ECTS", row, 1)
        if rankingGradeFlag:
            ranking = self.add_lineEdit("1", row, 2)
            return label, ects, ranking
        else:
            grade = self.add_lineEdit("5.00", row, 3)
            return label, ects, grade
    
    def get_default_schedule(self):
        '''Creates default timetableData JSON when new template creation
        is requested'''
        return {
            "wakeUpTime": "08:00:00",
            "hoursWorkedWeekly": {
                "monday": 4, "tuesday": 4, "wednesday": 4,
                "thursday": 4, "friday": 4
            },
            "startWorkHoursWeekly": {
                "monday": 9, "tuesday": 9, "wednesday": 9,
                "thursday": 9, "friday": 9
            },
            "semesterCourses": [
                {"courseName": f"Course {i+1}", "ECTS": "5 ECTS", "group": "", 
                "personalRanking": "1", "ranking": 0} for i in range(6)
            ]
        }

    def initGui(self):
        #appearance
        self.setGeometry(200,200,500,500)
        self.setWindowTitle("Optimal Scheduler")
        self.darkModeFlag = self.detectDarkModeGnome()
        theme = 'nightTheme.css' if self.darkModeFlag else 'dayTheme.css'
        self.setStyleSheet(open(theme).read())
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(10)

        self.displayLogo()

        #opening line and buttons
        self.add_label("Welcome! What would you like to do today?", 1, 0)
        self.add_button("Create new weekly schedule", 2, 0, self.createNewSchedule)

        self.add_button("Open existing schedule", 3, 0, self.viewOldSchedule)
        
        #creates template JSON file for new weekly timetable if it doesn't exist
        if not os.path.exists("timetableData.json"):
            with open("timetableData.json", "w") as f:
                f.write(json.dumps(self.get_default_schedule()))
        self.show()
    


    def clearLayout(self):
        '''Clears main layout so the same window can be used with 
        updated information'''
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def createNewSchedule(self):
        '''Wake up time Menu'''
        self.clearLayout()
        
        self.displayLogo()
        self.add_label("When would you like to start the day?", 1, 0)
        self.time_edit = QtWidgets.QTimeEdit()
        self.time_edit.setTime(QtCore.QTime(8, 0))
        self.grid.addWidget(self.time_edit, 2, 0, QtCore.Qt.AlignVCenter)
        self.add_button("Proceed", 2, 1, self.workHours)

        self.show()


    def workHours(self):
        #update JSON with wake up time
        with open("timetableData.json", "r") as f:
            timetableJSON = json.load(f)
        timetableJSON["wakeUpTime"] = self.time_edit.time().toString()
        with open("timetableData.json", "w") as f:
            json.dump(timetableJSON, f)

        self.clearLayout()

        self.displayLogo()
        self.add_label("How many hours do you work each day?", 1, 0)
        self.add_label("Monday", 2, 0)
        #self.flexible1 = QtWidgets.QCheckBox("Flexible")
        #self.grid.addWidget(self.flexible1, 2, 3)
        self.add_label("Tuesday", 3, 0)
        #self.flexible2 = QtWidgets.QCheckBox("Flexible")
        #self.grid.addWidget(self.flexible2, 3, 3)
        self.add_label("Wednesday", 4, 0)
        #self.flexible3 = QtWidgets.QCheckBox("Flexible")
        #self.grid.addWidget(self.flexible3, 4, 3)
        self.add_label("Thursday", 5, 0)
        #self.flexible4 = QtWidgets.QCheckBox("Flexible")
        #self.grid.addWidget(self.flexible4, 5, 3)
        self.add_label("Friday", 6, 0)
        #self.flexible5 = QtWidgets.QCheckBox("Flexible")
        #self.grid.addWidget(self.flexible5, 6, 3)

        #spin boxes for hours each day
        self.hoursWorkedM = QtWidgets.QSpinBox()
        self.hoursWorkedM.setRange(0,8)
        self.hoursWorkedM.setValue(4)
        self.hoursWorkedTu = QtWidgets.QSpinBox()
        self.hoursWorkedTu.setRange(0,8)
        self.hoursWorkedTu.setValue(4) 
        self.hoursWorkedW = QtWidgets.QSpinBox()
        self.hoursWorkedW.setRange(0,8)
        self.hoursWorkedW.setValue(4)
        self.hoursWorkedTh = QtWidgets.QSpinBox()
        self.hoursWorkedTh.setRange(0,8)
        self.hoursWorkedTh.setValue(4)
        self.hoursWorkedF = QtWidgets.QSpinBox()
        self.hoursWorkedF.setRange(0,8)
        self.hoursWorkedF.setValue(4)
        self.wHours = [self.hoursWorkedM, self.hoursWorkedTu, self.hoursWorkedW, self.hoursWorkedTh, self.hoursWorkedF]
        for i in range(2, 7):
            self.grid.addWidget(self.wHours[i-2], i, 2, QtCore.Qt.AlignVCenter)

        #save button
        self.buttonProcced = self.add_button("Proceed", 7, 3, self.universityCourseInput)

        self.show()


    def universityCourseInput(self):
        #update JSON with hours worked each day, and flexibility schedule
        with open("timetableData.json", "r") as f:
            timetableJSON = json.load(f)
        hours = [x.value() for x in self.wHours]
        i = 0
        for day in timetableJSON["hoursWorkedWeekly"].keys():
            #creates QTime object to calculate start work hours each day, 1 hour later after waking up
            timetableJSON["hoursWorkedWeekly"][day] = hours[i]
            time_str = timetableJSON["wakeUpTime"]
            time = QtCore.QTime.fromString(time_str, "HH:mm:ss").addSecs(3600)
            time_str = time.toString()
            timetableJSON["startWorkHoursWeekly"][day] = time_str
            i += 1
        with open("timetableData.json", "w") as f:
            json.dump(timetableJSON, f)
        #self.flexible = [self.flexible1.isChecked(), self.flexible2.isChecked(), self.flexible3.isChecked(), self.flexible4.isChecked(), self.flexible5.isChecked()]

        self.clearLayout()

        self.displayLogo()
        self.add_label("Please input class names, respective ECTS and perceived difficulty ranking from 1 to 10.", 1, 0)

        self.courses = []
        self.ects = []
        self.ranking = []

        for row in range(2, 8):
            label, ects, ranking = self.add_course_inputs(row, True)
            self.courses.append(label)
            self.ects.append(ects)
            self.ranking.append(ranking)

        self.add_button("Proceed", 8, 2, self.previousCourses)

        self.show()


    def previousCourses(self):
        #get previous data
        for row in range(0, 6):
            self.courses[row] = self.courses[row].text()
            self.ects[row] = self.ects[row].text()
            self.ranking[row] = self.ranking[row].text()

        #update JSON with semester
        with open("timetableData.json", "r") as f:
            timetableJSON = json.load(f)
        semesterCourses= timetableJSON["semesterCourses"]
        for i in range(6):
            semesterCourses[i]["courseName"] = self.courses[i]
            semesterCourses[i]["ECTS"] = int(self.ects[i][0])
            semesterCourses[i]["personalRanking"] = self.ranking[i]
        timetableJSON["semesterCourses"] = semesterCourses
        with open("timetableData.json", "w") as f:
            json.dump(timetableJSON, f)
        
        #get previous courses data
        self.clearLayout()

        self.displayLogo()
        self.add_label("Please input 5 previous courses, their ECTS and your grade", 1, 0)
        
        self.courses = []
        self.ects = []
        self.grades = []
        for row in range(2, 7):
            label, ects, grade = self.add_course_inputs(row, False)
            self.courses.append(label)
            self.ects.append(ects)
            self.grades.append(grade)

        self.add_button("Proceed", 7, 3, self.createNewScheduleTimetable)

        self.show()

    def displaySchedule(self, path: str):
        with open(path, "r") as f:
            timetableJSON = json.load(f)
        wake_up_time = QtCore.QTime.fromString(timetableJSON["wakeUpTime"], "hh:mm:ss")

        self.clearLayout()

        # Create the timetable layout   
        days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
        
        for i in range(1, 12):
            self.add_label(wake_up_time.toString("HH:mm"), i, 0)
            wake_up_time = wake_up_time.addSecs(3600)  # add one hour per row
        endOfWork = []
        for j, day in enumerate(days, start=1):
            self.add_label(day.capitalize(), 0, j)  # Day labels

            start_work_time = QtCore.QTime.fromString(timetableJSON["startWorkHoursWeekly"][day], "HH:mm:ss")
            hours_worked = timetableJSON["hoursWorkedWeekly"][day]

            # Populate work hours
            for k in range(hours_worked):
                work_time_slot = start_work_time.addSecs(k * 3600)  # Add each hour
                row_index = work_time_slot.hour() - int(timetableJSON["wakeUpTime"].split(":")[0]) + 1  # Row index for the time
                self.add_label("Work", row_index, j, "background-color: #B4D6CD;")
            endOfWork.append(row_index)
        self.add_label("Saturday",0, 6)
        self.add_label("Sunday", 0, 7)
        # Add 1-hour break after work

        # Schedule study sessions after the break
        study_courses = timetableJSON["semesterCourses"]
        i = 1 #start on monday
        k = 0
        l = 0
        colors = ["#FFDA76", "#FF8C9E", "#FF4E88", "#E9FF97", "#C3FF93", "#FFDB5C"]
        for course in study_courses:
            allocated_time = course["allocatedStudyHours"]
            remainingTime = 0
            if i in [6, 7]:
                slot = 2
            else: 
                slot = endOfWork[k]+2
            while (remainingTime < allocated_time):
                if slot > 11:
                    i+= 1
                    slot = endOfWork[k] + 2
                self.add_label(course["courseName"], slot, i, "background-color:"+colors[l]+";")
                remainingTime += 1
                slot += 1
            #switch to next day
            i += 1 
            k = 0
            l+=1

        self.show()

    def createNewScheduleTimetable(self):
        '''Displays weekly timetable from time of wake up'''
        #creates JSON with previous course performance
        performanceJSON = []
        for row in range(0, 5):
            performanceJSON.append({"courseName" : self.courses[row].text(), "ECTS" : int(self.ects[row].text()[0]), "grade" : float(self.grades[row].text())})

        with open("previousPerformance.json", "w") as f:
            json.dump(performanceJSON, f)
        self.createCourseOptimizedSchedule()
        with open("timetableData.json", "r") as f:
            timetableJSON = json.load(f)
        wake_up_time = QtCore.QTime.fromString(timetableJSON["wakeUpTime"], "hh:mm:ss")

        self.clearLayout()

        # Create the timetable layout   
        self.displaySchedule("timetableData.json")
        self.show()

    def displayOldSchedule(self):
        path = self.pathToJSON.text()
        self.displaySchedule(path)

    def viewOldSchedule(self):
        '''asks for JSON file and calls displayTimetable'''
        self.clearLayout()

        self.displayLogo()
        self.add_label("Please input the path to the .JSON file automatically created after you've saved your timetable.", 1, 0)
        self.add_label("PATH:", 2, 0)
        self.pathToJSON = self.add_lineEdit("timetableData.json", 3, 0)
        self.pathToJSON.setFixedWidth(500)
        self.add_button("View", 3, 1, self.displayOldSchedule)
        self.show()


    def createCourseOptimizedSchedule(self):
        with open("timetableData.json", "r") as f:
            timetableJSON = json.load(f)

        # Allocate study time using the greedy algorithm
        allocated_courses = greedyAlgorithm.allocateStudyTime(timetableJSON)
        return allocated_courses

    #Error message for viewing old schedules
    def errorMessage(self):
        '''Error alert for missing JSON file for timetable'''
        self.darkModeFlag = self.detectDarkModeGnome()
        if  self.darkModeFlag:
            self.setStyleSheet(open('nightTheme.css').read())
        else:
            self.setStyleSheet(open('dayTheme.css').read())
        alert = QtWidgets.QMessageBox()
        alert.setWindowTitle("Oops!")
        alert.setText("The file doesn't exist.") 
        alert.exec_() 

app = QtWidgets.QApplication([]) 
widow = Gui()   
app.exec_()
