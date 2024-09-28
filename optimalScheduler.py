from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import json


class Gui(QtWidgets.QWidget):
    '''Optimal Scheduler GUI Main Page'''
    def __init__(self):
        super().__init__()
        self.initGui()

    def displayLogo(self):
        self.logo = QtWidgets.QLabel()
        self.pixmap = QPixmap('logo.png')
        self.logo.setPixmap(self.pixmap)
        self.grid.addWidget(self.logo, 0, 0)
    
    def initGui(self):
        #appearance
        self.setGeometry(200,200,500,500)
        self.setWindowTitle("Optimal Scheduler")
        self.setStyleSheet("background-color: black; color: white; font-size: 20px;") 
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.grid.setSpacing(5)

        self.displayLogo()

        #opening line and buttons
        self.openingText = QtWidgets.QLabel("Welcome! What would you like to do today?")
        self.grid.addWidget(self.openingText, 1, 0)

        self.buttonCreateNewSchedule = QtWidgets.QPushButton("Create new weekly schedule")
        self.grid.addWidget(self.buttonCreateNewSchedule, 2, 0)
        self.buttonCreateNewSchedule.clicked.connect(self.createNewSchedule)

        self.buttonViewOldSchedule = QtWidgets.QPushButton("Open existing schedule")
        self.grid.addWidget(self.buttonViewOldSchedule, 3, 0)
        self.buttonViewOldSchedule.clicked.connect(self.viewOldSchedule)
        
        #creates template JSON file for new weekly timetable if it doesn't exist
        try: 
            f = open("timetableData.json", "r")
            f.close()
        except:
            f = open("timeTableData.json", "w")
            f.write("{\"wakeUpTime\": \"08:00:00\", \"hoursWorkedWeekly\": {\"monday\": 4, \"tuesday\": 4, \"wednesday\": 4, \"thursday\": 4, \"friday\": 4}, \"startWorkHoursWeekly\": {\"monday\": 9, \"tuesday\": 9, \"wednesday\": 9, \"thursday\": 9, \"friday\": 9}, \"semesterCourses\": [{\"courseName\": \"Course 1\", \"ECTS\": \"5 ECTS\", \"group\": \"\", \"personalRanking\": \"1\", \"ranking\": 0}, {\"courseName\": \"Course 2\", \"ECTS\": \"5 ECTS\", \"group\": \"\", \"personalRanking\": \"1\", \"ranking\": 0}, {\"courseName\": \"Course 3\", \"ECTS\": \"5 ECTS\", \"group\": \"\", \"personalRanking\": \"1\", \"ranking\": 0}, {\"courseName\": \"Course 4\", \"ECTS\": \"5 ECTS\", \"group\": \"\", \"personalRanking\": \"1\", \"ranking\": 0}, {\"courseName\": \"Course 5\", \"ECTS\": \"5 ECTS\", \"group\": \"\", \"personalRanking\": \"1\", \"ranking\": 0}, {\"courseName\": \"Course 6\", \"ECTS\": \"5 ECTS\", \"group\": \"\", \"personalRanking\": \"1\", \"ranking\": 0}]}")
            f.close()
        self.show()

    def saveIntoTimetable(self):
        '''Saves user inputed data into timetableData.json'''
        return
    
    def displayTimetable(self):
        '''Displays new timetable visually from timetableData.json'''
        try:
            f = open(self.pathToJSON, "r")
        except:
            self.errorMessage()

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

        self.wakeUpLabel = QtWidgets.QLabel("When would you like to start the day?")
        self.time_edit = QtWidgets.QTimeEdit()
        self.time_edit.setTime(QtCore.QTime(8, 0))

        self.grid.addWidget(self.wakeUpLabel, 1, 0)
        self.grid.addWidget(self.time_edit, 2, 0, QtCore.Qt.AlignVCenter)

        self.buttonSaveWakeUp = QtWidgets.QPushButton("Proceed")
        self.grid.addWidget(self.buttonSaveWakeUp, 2, 1, QtCore.Qt.AlignVCenter)
        self.buttonSaveWakeUp.clicked.connect(self.workHours)

        self.show()

    def workHours(self):
        #update JSON with wake up time
        f = open("timetableData.json", "r")
        timetableJSON = json.load(f)
        f.close()
        timetableJSON["wakeUpTime"] = self.time_edit.time().toString()
        f = open("timetableData.json", "w")
        json.dump(timetableJSON, f)
        f.close()

        self.clearLayout()

        self.displayLogo()

        self.label = QtWidgets.QLabel("How many hours do you work each day?")
        self.grid.addWidget(self.label, 1, 0)
        self.monday = QtWidgets.QLabel("Monday")
        self.grid.addWidget(self.monday, 1, 1)
        self.tuesday = QtWidgets.QLabel("Tuesday")
        self.grid.addWidget(self.tuesday, 1, 2)
        self.wednesday = QtWidgets.QLabel("Wednesday")
        self.grid.addWidget(self.wednesday, 1, 3)
        self.thursday = QtWidgets.QLabel("Thursday")
        self.grid.addWidget(self.thursday, 1, 4)
        self.friday = QtWidgets.QLabel("Friday")
        self.grid.addWidget(self.friday, 1, 5)

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
        for i in range(5):
            self.grid.addWidget(self.wHours[i], 2, 1+i, QtCore.Qt.AlignVCenter)

        #save button
        self.buttonProcced = QtWidgets.QPushButton("Proceed")
        self.buttonProcced.clicked.connect(self.universityCourseInput)
        self.grid.addWidget(self.buttonProcced, 2, 7)

        self.show()

    def universityCourseInput(self):
        #update JSON with hours worked each day
        f = open("timetableData.json", "r")
        timetableJSON = json.load(f)
        f.close()
        hours = [x.value() for x in self.wHours]
        i = 0
        for day in timetableJSON["hoursWorkedWeekly"].keys():
            timetableJSON["hoursWorkedWeekly"][day] = hours[i]
            i += 1
        f = open("timetableData.json", "w")
        json.dump(timetableJSON, f)
        f.close()

        self.clearLayout()

        self.displayLogo()
        self.label = QtWidgets.QLabel("Please input class names, respective ECTS and perceived difficulty ranking from 1 to 10.")
        self.label.setWordWrap(True)  
        self.grid.addWidget(self.label, 1, 0)

        self.courses = []
        self.ects = []
        self.ranking = []

        self.label1 = QtWidgets.QLineEdit("Course 1")
        self.grid.addWidget(self.label1, 2, 0)
        self.ects1 = QtWidgets.QLineEdit("5 ECTS")
        self.grid.addWidget(self.ects1, 2, 1)
        self.ranking1 = QtWidgets.QLineEdit("1")
        self.grid.addWidget(self.ranking1, 2, 2)

        self.label2 = QtWidgets.QLineEdit("Course 2")
        self.grid.addWidget(self.label2, 3, 0)
        self.ects2 = QtWidgets.QLineEdit("5 ECTS")
        self.grid.addWidget(self.ects2, 3, 1)
        self.ranking2 = QtWidgets.QLineEdit("1")
        self.grid.addWidget(self.ranking2, 3, 2)

        self.label3 = QtWidgets.QLineEdit("Course 3")
        self.grid.addWidget(self.label3, 4, 0)
        self.ects3 = QtWidgets.QLineEdit("5 ECTS")
        self.ranking3 = QtWidgets.QLineEdit("1")
        self.grid.addWidget(self.ranking3, 4, 2)
        self.grid.addWidget(self.ects3, 4, 1)

        self.label4 = QtWidgets.QLineEdit("Course 4")
        self.ranking4 = QtWidgets.QLineEdit("1")
        self.grid.addWidget(self.ranking4, 5, 2)
        self.grid.addWidget(self.label4, 5, 0)
        self.ects4 = QtWidgets.QLineEdit("5 ECTS")
        self.grid.addWidget(self.ects4, 5, 1)

        self.label5 = QtWidgets.QLineEdit("Course 5")
        self.grid.addWidget(self.label5, 6, 0)
        self.ects5 = QtWidgets.QLineEdit("5 ECTS")
        self.grid.addWidget(self.ects5, 6, 1)
        self.ranking5 = QtWidgets.QLineEdit("1")
        self.grid.addWidget(self.ranking5, 6, 2)

        self.label6 = QtWidgets.QLineEdit("Course 6")
        self.grid.addWidget(self.label6, 7, 0)
        self.ects6 = QtWidgets.QLineEdit("5 ECTS")
        self.grid.addWidget(self.ects6, 7, 1)
        self.ranking6 = QtWidgets.QLineEdit("1")
        self.grid.addWidget(self.ranking6, 7, 2)

        self.button = QtWidgets.QPushButton("Proceed")
        self.button.clicked.connect(self.previousCourses)
        self.grid.addWidget(self.button, 8, 2)

        self.show()

    def previousCourses(self):
        #get previous data
        self.courses.append(self.label1.text())
        self.ects.append(self.ects1.text())
        self.ranking.append(self.ranking1.text())
        self.courses.append(self.label2.text())
        self.ects.append(self.ects2.text())
        self.ranking.append(self.ranking2.text())
        self.courses.append(self.label3.text())
        self.ects.append(self.ects3.text())
        self.ranking.append(self.ranking3.text())
        self.courses.append(self.label4.text())
        self.ects.append(self.ects4.text())
        self.ranking.append(self.ranking4.text())
        self.courses.append(self.label5.text())
        self.ects.append(self.ects5.text())
        self.ranking.append(self.ranking5.text())
        self.courses.append(self.label6.text())
        self.ects.append(self.ects6.text())
        self.ranking.append(self.ranking6.text())
         #update JSON with semester
        f = open("timetableData.json", "r")
        timetableJSON = json.load(f)
        f.close()
        semesterCourses= timetableJSON["semesterCourses"]
        for i in range(6):
            semesterCourses[i]["courseName"] = self.courses[i]
            semesterCourses[i]["ECTS"] = self.ects[i]
            semesterCourses[i]["personalRanking"] = self.ranking[i]
        timetableJSON["semesterCourses"] = semesterCourses
        f = open("timetableData.json", "w")
        json.dump(timetableJSON, f)
        f.close()
        
        #get previous courses data
        self.clearLayout()
        self.label = QtWidgets.QLabel("Please input previous courses and your grade")
        self.grid.addWidget(self.label)
        self.show()


    def createNewScheduleTimetable(self):
        '''Displays weekly timetable from time of wake up'''
        #updates JSON with hours worked every day

        self.clearLayout()
        displayTime = self.time_edit.time()
        self.grid.addWidget(QtWidgets.QLabel(""), 0, 0)
        for i in range(1,12):
            self.grid.addWidget(QtWidgets.QLabel(displayTime.toString()), i, 0)
            displayTime = displayTime.addSecs(3600)
        self.monday = QtWidgets.QLabel("Monday")
        self.grid.addWidget(self.monday, 0, 1)
        self.tuesday = QtWidgets.QLabel("Tuesday")
        self.grid.addWidget(self.tuesday, 0, 2)
        self.wednesday = QtWidgets.QLabel("Wednesday")
        self.grid.addWidget(self.wednesday, 0, 3)
        self.thursday = QtWidgets.QLabel("Thursday")
        self.grid.addWidget(self.thursday, 0, 4)
        self.friday = QtWidgets.QLabel("Friday")
        self.grid.addWidget(self.friday, 0, 5)
        self.saturday = QtWidgets.QLabel("Saturday")
        self.grid.addWidget(self.saturday, 0, 6)
        self.sunday = QtWidgets.QLabel("Sunday")
        self.grid.addWidget(self.sunday, 0, 7)
        self.show()
    
    def viewOldSchedule(self):
        '''asks for JSON file and calls displayTimetable'''
        self.clearLayout()
        self.logo = QtWidgets.QLabel()
        self.pixmap = QPixmap('logo.png')
        self.logo.setPixmap(self.pixmap)
        self.grid.addWidget(self.logo, 0, 0)
        self.label1 = QtWidgets.QLabel("Please input the path to the .JSON file automatically created after you've saved your timetable.")
        self.grid.addWidget(self.label1, 1, 0)
        self.label2 = QtWidgets.QLabel("PATH:")
        self.grid.addWidget(self.label2, 2, 0)
        self.pathToJSON = QtWidgets.QLineEdit()
        self.pathToJSON.setFixedWidth(500)
        self.grid.addWidget(self.pathToJSON, 3, 0)
        self.viewButton = QtWidgets.QPushButton("View")
        self.viewButton.clicked.connect(self.displayTimetable)
        self.grid.addWidget(self.viewButton, 3, 1)
        self.show()


    def errorMessage(self):
        '''Error alert for missing JSON file for timetable'''
        alert = QtWidgets.QMessageBox()
        alert.setWindowTitle("Oops!")
        alert.setText("The file doesn't exist.") 
        alert.exec_() 

app = QtWidgets.QApplication([]) 
widow = Gui()   
app.exec_()