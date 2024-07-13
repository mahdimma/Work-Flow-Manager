import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QHBoxLayout, QScrollArea, QDateTimeEdit, QComboBox, QCheckBox
from PyQt6.QtCore import Qt, QSize, QCalendar, QLocale, QDateTime, QTimer
import jdatetime
import datetime
import locale
from qt_material import apply_stylesheet, list_themes

locale.setlocale(locale.LC_ALL, jdatetime.FA_LOCALE)

class PersianDateTimeSelector(QDateTimeEdit):
    def __init__(self):
        super().__init__()
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy/MM/dd HH:mm")
        self.setDateTime(QDateTime.currentDateTime())
        jalali_calendar = QCalendar(QCalendar.System.Jalali)
        self.setCalendar(jalali_calendar)
        self.setLocale(QLocale(QLocale.Language.Persian))

class ShowScoreWindow(QMainWindow):
    def __init__(self, employeeID=None):
        super().__init__()
        self.employeeID = employeeID
        self.resize(QSize(400,200))
        if self.employeeID is not None:
            self.setWindowTitle(f"نمرات کارمند {self.employeeID}")
            self.scoreInfo = self.getScoreInfo()
        else:
            self.setWindowTitle("میانگین نمرات")
            self.scoreInfo = self.getAllScoreMean()
        self.display()
    def display(self):
        self.mainWidget = QWidget()
        self.mainLayout = QHBoxLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)
        self.mainLayout.addWidget(QLabel(f"نمره سالانه: {self.scoreInfo["y"]}"))
        self.mainLayout.addWidget(QLabel(f"نمره ماهانه: {self.scoreInfo["m"]}"))
        self.mainLayout.addWidget(QLabel(f"نمره هفتگی: {self.scoreInfo["w"]}"))

    def getScoreInfo(self) -> dict[str, float]:
        return {"w": 2.5, "m": 3.5, "y": 3.0}
        pass # with sql

    def getAllScoreMean(self) -> dict[str, float]:
        return {"w": 3.5, "m": 1.5, "y": 4.0}
        pass # with sql

