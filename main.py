import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QHBoxLayout, QScrollArea, QDateTimeEdit, QComboBox, QCheckBox
from PyQt6.QtCore import Qt, QSize, QCalendar, QLocale, QDateTime, QTimer
from PyQt6.QtGui import QPalette, QColor
import jdatetime
import datetime
import locale
from qt_material import apply_stylesheet, list_themes

locale.setlocale(locale.LC_ALL, jdatetime.FA_LOCALE)

class MainAppStyleWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        
        # self.setPalette(bgColor)
        
        locale.setlocale(locale.LC_ALL, jdatetime.FA_LOCALE)
        
        # initial widget and layout
        self.mainWidget = QWidget()
        self.mainWidget.setMinimumSize(QSize(700,400))
        self.resize(QSize(1000,600))
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        
        # up layout (for user information, date and time, user actions)
        self.upLayout = QHBoxLayout()
        self.upLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
        
        # Layout in right of up, for information of users
        self.infoLayout = QHBoxLayout()
        self.infoLayout.setSpacing(0)
        self.infoLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
        
        self.userIdLabel = QLabel('شماره کاربر')
        self.infoLayout.addWidget(self.userIdLabel)
        
        # name sub Layout
        self.nameLayout = QVBoxLayout()
        self.firstNameLabel = QLabel('نام کوچک')
        self.nameLayout.addWidget(self.firstNameLabel)
        self.lastNameLabel = QLabel('نام خانوادگی')
        self.nameLayout.addWidget(self.lastNameLabel)
        self.infoLayout.addLayout(self.nameLayout)
        
        self.workTypeLabel = QLabel('حوزه کاری', self)
        self.infoLayout.addWidget(self.workTypeLabel)
        
        self.dateTimeNowLabel = QLabel(str(jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S')), self)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerUpdate)
        self.timer.start(1000)
        self.infoLayout.addWidget(self.dateTimeNowLabel)
        
        self.upLayout.addLayout(self.infoLayout)
        
        # create action layout base
        self.actionLayout = QHBoxLayout()
        self.actionLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
        self.upLayout.addLayout(self.actionLayout)
        
        self.mainLayout.addLayout(self.upLayout)
        
        # down scroll layout
        self.downScrollLayout = QScrollArea()
        self.downScrollLayout.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.downScrollLayout.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.downScrollLayout.setWidgetResizable(True)
        
        self.mainLayout.addWidget(self.downScrollLayout)
        
    def timerUpdate(self):
        self.dateTimeNowLabel.setText(str(jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S')))
    
    # change info layout with tuple(UserId, First Name, Last Name, Type of Work)
    def updateInfo(self, info: tuple):
        self.userIdLabel.setText(info[0])
        self.firstNameLabel.setText(info[1])
        self.lastNameLabel.setText(info[2])
        self.workTypeLabel.setText(info[3])

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
                self.EmployeeWindow = EmployeeWindow(self.loginResault["ID"])
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

class EmployeeWindow(MainAppStyleWindow):
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
                            
        def __init__(self, uodateFunc):
            self.updateFunc = uodateFunc
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
            workName = self.workNameInput.text()
            workDateTimeStart = jdatetime.datetime.fromgregorian(date=self.dateTimeStartSelector.dateTime().toPyDateTime())
            workDateTimeEnd = jdatetime.datetime.fromgregorian(date=self.dateTimeEndSelector.dateTime().toPyDateTime())
            print(workName, workDateTimeStart, workDateTimeEnd) # delete
            
            #do sql
            
            self.updateFunc()
            pass
    
    class EditWorkWindow(AddWorkWindow):
        def __init__(self, updateFunc, workId):
            self.workId = workId
            super().__init__(updateFunc)
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
            
            self.updateFunc()
            
            pass
        
        def getWorkInfo(self):
            return {"name":"جوشکاری سقف بردار",
                    "dateTimeStart": datetime.datetime.now(),
                    "dateTimeEnd": datetime.datetime(2024,12,13,12,45)}
            pass
        
    def __init__(self, userId : int) -> None:
        super().__init__()
        self.employeeID = userId
        self.userInfo = self.getUserInfo()
        self.updateInfo(self.userInfo)
        
        # vertical layout for to choise work show
        self.showWorkLayout = QVBoxLayout()
        
        self.workStatusSelect = QComboBox()
        self.workStatusSelect.addItems(['کارهای بررسی نشده', 'کارهای رد شده', 'کارهای انجام شده'])
        self.workStatusSelect.currentIndexChanged.connect(self.updateWorkTable)
        self.showWorkLayout.addWidget(self.workStatusSelect)
        self.workShowNum = QCheckBox('نشان دادن 50 تای اول')
        self.workShowNum.setChecked(True)
        self.workShowNum.checkStateChanged.connect(self.updateWorkTable)
        self.showWorkLayout.addWidget(self.workShowNum)
        
        self.actionLayout.addLayout(self.showWorkLayout)
        
        # button of up (add task and show score)
        self.buttonsLayout = QVBoxLayout()
        
        self.addWorkBtn = QPushButton("اضافه کردن کار")
        self.addWorkBtn.clicked.connect(self.addWork)
        self.buttonsLayout.addWidget(self.addWorkBtn)
        self.showScoreBtn = QPushButton("نشان دادن نمره")
        self.showScoreBtn.clicked.connect(self.showScore)
        self.buttonsLayout.addWidget(self.showScoreBtn)
        
        self.actionLayout.addLayout(self.buttonsLayout)
        
        # run initials works showing
        self.updateWorkTable()
        
    # return a tuple with (user ID, first name, last name, work type)
    def getUserInfo(self):
        return 'شماره کارمند', 'نام کارمند', 'نام خانوادگی کارمند', 'گروه کاری کارمند'
    
    def updateWorkTable(self):
        self.widgetWorks = QWidget()
        
        works = self.getEmployeeWorks()
        self.layoutWorks = self.convertWorksToGui(works)
        
        self.widgetWorks.setLayout(self.layoutWorks)
        self.downScrollLayout.setWidget(self.widgetWorks)
    
    def getEmployeeWorks(self):
        """
        Retrieves a list of work items for an employee based on the selected work status and optional filtering.

        This function fetches work details for an employee, including work ID, work name, start and end times,
        importance degree, score, and status. The results can be filtered by the selected work status and limited
        to the 50 most recent works if specified.

        Returns:
            list: A list of tuples containing work details. Each tuple includes:
                - Work ID (str)
                - Work Name (str)
                - update DateTime (datetime)
                - Start DateTime (datetime)
                - End DateTime (datetime)
                - Importance Degree (int)
                - Score (float)
                - Status (int): 0 for not checked, 1 for rejected, 2 for accepted

                The first element of the list is a tuple of titles for each column in the work details.

        Note:
            The function currently includes placeholders (`pass`) for the logic to handle the number of works to show.
            This logic should be implemented to complete the functionality.
        """
        
        # 0 for not checked, 1 for rejected, 2 for accepted
        workTypeToShow = self.workStatusSelect.currentIndex()
        
        # if check show just 50 lastest work (sort by update date)
        if self.workShowNum.isChecked():
            pass
        else:
            pass
        
        works = []
        
        #must out of date
        works = [(25,"جوشکاری سقف دیگ نسوز", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 4, 10, 0),
                (100,"جوشکاری کف ایستگاه خاک", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 2, 7, 1),
                (99,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2),
                (33,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 0),
                (44,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1),
                (55,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1),
                (66,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2),
                (77,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2),
                (88,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1)]

        workInfoTitles = ("شماره کار", "نام کار", "زمان ویرایش", "شروع","پایان", "اهمیت کار", "نمره کار", "وضیعت تایید")
        works.insert(0, workInfoTitles)
        return works
    
    def convertWorksToGui(self, works):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        colorList = [QPalette(QColor(30,200,200)),
                    QPalette(QColor(6,208,1)),
                    QPalette(QColor(255, 162, 127))]
        for row in works:
            partWidget = QWidget()
            partLayout = QHBoxLayout()
            partLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
            partLayout.setSpacing(2)
            rejected = False
            colorSet = 0
            for i in range(len(row)):
                label = None
                if i == len(row) - 1 and type(row[i]) != str:
                    massage = None
                    if row[i] == 0:
                        massage = "عدم بررسی"
                        partWidget.setProperty('class', 'noSeeRecords')
                    elif row[i] == 1:
                        massage = "تایید"
                        colorSet = 1
                        partWidget.setProperty('class', 'acceptRecords')
                    else:
                        massage = "رد شده"
                        rejected = True
                        colorSet = 2
                        partWidget.setProperty('class', 'noRecords')
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
            
            partWidget.setLayout(partLayout)
            layout.addWidget(partWidget)
        return layout
    
    def showScore(self):
        self.showScoreWindow = self.ShowScoreWindow(self.employeeID)
        self.showScoreWindow.show()
    
    def addWork(self):
        self.addWorkWindow = self.AddWorkWindow(self.updateWorkTable)
        self.addWorkWindow.show()
        
    def editWork(self,workID):
        self.editWorkWindow = self.EditWorkWindow(self,workID)
        self.editWorkWindow.show()

if __name__ == '__main__':
    
    themeList = list_themes()
    app = QApplication(sys.argv)
    #window = LoginWindow()
    window = EmployeeWindow(50)
    
    apply_stylesheet(app, theme=themeList[11], css_file='custom.css')
    window.show()
    exitCode = app.exec()
    
    print(f"program finished, status code {exitCode}")
    sys.exit(exitCode)