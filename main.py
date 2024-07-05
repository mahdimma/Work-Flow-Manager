import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QHBoxLayout, QScrollArea, QDateTimeEdit
from PyQt6.QtCore import Qt, QSize, QCalendar, QLocale, QDateTime, QDate, QTime
from PyQt6.QtGui import QPalette, QColor
import jdatetime
import datetime
import locale

locale.setlocale(locale.LC_ALL, jdatetime.FA_LOCALE)

globalColor = {"bg": QPalette(QColor(68,68,68))}

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
    def __init__(self, colorBg: QPalette):
        self.colorBg = colorBg
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Login Window')
        self.resize(QSize(300,300))
        self.centerize()
        
        self.setPalette(self.colorBg)
        
        layout = QVBoxLayout()

        self.label_username = QLabel('Username:', self)
        layout.addWidget(self.label_username)

        self.text_username = QLineEdit(self)
        layout.addWidget(self.text_username)

        self.label_password = QLabel('Password:', self)
        layout.addWidget(self.label_password)

        self.text_password = QLineEdit(self)
        self.text_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
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
                self.EmployeeWindow = EmployeeWindow(self.loginResault["ID"], self.colorBg)
                self.hide()
                self.EmployeeWindow.show()
            elif self.loginResault["type"] == 2: # manager
                pass
            else: # supervisor
                pass
        else:
            QMessageBox.warning(self, 'خطا', 'نام کاربری یا رمز اشتباه وارد شده است!')

            
    def centerize(self):
        # Get screen geometry and window geometry
        screen_rect = QApplication.primaryScreen().geometry()
        window_rect = self.geometry()

        # Calculate center coordinates
        center_x = (screen_rect.center().x() - window_rect.width() // 2)
        center_y = (screen_rect.center().y() - window_rect.height() // 2)

        # Move the window to the center
        self.move(center_x, center_y)
    
    def loginCheck(self, username, password) -> dict:
        return {"correct": True, "type": 1, "ID": 34}
        #return dict {"correct": (False|True), "type": (1(Employee) | 2(manager) | 3(supervisor)), "ID": id_number}
        pass #sql

class EmployeeWindow(QMainWindow):
    
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
            self.okBtn.clicked.connect(self.doDatabaseChange)
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
        
        def minimumEndUpdate(self,dateTime):
            self.dateTimeEndSelector.setMinimumDateTime(dateTime)
            
        def doDatabaseChange(self):
            print("apend in database")
            workName = self.workNameInput.text()
            workDateTimeStart = jdatetime.datetime.fromgregorian(date=self.dateTimeStartSelector.dateTime().toPyDateTime())
            workDateTimeEnd = jdatetime.datetime.fromgregorian(date=self.dateTimeEndSelector.dateTime().toPyDateTime())
            print(workName, workDateTimeStart, workDateTimeEnd)
            
            #do sql
            
            self.parent.insertWorks()
            pass

    class EditWorkWindow(AddWorkWindow):
        def __init__(self, parent, workId):
            self.workId = workId
            super().__init__(parent)
            self.setWindowTitle(f"ویرایش کار {workId}")
            self.resize(QSize(400,200))
            
            workInfo = self.getWorkInfo()
            
            self.workNameInput.setText(workInfo['name'])
            self.dateTimeStartSelector.setDateTime(workInfo['dateTimeStart'])
            self.dateTimeEndSelector.setDateTime(workInfo['dateTimeEnd'])
        
        def doDatabaseChange(self):
            print("edit in database")
            workName = self.workNameInput.text()
            workDateTimeStart = jdatetime.datetime.fromgregorian(date=self.dateTimeStartSelector.dateTime().toPyDateTime())
            workDateTimeEnd = jdatetime.datetime.fromgregorian(date=self.dateTimeEndSelector.dateTime().toPyDateTime())
            print(workName, workDateTimeStart, workDateTimeEnd)
            
            # do sql
            
            self.parent.insertWorks()
            
            pass
        
        def getWorkInfo(self):
            return {"name":"جوشکاری سقف بردار",
                    "dateTimeStart": datetime.datetime.now(),
                    "dateTimeEnd": datetime.datetime(2024,12,13,12,45)}
            pass

    def __init__(self, employeeID, bgColor):
        self.employeeID = employeeID
        super().__init__()
        self.setWindowTitle("کارمند")
        
        self.resize(QSize(1000,600))
        
        #get information of employee
        self.employeeInformation = self.getEmployeeInformation(self.employeeID)
        
        self.setPalette(bgColor)
        
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
        self.widgetWorks = QWidget()
        
        works = self.getEmployeeWorks()
        self.layoutWorks = self.convertWorksToGui(works)
        
        self.widgetWorks.setLayout(self.layoutWorks)
        self.scrollPart.setWidget(self.widgetWorks)
        pass # with sql
    
    def getEmployeeWorks(self):
        # list of tuples (workID, workName, dateTime start, dateTime end, importance degree, score, status)
        
        workInfoTitles = ("شماره کار", "نام کار", "شروع","پایان", "اهمیت کار", "نمره کار", "وضیعت تایید")
        works = [(25,"جوشکاری سقف دیگ نسوز", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 4, 10, 0),
                (100,"جوشکاری کف ایستگاه خاک", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 2, 7, 1),
                (99,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2),
                (33,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 0),
                (44,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1),
                (55,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1),
                (66,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2),
                (77,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2),
                (88,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1)]
        works.insert(0, workInfoTitles)
        return works
        pass
    
    def convertWorksToGui(self, works):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        colorList = [QPalette(QColor(30,200,200)),
                    QPalette(QColor(6,208,1)),
                    QPalette(QColor(255, 162, 127))]
        
        for row in works:
            partLayout = QHBoxLayout()
            partLayout.setSpacing(2)
            rejected = False
            colorSet = 0
            for i in range(len(row) - 1, -1, -1):
                label = None
                if i == len(row) - 1 and type(row[i]) != str:
                    massage = None
                    if row[i] == 0:
                        massage = "عدم بررسی"
                    elif row[i] == 1:
                        massage = "تایید"
                        colorSet = 1
                    else:
                        massage = "رد شده"
                        rejected = True
                        colorSet = 2
                    label = QLabel(massage)
                else:
                    label = QLabel(str(row[i]))
                label.setPalette(colorList[colorSet])
                label.setAutoFillBackground(True)
                label.setWordWrap(True)
                label.setMinimumSize(QSize(100,60))
                label.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
                label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
                partLayout.addWidget(label)
            editBtn = None
            if rejected:
                editBtn = QPushButton("ویرایش", self)
                workId = row[0]
                editBtn.clicked.connect(lambda checked, wid=workId: self.editWork(wid))
            else:
                editBtn = QLabel("")
            editBtn.setPalette(colorList[colorSet])
            editBtn.setAutoFillBackground(True)
            editBtn.setMinimumSize(QSize(100,60))
            editBtn.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
            partLayout.addWidget(editBtn)
            
            layout.addLayout(partLayout)
        return layout
    
    def addWork(self):
        self.addWorkWindow = self.AddWorkWindow(self)
        self.addWorkWindow.show()
        pass
        
    def showScore(self):
        self.showScoreWindow = self.ShowScoreWindow(self.employeeID)
        self.showScoreWindow.show()
    
    def editWork(self,workID):
        self.editWorkWindow = self.EditWorkWindow(self,workID)
        self.editWorkWindow.show()
    
    def getEmployeeInformation(self, employeeId):
        return {"fName": "نام", "lName": "فامیلی", "workType": "نوع کار"}
        pass # with sql

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow(globalColor["bg"])
    #window = EmployeeWindow(50, globalColor["bg"])
    window.show()
    sys.exit(app.exec())