class MainAppStyleWindow(QMainWindow):
    def __init__(self, userID) -> None:
        self.userID = userID
        super().__init__()
        # self.setPalette(bgColor)

        locale.setlocale(locale.LC_ALL, jdatetime.FA_LOCALE)

        # initial widget and layout
        self.mainWidget = QWidget()
        self.mainWidget.setMinimumSize(QSize(600,400))
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
        self.userIdLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        self.updateInfo()

    def timerUpdate(self):
        self.dateTimeNowLabel.setText(str(jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S')))

    def updateInfo(self):
        # change info layout with tuple(UserId, First Name, Last Name, Type of Work)
        info = self.__getUserInfo()
        self.userIdLabel.setText(info[0])
        self.firstNameLabel.setText(info[1])
        self.lastNameLabel.setText(info[2])
        self.workTypeLabel.setText(info[3])

    def __getUserInfo(self):
        # return a tuple with (user ID, first name, last name, work type)
        return f'شماره کاربر: {self.userID}', 'نام', 'نام خانوادگی', 'گروه کاری'

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

    def __init__(self, userID : int, changeInUpdate = None) -> None:
        super().__init__(userID)
        self.employeeID = userID
        self.changeInUpdate = changeInUpdate
        self.setWindowTitle(f"کارمند {self.employeeID}")

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

    def updateWorkTable(self):
        self.widgetWorks = QWidget()

        works = self.getEmployeeWorks()
        self.layoutWorks = self.convertWorksToGui(works)

        self.widgetWorks.setLayout(self.layoutWorks)
        self.downScrollLayout.setWidget(self.widgetWorks)
        if self.changeInUpdate is not None:
            self.changeInUpdate(self)

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
        for row in works:
            partWidget = QWidget()
            partWidget.setProperty('class', 'title')
            partLayout = QHBoxLayout()
            partLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
            partLayout.setSpacing(2)
            rejected = False
            for i in range(len(row)):
                label = None
                if i == len(row) - 1 and type(row[i]) != str:
                    massage = None
                    if row[i] == 0:
                        massage = "عدم بررسی"
                        partWidget.setProperty('class', 'noSeeRecords')
                    elif row[i] == 1:
                        massage = "تایید"
                        partWidget.setProperty('class', 'acceptRecords')
                    else:
                        massage = "رد شده"
                        rejected = True
                        partWidget.setProperty('class', 'noRecords')
                    label = QLabel(massage)
                else:
                    label = QLabel(str(row[i]))
                label.setAutoFillBackground(True)
                label.setWordWrap(True)
                label.setMinimumSize(QSize(100,60))
                label.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                partLayout.addWidget(label)
            editBtn = None
            if rejected:
                editBtn = QPushButton("ویرایش", self)
                workId = row[0]
                editBtn.clicked.connect(lambda checked, wid=workId: self.editWork(wid))
            else:
                editBtn = QLabel("")
            editBtn.setAutoFillBackground(True)
            editBtn.setMinimumSize(QSize(100,60))
            editBtn.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
            editBtn.setObjectName('employeeWorkEditBtn')
            partLayout.addWidget(editBtn)

            partWidget.setLayout(partLayout)
            layout.addWidget(partWidget)
        return layout

    def showScore(self):
        self.showScoreWindow = ShowScoreWindow(self.employeeID)
        self.showScoreWindow.show()

    def addWork(self):
        self.addWorkWindow = self.AddWorkWindow(self.updateWorkTable)
        self.addWorkWindow.show()

    def editWork(self,workID):
        self.editWorkWindow = self.EditWorkWindow(self,workID)
        self.editWorkWindow.show()

class ManagerWindow(MainAppStyleWindow):
    def __init__(self, userID: int) -> None:
        super().__init__(userID)
        self.managerId = userID
        self.setWindowTitle(f"مدیر {self.managerId}")
        self.resize(QSize(1100,680))

        self.updateBtn = QPushButton('بروزرسانی')
        self.updateBtn.clicked.connect(self.updateWorksTable)
        self.actionLayout.addWidget(self.updateBtn)

        self.updateWorksTable()

    def updateWorksTable(self):
        self.widgetWorks = QWidget()

        self.layoutWorks = self.convertWorksToGui(self.getNoCheckedWorks())

        self.widgetWorks.setLayout(self.layoutWorks)
        self.downScrollLayout.setWidget(self.widgetWorks)

    def convertWorksToGui(self, works: list[tuple]):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        for j, row in enumerate(works):
            partWidget = QWidget()
            partLayout = QHBoxLayout()
            partLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
            partLayout.setSpacing(2)

            for i in range(len(row)):
                label = None
                if i == len(row) - 1 and type(row[i]) != str:
                    partWidget.setProperty('class', 'noSeeRecords')
                    label = QLabel("عدم بررسی")
                else:
                    label = QLabel(str(row[i]))
                label.setAutoFillBackground(True)
                label.setWordWrap(True)
                label.setMinimumSize(QSize(100,60))
                label.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
                label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
                partLayout.addWidget(label)

            if j == 0:
                partLayout.addWidget(QLabel(""))
                partLayout.addWidget(QLabel(""))
            else:
                acceptWorkBtn = QPushButton("تایید", self)
                workId = row[0]
                acceptWorkBtn.clicked.connect(lambda checked, wid=workId: self.acceptWork(wid))
                acceptWorkBtn.setMinimumSize(QSize(100,60))
                acceptWorkBtn.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
                partLayout.addWidget(acceptWorkBtn)

                rejectWorkBtn = QPushButton("رد", self)
                workId = row[0]
                rejectWorkBtn.clicked.connect(lambda checked, wid=workId: self.rejectWork(wid))
                rejectWorkBtn.setMinimumSize(QSize(100,60))
                rejectWorkBtn.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
                partLayout.addWidget(rejectWorkBtn)


            partWidget.setLayout(partLayout)
            layout.addWidget(partWidget)
        return layout

    def acceptWork(self, workID):
        self.updateWorksTable()
        pass

    def rejectWork(self, workID):
        self.updateWorksTable()
        pass

    def getNoCheckedWorks(self):
        works = []

        #must out of date
        works = [(25,"جوشکاری سقف دیگ نسوز", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 4, 10, 0),
                (100,"جوشکاری کف ایستگاه خاک", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 2, 7, 0),
                (99,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 0),
                (33,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 0),
                (44,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 0)]

        workInfoTitles = ("شماره کار", "نام کار", "زمان ویرایش", "شروع","پایان", "اهمیت کار", "نمره کار", "وضیعت تایید")
        works.insert(0, workInfoTitles)
        return works
        pass

class SuperManagerWindow(MainAppStyleWindow):
    class AddUserWindow(QMainWindow):
        def __init__(self, eventHandler) -> None:
            super().__init__()
            self.eventHandler = eventHandler
            
            self.resize(QSize(600,200))
            
            self.mainWidget = QWidget()
            self.mainLayout = QHBoxLayout(self.mainWidget)
            self.mainLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
            
            # id Label
            self.idLabel = QLabel('')
            self.mainLayout.addWidget(self.idLabel)
            self.idLabel.setHidden(True)
            
            # name sub Layout
            self.nameLayout = QVBoxLayout()
            self.nameLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.firstNameLabel = QLabel('نام کوچک')
            self.nameLayout.addWidget(self.firstNameLabel)
            self.firstNameInput = QLineEdit(self)
            self.nameLayout.addWidget(self.firstNameInput)
            self.lastNameLabel = QLabel('نام خانوادگی')
            self.nameLayout.addWidget(self.lastNameLabel)
            self.lastNameInput = QLineEdit(self)
            self.nameLayout.addWidget(self.lastNameInput)
            self.mainLayout.addLayout(self.nameLayout)
            
            # type Layout
            self.typeLayout = QVBoxLayout()
            self.typeLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.degreeCombo = QComboBox()
            self.degreeCombo.setMinimumSize(QSize(120,20))
            self.degreeCombo.addItems(['کارمند', 'مدیر', 'مدیر ارشد'])
            self.typeLayout.addWidget(self.degreeCombo)
            self.workGroupCombo = QComboBox()
            self.workGroupCombo.addItems(self.getWorkGroupsList())
            self.typeLayout.addWidget(self.workGroupCombo)
            self.mainLayout.addLayout(self.typeLayout)
            
            self.passwordLayout = QVBoxLayout()
            self.passwordLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.passwordLabel = QLabel('رمز کاربر', self)
            self.passwordLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.passwordLayout.addWidget(self.passwordLabel)
            self.passwordInput = QLineEdit(self)
            self.passwordInput.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
            self.passwordLayout.addWidget(self.passwordInput)
            self.mainLayout.addLayout(self.passwordLayout)
            
            self.okBtn = QPushButton('تایید')
            self.okBtn.setMinimumSize(QSize(120,20))
            self.okBtn.clicked.connect(self.insertInDataBase)
            self.mainLayout.addWidget(self.okBtn)
            
            self.setCentralWidget(self.mainWidget)
            
        def getWorkGroupsList(self) -> list[str]:
            return ['اصلی', 'انسانی', 'صنعت']
            pass
        
        def insertInDataBase(self):
            pass #with sql
            self.eventHandler()
            self.close()
            
    class EditUserWindow(AddUserWindow):
        def __init__(self, userID : int,  eventHandler) -> None:
            super().__init__(eventHandler)
            self.userID = userID
            self.setWindowTitle(f'کاربر {self.userID}')
            
            self.userInfo = self.getInfo()
            self.firstNameInput.setText(self.userInfo[0])
            self.lastNameInput.setText(self.userInfo[1])
            self.degreeCombo.setCurrentIndex(self.userInfo[2])
            self.workGroupCombo.setCurrentIndex(self.userInfo[3])
            
        def getInfo(self):
            return ['نام', 'شهرت', 0, 2]
            pass
        
        def insertInDataBase(self):
            pass # with sql
            self.eventHandler()
            self.close()
    
    def __init__(self, userID) -> None:
        super().__init__(userID)
        self.seniorManagerId = userID
        self.setWindowTitle(f"مدیر ارشد {self.seniorManagerId}")
        self.resize(QSize(1100,680))

        # vertical layout for to choise work show
        self.showTableLayout = QVBoxLayout()

        self.typeTableSelect = QComboBox()
        self.typeTableSelect.addItems(['کارها', 'کاربرها'])
        self.typeTableSelect.currentIndexChanged.connect(self.changeTypeTable)
        self.showTableLayout.addWidget(self.typeTableSelect)
        self.workStatusSelect = QComboBox()
        self.workStatusSelect.addItems(['کارهای بررسی نشده', 'کارهای رد شده', 'کارهای انجام شده'])
        self.workStatusSelect.currentIndexChanged.connect(self.updateTable)
        self.workStatusSelect.setHidden(False)
        self.showTableLayout.addWidget(self.workStatusSelect)
        self.usersType = QComboBox()
        self.usersType.addItems(['کارمندان', 'مدیران', 'مدیران ارشد'])
        self.usersType.currentIndexChanged.connect(self.updateTable)
        self.usersType.setHidden(True)
        self.showTableLayout.addWidget(self.usersType)
        self.showNum = QCheckBox('نشان دادن 50 تای اول')
        self.showNum.setChecked(True)
        self.showNum.checkStateChanged.connect(self.updateTable)
        self.showTableLayout.addWidget(self.showNum)

        self.actionLayout.addLayout(self.showTableLayout)

        self.changeLayout = QVBoxLayout()

        self.addUserBtn = QPushButton('اضافه کردن کاربر')
        self.addUserBtn.clicked.connect(self.addUser)
        self.changeLayout.addWidget(self.addUserBtn)

        self.updateScoresBtn = QPushButton('بروزرسانی نمرات')
        self.updateScoresBtn.clicked.connect(self.updateScores)
        self.changeLayout.addWidget(self.updateScoresBtn)

        self.showMeanOfScoresBtn = QPushButton('نمایش میانگین نمرات')
        self.showMeanOfScoresBtn.clicked.connect(self.showMeanOfScores)
        self.changeLayout.addWidget(self.showMeanOfScoresBtn)

        self.actionLayout.addLayout(self.changeLayout)

        self.updateTable()

    def updateTable(self):
        widgetWorks = QWidget()
        recordsLayout = None
        if self.typeTableSelect.currentIndex() == 0:
            recordsLayout = self.convertWorksToGui(self.getWorks())
        else:
            recordsLayout = self.convertUsersToGui(self.getUsers())

        widgetWorks.setLayout(recordsLayout)
        self.downScrollLayout.setWidget(widgetWorks)

    def convertWorksToGui(self, works):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        for row in works:
            partWidget = QWidget()
            partWidget.setProperty('class', 'title')
            partLayout = QHBoxLayout()
            partLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
            partLayout.setSpacing(2)
            for i in range(len(row)):
                label = None
                if i == len(row) - 3 and type(row[i]) != str:
                    massage = None
                    if row[i] == 0:
                        massage = "عدم بررسی"
                        partWidget.setProperty('class', 'noSeeRecords')
                    elif row[i] == 1:
                        massage = "تایید"
                        partWidget.setProperty('class', 'acceptRecords')
                    else:
                        massage = "رد شده"
                        partWidget.setProperty('class', 'noRecords')
                    label = QLabel(massage)
                else:
                    label = QLabel(str(row[i]))
                label.setAutoFillBackground(True)
                label.setWordWrap(True)
                label.setMinimumSize(QSize(100,60))
                label.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                partLayout.addWidget(label)

            partWidget.setLayout(partLayout)
            layout.addWidget(partWidget)
        return layout

    def convertUsersToGui(self, users):
        layout = QVBoxLayout()
        layout.setSpacing(5)
        for row in users:
            partWidget = QWidget()
            partWidget.setProperty('class', 'title')
            partLayout = QHBoxLayout()
            partLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
            partLayout.setSpacing(2)
            isEmployee = False
            isManager = False
            for i in range(len(row)):
                label = None
                if i == len(row) - 1 and type(row[i]) != str:
                    massage = None
                    if row[i] == 0:
                        massage = "کارمند"
                        isEmployee = True
                        partWidget.setProperty('class', 'noSeeRecords')
                    elif row[i] == 1:
                        massage = "مدیر"
                        isManager = True
                        partWidget.setProperty('class', 'acceptRecords')
                    else:
                        massage = "مدیر ارشد"
                        partWidget.setProperty('class', 'noRecords')
                    label = QLabel(massage)
                else:
                    label = QLabel(str(row[i]))
                label.setAutoFillBackground(True)
                label.setWordWrap(True)
                label.setMinimumSize(QSize(80,60))
                label.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                partLayout.addWidget(label)
            editBtn = userWorkBtn = None
            if isEmployee:
                editBtn = QPushButton("ویرایش", self)
                userWorkBtn = QPushButton("کارهای کارمند", self)
                userId = row[0]
                editBtn.clicked.connect(lambda checked, uId=userId: self.editUser(uId))
                userWorkBtn.clicked.connect(lambda checked, uId=userId: self.showUserWork(uId))
            elif isManager:
                editBtn = QPushButton("ویرایش", self)
                userId = row[0]
                editBtn.clicked.connect(lambda checked, uId=userId: self.editUser(uId))
                userWorkBtn = QLabel("")
            else:
                editBtn = QLabel("")
                userWorkBtn = QLabel("")
            editBtn.setAutoFillBackground(True)
            editBtn.setMinimumSize(QSize(100,60))
            editBtn.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
            partLayout.addWidget(editBtn)
            userWorkBtn.setAutoFillBackground(True)
            userWorkBtn.setMinimumSize(QSize(120,60))
            userWorkBtn.setLocale(QLocale(QLocale.Language.Persian,QLocale.Country.Iran ))
            partLayout.addWidget(userWorkBtn)

            partWidget.setLayout(partLayout)
            layout.addWidget(partWidget)
        return layout

    def getWorks(self):
        if self.showNum.isChecked():
            pass
        else:
            pass

        works = []

        #must out of date
        works = [(25,"جوشکاری سقف دیگ نسوز", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 4, 10, 0, 22, 12),
                (100,"جوشکاری کف ایستگاه خاک", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 2, 7, 1, 28, 12),
                (99,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2, 28, 12),
                (33,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 0, 35, 12),
                (44,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1, 21, 10),
                (55,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1, 27, 11),
                (66,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2, 39, 18),
                (77,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 2, 58, 13),
                (88,"فراردهی گاز مایع", jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'),jdatetime.datetime.now().strftime('%d %b %Y\n%H:%M:%S'), 5, 6, 1, 96, 12)]

        workInfoTitles = ("شماره کار", "نام کار", "زمان ویرایش", "شروع","پایان", "اهمیت کار", "نمره کار", "وضیعت تایید", "کارمند انجام دهنده", "مدیر آخرین تغییرات")
        works.insert(0, workInfoTitles)
        return works

    def getUsers(self):
        if self.showNum.isChecked():
            pass
        else:
            pass

        users = []

        #must out of date
        users = [(25,"احمد", "متوسلی", 2, 2.5, 3.5, 4.5, 0),
                (12,"رضا", "متوسلی", 2, 2.5, 3.5, 4.5, 0),
                (27,"کامران", "علیان", 2, 2.5, 3.5, 4.5, 2),
                (2,"شاهد", "مولی", 3, 2.5, 3.5, 4.5, 1),
                (45,"یادین", "فونتیا", 1, 2.5, 3.5, 4.5, 0)]

        userInfoTitle = ("شماره کاربر", "نام کاربر", "نام خانوادگی کاربر", "نوع کار کاربر","امتیاز هفتگی", "امتیاز ماهانه", "امتیاز سالانه", "نوع کاربر")
        users.insert(0, userInfoTitle)
        return users

    def changeTypeTable(self, index):
        if index == 0:
            self.workStatusSelect.setHidden(False)
            self.usersType.setHidden(True)
            self.updateTable()
        else:
            self.workStatusSelect.setHidden(True)
            self.usersType.setHidden(False)
            self.updateTable()

    def addUser(self):
        self.addUserWindow = self.AddUserWindow(self.updateTable)
        self.addUserWindow.show()

    def editUser(self, userID):
        self.editUserWindow = self.EditUserWindow(userID, self.updateTable)
        self.editUserWindow.idLabel.setText(f"شماره کاربر: {userID}")
        self.editUserWindow.idLabel.setHidden(False)
        self.editUserWindow.show()

    def showUserWork(self, userID):
        employeeWindow = EmployeeWindow(userID, self.removeUserEditWork)
        employeeWindow.show()
        employeeWindow.addWorkBtn.setHidden(True)
    
    def removeUserEditWork(self, employeeWindow):
        for buttons in employeeWindow.findChildren(QPushButton, 'employeeWorkEditBtn'):
            buttons.setHidden(True)
        for label in employeeWindow.findChildren(QLabel, 'employeeWorkEditBtn'):
            label.setHidden(True)
    
    def updateScores(self):
        pass # with sql
        self.updateTable()

    def showMeanOfScores(self):
        self.scoresMeanWindow = ShowScoreWindow()
        self.scoresMeanWindow.show()

if __name__ == '__main__':

    themeList = list_themes()
    app = QApplication(sys.argv)
    #window = LoginWindow()
    #window = EmployeeWindow(50)
    #window = ManagerWindow(34)
    window = SuperManagerWindow(20)

    apply_stylesheet(app, theme=themeList[11], css_file='custom.css')

    window.show()
    exitCode = app.exec()

    print(f"program finished, status code {exitCode}")
    sys.exit(exitCode)