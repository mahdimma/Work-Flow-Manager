import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QHBoxLayout, QScrollArea, QDateTimeEdit
from PyQt6.QtCore import Qt, QSize, QCalendar, QLocale, QDateTime, QDate, QTime
from PyQt6.QtGui import QPalette, QColor
import jdatetime
import locale

import copy

# Persian Date and Time Selector
class PersianDateTimeSelector(QDateTimeEdit):
    def __init__(self):
        super().__init__()
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy/MM/dd HH:mm")
        self.setDateTime(QDateTime.currentDateTime())
        jalali_calendar = QCalendar(QCalendar.System.Jalali)
        self.setCalendar(jalali_calendar)
        self.setLocale(QLocale(QLocale.Language.Persian))

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login Window')
        self.resize(QSize(300,300))
        self.centerize()
        
        layout = QVBoxLayout()

        self.label_username = QLabel('Username:', self)
        layout.addWidget(self.label_username)

        self.text_username = QLineEdit(self)
        layout.addWidget(self.text_username)

        self.label_password = QLabel('Password:', self)
        layout.addWidget(self.label_password)

        self.text_password = QLineEdit(self)
        self.text_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.text_password)

        self.button_login = QPushButton('Login', self)
        self.button_login.clicked.connect(self.handle_login)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def handle_login(self):
        username = self.text_username.text()
        password = self.text_password.text()
        self.loginResault = self.loginCheck(username, password)
        
        if self.loginResault["correct"] is True:
            if self.loginResault["type"] == 1: # employee
                QMessageBox.information(self, 'Success', 'Login successful!')
                self.EmployeeWindow = EmployeeWindow(self.loginResault["ID"])
                self.hide()
                self.EmployeeWindow.show()
            elif self.loginResault["type"] == 2: # manager
                pass
            else: # supervisor
                pass
        else:
            QMessageBox.warning(self, 'Error', 'Login failed!')
            
    def centerize(self):
        # Get screen geometry and window geometry
        screen_rect = QApplication.primaryScreen().geometry()
        window_rect = self.geometry()

        # Calculate center coordinates
        center_x = (screen_rect.center().x() - window_rect.width() // 2)
        center_y = (screen_rect.center().y() - window_rect.height() // 2)

        # Move the window to the center
        self.move(center_x, center_y)
        print(self.geometry())
    
    def loginCheck(self, username, password) -> dict:
        #return dict {"correct": (False|True), "type": (1(Employee) | 2(manager) | 3(supervisor)), "ID": id_number}
        pass

class EmployeeWindow(QMainWindow):
    def __init__(self, employeeID):
        self.employeeID = employeeID
        print(self.employeeID)
        super().__init__()
        self.setWindowTitle("کارمند")
        
        #get information of employee
        self.employeeInformation = self.getEmployeeInformation(self.employeeID)

        # Main widget and layout
        self.main_widget = QWidget(self)
        self.main_widget.setMinimumSize(QSize(700,400))
        self.setCentralWidget(self.main_widget)
        self.layoutMain = QVBoxLayout(self.main_widget)

        #layout information
        self.layoutUp = QHBoxLayout()
        
        # button of up (add task and show score)
        self.layoutBtnTaskAndScor = QVBoxLayout()
        self.addWorkBtn = QPushButton("اضافه کردن کار")
        self.addWorkBtn.clicked.connect(self.addWork)
        self.layoutBtnTaskAndScor.addWidget(self.addWorkBtn)
        self.showScoreBtn = QPushButton("نشان دادن نمره")
        self.showScoreBtn.clicked.connect(self.showScore)
        self.layoutBtnTaskAndScor.addWidget(self.showScoreBtn)
        self.layoutUp.addLayout(self.layoutBtnTaskAndScor)
        
        self.layoutUp.addWidget(QLabel(str(), self))
        
        
        #date show
        locale.setlocale(locale.LC_ALL, jdatetime.FA_LOCALE)
        self.layoutUp.addWidget(QLabel(str(jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S')), self))
        #type of work
        self.layoutUp.addWidget(QLabel(self.employeeInformation['workType'], self))
        
        # name widget to display name
        self.layoutName = QVBoxLayout()
        self.fNameLabel = QLabel(self.employeeInformation['fName'], self)
        self.layoutName.addWidget(self.fNameLabel)
        self.lNameLabel = QLabel(self.employeeInformation['lName'], self)
        self.layoutName.addWidget(self.lNameLabel)
        self.layoutUp.addLayout(self.layoutName)
        
        # Employee ID
        self.employeeIdLabel = QLabel(f"شماره کارمند: {self.employeeID}", self)
        self.layoutUp.addWidget(self.employeeIdLabel)
        
        #works layout
        self.scrollPart = QScrollArea()
        self.scrollPart.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollPart.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollPart.setWidgetResizable(True)
        
        #work layout config
        self.insertWorks()
        
        #main layout config
        self.layoutMain.addLayout(self.layoutUp)
        self.layoutMain.addWidget(self.scrollPart)
    
    def insertWorks(self):
        self.layoutWorks = QVBoxLayout()
        self.layoutWorks.addWidget(QLabel("my baby my baby"))
        self.widgetWorks = QWidget()
        
        # implemente of add works (sql)
        
        self.widgetWorks.setLayout(self.layoutWorks)
        self.scrollPart.setWidget(self.widgetWorks)
        pass # with sql
    
    def addWork(self):
        self.addWorkWindow = AddWorkWindow(self)
        self.addWorkWindow.show()
        pass
        
    def showScore(self):
        self.showScoreWindow = ShowScoreWindow(self.employeeID)
        self.showScoreWindow.show()
    
    def editWork(self,workID):
        print(workID)
        self.editWorkWindow = EditWorkWindow(self,int(workID))
        self.editWorkWindow.show()
        pass
    
    def getEmployeeInformation(self, employeeId):
        return {"fName": "نام", "lName": "فامیلی", "workType": "نوع کار"}
        pass # with sql

class ShowScoreWindow(QMainWindow):
    def __init__(self, employeeID):
        self.employeeID = employeeID
        super().__init__()
        self.setWindowTitle(f"نمرات کارمند {self.employeeID}")
        self.resize(QSize(400,200))
        self.scoreInfo = self.getScoreInfo()
        
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)
        
        self.paletteBg = QPalette()
        self.paletteBg.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))
        self.mainWidget.setPalette(self.paletteBg)
        self.mainWidget.setAutoFillBackground(True)
        
        self.mainLayout.addWidget(QLabel(f"نمره سالانه: {self.scoreInfo["y"]}"))
        self.mainLayout.addWidget(QLabel(f"نمره ماهانه: {self.scoreInfo["m"]}"))
        self.mainLayout.addWidget(QLabel(f"نمره هفتگی: {self.scoreInfo["w"]}"))

        
    def getScoreInfo(self) -> dict:
        return {"w": 2.5, "m": 3.5, "y": 3.0}
        pass # with sql

#implement
class AddWorkWindow(QMainWindow):
    class PersianDateTimeSelectorStart(PersianDateTimeSelector):
        def __init__(self, eventHandler):
            super().__init__()
            self.dateTimeChanged.connect(eventHandler)
                        
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.setWindowTitle("اضافه کردن کار")
        self.resize(QSize(400,200))
        
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        
        # main layout
        self.mainLayout = QHBoxLayout(self.mainWidget)
        
        # ok button
        self.okBtn = QPushButton("تایید", self)
        self.okBtn.clicked.connect(self.insertInDatabase)
        self.mainLayout.addWidget(self.okBtn)
        
        # work date start and end
        self.workDateTimeLayout = QVBoxLayout()
        self.workDateTimeStartLabel = QLabel("تاریخ و ساعت شروع کار", self)
        self.dateTimeStartSelector = self.PersianDateTimeSelectorStart(self.minimumEndUpdate)
        self.workDateTimeEndLabel = QLabel("تاریخ و ساعت پایان کار", self)
        self.dateTimeEndSelector = PersianDateTimeSelector()
        self.dateTimeEndSelector.setMinimumDateTime(QDateTime.currentDateTime())
        self.workDateTimeLayout.addWidget(self.workDateTimeStartLabel)
        self.workDateTimeLayout.addWidget(self.dateTimeStartSelector)
        self.workDateTimeLayout.addWidget(self.workDateTimeEndLabel)
        self.workDateTimeLayout.addWidget(self.dateTimeEndSelector)
        self.mainLayout.addLayout(self.workDateTimeLayout)
        
        # work name
        self.workNameLayout = QVBoxLayout()
        self.workNameLabel = QLabel("نام کار", self)
        self.workNameInput = QLineEdit(self)
        self.workNameLayout.addWidget(self.workNameLabel)
        self.workNameLayout.addWidget(self.workNameInput)
        self.mainLayout.addLayout(self.workNameLayout)
    
    def closeEvent(self, event):
        self.parent.insertWorks()
        print("add work is being closed!")
        event.accept()
    
    def minimumEndUpdate(self,dateTime):
        self.dateTimeEndSelector.setMinimumDateTime(dateTime)
        
    def insertInDatabase(self):
        workName = self.workNameInput.text()
        workDateTimeStart = jdatetime.datetime.fromgregorian(date=self.dateTimeStartSelector.dateTime().toPyDateTime())
        workDateTimeEnd = jdatetime.datetime.fromgregorian(date=self.dateTimeEndSelector.dateTime().toPyDateTime())
        print(workName, workDateTimeStart, workDateTimeEnd)
        pass

#imlement
class EditWorkWindow(QMainWindow):
    def __init__(self, parent, workId):
        super().__init__()
        self.setWindowTitle(f"ویرایش کار {workId}")
        self.resize(QSize(400,200))
        pass # window and sql
    
    def closeEvent(self, event):
        self.parent.insertWorks()
        print("edit work is being closed!")
        event.accept()   

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #window = LoginWindow()
    #window = EmployeeWindow(50)
    window = AddWorkWindow(None)
    window.show()
    sys.exit(app.exec())