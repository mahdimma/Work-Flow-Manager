import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QMainWindow, QHBoxLayout, QScrollArea, QDateTimeEdit, QComboBox, QCheckBox
from PyQt6.QtCore import Qt, QSize, QCalendar, QLocale, QDateTime, QTimer
import jdatetime
import datetime
import locale
import pyodbc
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
    def __init__(self, cursor: pyodbc.Cursor, employeeID=None):
        super().__init__()
        self.employeeID = employeeID
        self.resize(QSize(400,200))
        self.dbCursor = cursor
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
        self.dbCursor.execute(f'select weeklyScore, monthlyScore, yearlyScore from users where userId={self.employeeID}')
        row = self.dbCursor.fetchone()
        if row is not None:
            return {"w": row[0], "m": row[1], "y": row[2]}
        return {"w": 0, "m": 0, "y": 0}
    
    def getAllScoreMean(self) -> dict[str, float]:
        self.dbCursor.execute("""SELECT
            ROUND(AVG(weeklyScore), 4) AS MeanWeeklyScore,
            ROUND(AVG(monthlyScore), 4) AS MeanMonthlyScore,
            ROUND(AVG(yearlyScore), 4) AS MeanYearlyScore
            FROM users
            WHERE degreeUser = 0;""")
        row = self.dbCursor.fetchone()
        print(row)
        if row is not None:
            return {"w": row[0], "m": row[1], "y": row[2]}
        return {"w": 0, "m": 0, "y": 0}

class MainAppStyleWindow(QMainWindow):
    def __init__(self, userID, cursor: pyodbc.Cursor) -> None:
        self.userID = userID
        self.dbCursor = cursor
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
        query = """SELECT u.firstName, u.lastName, wg.workGroupName AS workTypeName
            FROM users u
            JOIN workGroup wg ON u.workType = wg.workGroupId
            WHERE u.userId = ?;
                    """
        self.dbCursor.execute(query, self.userID)
        row = self.dbCursor.fetchone()
        if row is not None:
            return (f'شماره کاربر: {self.userID}', row[0], row[1], row[2])
        print("sql not found")
        exit(2)

class LoginWindow(QWidget):
    def __init__(self, cursor: pyodbc.Cursor):
        super().__init__()
        self.initUI()
        self.dbCursor = cursor

    def initUI(self):
        self.setWindowTitle('ورود')
        self.resize(QSize(300,300))

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_username = QLabel('آیدی:', self)
        layout.addWidget(self.label_username)

        self.text_username = QLineEdit(self)
        layout.addWidget(self.text_username)

        self.label_password = QLabel('رمز عبور:', self)
        layout.addWidget(self.label_password)

        self.text_password = QLineEdit(self)
        self.text_password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        layout.addWidget(self.text_password)

        self.button_login = QPushButton('ورود', self)
        self.button_login.clicked.connect(self.handle_login)
        layout.addWidget(self.button_login)

        self.setLayout(layout)

    def handle_login(self):
        userId = self.text_username.text()
        password = self.text_password.text()
        self.loginResault = self.loginCheck(int(userId), password)
        print(self.loginResault)
        if self.loginResault["correct"] is True:
            if self.loginResault["type"] == 0: # employee
                self.employeeWindow = EmployeeWindow(self.loginResault["ID"], self.dbCursor)
                self.hide()
                self.employeeWindow.show()
            elif self.loginResault["type"] == 1: # manager
                self.managerWindow = ManagerWindow(self.loginResault["ID"], self.dbCursor)
                self.hide()
                self.managerWindow.show()
            else: # supervisor
                self.superManagerWindow = SuperManagerWindow(self.loginResault["ID"], self.dbCursor)
                self.hide()
                self.superManagerWindow.show()
        else:
            QMessageBox.warning(self, 'خطا', 'نام کاربری یا رمز اشتباه وارد شده است!')

    def loginCheck(self, userId, password) -> dict:
        self.dbCursor.execute(f'select password, degreeUser from users where userId={userId}')
        row = self.dbCursor.fetchone()
        print(row)
        if row is not None:
            if row[0] == password:
                return {"correct": True, "type": row[1], "ID": userId}
        return {'correct': False, 'type': 0, "ID": 0}

class EmployeeWindow(MainAppStyleWindow):

    class AddWorkWindow(QMainWindow):
        class PersianDateTimeSelectorStart(PersianDateTimeSelector):
            def __init__(self, eventHandler):
                super().__init__()
                self.dateTimeChanged.connect(eventHandler)

        def __init__(self, uodateFunc, cursor: pyodbc.Cursor, employeeId: int):
            self.updateFunc = uodateFunc
            super().__init__()
            self.dbCursor = cursor
            self.employeeId = employeeId
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
            workDateTimeStart = self.dateTimeStartSelector.dateTime().toPyDateTime()
            print(jdatetime.datetime.fromgregorian(date=self.dateTimeStartSelector.dateTime().toPyDateTime()))
            workDateTimeEnd = self.dateTimeEndSelector.dateTime().toPyDateTime()
            print(jdatetime.datetime.fromgregorian(date=self.dateTimeEndSelector.dateTime().toPyDateTime()))
            
            query = """INSERT INTO works (w_name, updateDateTime, w_start_datetime, w_end_datetime, w_employee_do)
                VALUES (?, ?, ?, ?, ?);
                """
            self.dbCursor.execute(query, workName,datetime.datetime.now(), workDateTimeStart, workDateTimeEnd, self.employeeId)
            self.dbCursor.commit()
            
            self.updateFunc()
            self.close()

    class EditWorkWindow(AddWorkWindow):
        def __init__(self, updateFunc, workId, cursor: pyodbc.Cursor, employeeId: int):
            self.workId = workId
            self.dbCursor = cursor
            super().__init__(updateFunc, self.dbCursor, employeeId)
            
            self.setWindowTitle(f"ویرایش کار {workId}")
            self.resize(QSize(400,200))

            workInfo = self.getWorkInfo()

            self.workNameInput.setText(workInfo['name'])
            self.dateTimeStartSelector.setDateTime(workInfo['dateTimeStart'])
            self.dateTimeEndSelector.setDateTime(workInfo['dateTimeEnd'])

        def doDatabaseChange(self):
            print("edit in database")
            workName = self.workNameInput.text()
            workDateTimeStart = self.dateTimeStartSelector.dateTime().toPyDateTime()
            print(jdatetime.datetime.fromgregorian(date=self.dateTimeStartSelector.dateTime().toPyDateTime()))
            workDateTimeEnd = self.dateTimeEndSelector.dateTime().toPyDateTime()
            print(jdatetime.datetime.fromgregorian(date=self.dateTimeEndSelector.dateTime().toPyDateTime()))
            print(workName, workDateTimeStart, workDateTimeEnd) # delete

            query = """
                UPDATE works
                SET w_name = ?,
                    updateDateTime = ?,
                    w_start_datetime = ?,
                    w_end_datetime = ?,
                    w_status = ?
                WHERE w_id = ?;
                """
            self.dbCursor.execute(query, workName, datetime.datetime.now(), workDateTimeStart, workDateTimeEnd, 0, self.workId)
            self.dbCursor.commit()

            self.updateFunc()
            self.close()

        def getWorkInfo(self):
            query = """SELECT
                        w_name,
                        w_start_datetime,
                        w_end_datetime
                    FROM works
                    WHERE w_id = ?;
                    """
            self.dbCursor.execute(query, self.workId)
            row = self.dbCursor.fetchone()
            if row is not None:
                return {"name": row[0],
                    "dateTimeStart": row[1],
                    "dateTimeEnd": row[2]}
            print("sql not found")
            exit(2)

    def __init__(self, userID : int, cursor: pyodbc.Cursor, changeInUpdate = None) -> None:
        super().__init__(userID, cursor)
        self.employeeID = userID
        self.dbCursor = cursor
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
        # 0 for not checked, 1 for rejected, 2 for accepted
        workTypeToShow = self.workStatusSelect.currentIndex()

        query = ''
        # if check show just 50 lastest work (sort by update date)
        if self.workShowNum.isChecked():
            if workTypeToShow == 0:
                query = """SELECT TOP 50 w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 0 AND w_employee_do = ?
                            ORDER BY w_id DESC;
                        """
            elif workTypeToShow == 1:
                query = """SELECT TOP 50 w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 1 AND w_employee_do = ?
                            ORDER BY w_id DESC;
                        """
            else:
                query = """SELECT TOP 50 w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 2 AND w_employee_do = ?
                            ORDER BY w_id DESC;
                        """
        else:
            if workTypeToShow == 0:
                query = """SELECT w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 0 AND w_employee_do = ?
                            ORDER BY w_id DESC;
                        """
            elif workTypeToShow == 1:
                query = """SELECT w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 1 AND w_employee_do = ?
                            ORDER BY w_id DESC;
                        """
            else:
                query = """SELECT w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 2 AND w_employee_do = ?
                            ORDER BY w_id DESC;
                        """
            
        self.dbCursor.execute(query, self.employeeID)
        rows = self.dbCursor.fetchall()
        
        jalaliRows = []
        for row in rows:
            jalali_row = list(row)
            jalali_row[2] = jdatetime.datetime.fromgregorian(datetime=row[2]).strftime('%d %b %Y\n%H:%M:%S')
            jalali_row[3] = jdatetime.datetime.fromgregorian(datetime=row[3]).strftime('%d %b %Y\n%H:%M:%S')
            jalali_row[4] = jdatetime.datetime.fromgregorian(datetime=row[4]).strftime('%d %b %Y\n%H:%M:%S')
            jalaliRows.append(jalali_row)
        
        workInfoTitles = ("شماره کار", "نام کار", "زمان ویرایش", "شروع","پایان", "اهمیت کار", "نمره کار", "مدیر آخرین ویرایش", "وضیعت تایید")
        jalaliRows.insert(0, workInfoTitles)
        return jalaliRows

    def convertWorksToGui(self, works):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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
                    elif row[i] == 2:
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
        self.showScoreWindow = ShowScoreWindow(self.dbCursor, self.employeeID)
        self.showScoreWindow.show()

    def addWork(self):
        self.addWorkWindow = self.AddWorkWindow(self.updateWorkTable, self.dbCursor, self.employeeID)
        self.addWorkWindow.show()

    def editWork(self,workID):
        self.editWorkWindow = self.EditWorkWindow(self.updateWorkTable, workID, self.dbCursor, self.employeeID)
        self.editWorkWindow.show()

class ManagerWindow(MainAppStyleWindow):
    class AcceptWindow(QMainWindow):
        def __init__(self, userID: int, workId: int, cursor: pyodbc.Cursor, updateFunc) -> None:
            super().__init__()
            self.dbCursor = cursor
            self.managerId = userID
            self.updateWorksTable = updateFunc
            self.workId = workId
            
            mainWidget = QWidget()
            self.setCentralWidget(mainWidget)
            self.showWorkLayout = QVBoxLayout(mainWidget)

            self.workImportanceSelect = QComboBox()
            self.workImportanceSelect.addItems([str(x) for x in range(1, 6)])
            self.showWorkLayout.addWidget(self.workImportanceSelect)
            self.workScoreSelect = QComboBox()
            self.workScoreSelect.addItems([str(x) for x in range(1, 11)])
            self.showWorkLayout.addWidget(self.workScoreSelect)
            self.okBtn = QPushButton('تایید')
            self.okBtn.clicked.connect(self.acceptHandle)
            self.showWorkLayout.addWidget(self.okBtn)
            
        def acceptHandle(self):
            query = """UPDATE works
                    SET
                        updateDateTime = ?,
                        importance = ?,
                        score = ?,
                        w_manager_do = ?,
                        w_status = ?
                    WHERE w_id = ?;
                        """
            self.dbCursor.execute(query, datetime.datetime.now(), self.workImportanceSelect.currentIndex() + 1, self.workScoreSelect.currentIndex() + 1, self.managerId, 2, self.workId)
            self.dbCursor.commit()
            self.updateWorksTable()
            self.close()
    
    def __init__(self, userID: int, cursor: pyodbc.Cursor) -> None:
        super().__init__(userID, cursor)
        self.dbCursor = cursor
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
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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
        self.acceptWindow = self.AcceptWindow(self.managerId, workID, self.dbCursor, self.updateWorksTable)
        self.acceptWindow.setWindowModality(Qt.WindowModality.ApplicationModal) 
        self.acceptWindow.show()

    def rejectWork(self, workID):
        query = """UPDATE works
                    SET
                        updateDateTime = ?,
                        w_manager_do = ?,
                        w_status = ?
                    WHERE w_id = ?;
                        """
        self.dbCursor.execute(query,datetime.datetime.now(), self.managerId, 1, workID)
        self.dbCursor.commit()
        self.updateWorksTable()

    def getNoCheckedWorks(self):
        query = """SELECT TOP 50 w_id, w_name, updateDateTime, w_start_datetime,
                    w_end_datetime, w_employee_do
                    FROM works
                    WHERE w_status = 0
                    ORDER BY w_id;
                """
                
        self.dbCursor.execute(query)
        rows = self.dbCursor.fetchall()
        
        jalaliRows = []
        for row in rows:
            jalali_row = list(row)
            jalali_row[2] = jdatetime.datetime.fromgregorian(datetime=row[2]).strftime('%d %b %Y\n%H:%M:%S')
            jalali_row[3] = jdatetime.datetime.fromgregorian(datetime=row[3]).strftime('%d %b %Y\n%H:%M:%S')
            jalali_row[4] = jdatetime.datetime.fromgregorian(datetime=row[4]).strftime('%d %b %Y\n%H:%M:%S')
            jalaliRows.append(jalali_row)
        
        workInfoTitles = ("شماره کار", "نام کار", "زمان ویرایش", "شروع","پایان", "کارمند انجام دهنده")
        jalaliRows.insert(0, workInfoTitles)
        return jalaliRows

class SuperManagerWindow(MainAppStyleWindow):

    class AddUserWindow(QMainWindow):
        def __init__(self, eventHandler, cursor: pyodbc.Cursor) -> None:
            super().__init__()
            self.eventHandler = eventHandler
            self.dbCursor = cursor
            
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
            query = """SELECT workGroupId, workGroupName
                    FROM workGroup
                """
            self.dbCursor.execute(query)
            rows = self.dbCursor.fetchall()
            names = []
            self.groupTypes = []
            for row in rows:
                names.append(row[1])
                self.groupTypes.append(row[0])
            return names
        
        def insertInDataBase(self):
            firstName = self.firstNameInput.text()
            lastName = self.lastNameInput.text()
            degreeUser = self.degreeCombo.currentIndex()
            workGroupType = self.groupTypes[self.workGroupCombo.currentIndex()]
            password = self.passwordInput.text()
            query = """INSERT INTO users(firstName, lastName, degreeUser, workType, password)
                        VALUES (?, ?, ?, ?, ?)
                    """
            self.dbCursor.execute(query, firstName, lastName, degreeUser, workGroupType, password)
            self.dbCursor.commit()
            
            self.eventHandler()
            self.close()
            
    class EditUserWindow(AddUserWindow):
        def __init__(self, userID : int,  eventHandler, cursor: pyodbc.Cursor) -> None:
            super().__init__(eventHandler, cursor)
            self.userID = userID
            self.setWindowTitle(f'کاربر {self.userID}')
            
            self.userInfo = self.getInfo()
            self.firstNameInput.setText(self.userInfo[0])
            self.lastNameInput.setText(self.userInfo[1])
            self.degreeCombo.setCurrentIndex(self.userInfo[2])
            self.workGroupCombo.setCurrentIndex(self.userInfo[3])
            
        def getInfo(self):
            query = """SELECT firstName, lastName, degreeUser, workType
                    FROM users
                    WHERE userId = ?
                """
            self.dbCursor.execute(query, self.userID)
            row = self.dbCursor.fetchone()
            self.dbCursor.execute('SELECT workGroupId FROM workGroup ORDER BY workGroupId;')
            workTypes = self.dbCursor.fetchall()
            for i, workType in enumerate(workTypes):
                if row is not None and workType[0] == row[3]:
                    row = (row[0], row[1], row[2], i)
            if row is not None:
                return row
            exit(2)
        
        def insertInDataBase(self):
            firstName = self.firstNameInput.text()
            lastName = self.lastNameInput.text()
            degreeUser = self.degreeCombo.currentIndex()
            workGroupType = self.groupTypes[self.workGroupCombo.currentIndex()]
            password = self.passwordInput.text()
            print(password)
            if password != '':
                query = """UPDATE users
                        SET firstName = ?,
                            lastName = ?,
                            degreeUser = ?,
                            workType = ?,
                            password = ?
                        WHERE userId = ?;
                    """
                self.dbCursor.execute(query, firstName, lastName, degreeUser, workGroupType, password, self.userID)
            else:
                query = """UPDATE users
                        SET firstName = ?,
                            lastName = ?,
                            degreeUser = ?,
                            workType = ?
                        WHERE userId = ?;
                    """
                self.dbCursor.execute(query, firstName, lastName, degreeUser, workGroupType, self.userID)
            
            self.dbCursor.commit()
            
            self.eventHandler()
            self.close()
    
    def __init__(self, userID, cursor: pyodbc.Cursor) -> None:
        super().__init__(userID, cursor)
        self.seniorManagerId = userID
        self.dbCursor = cursor
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
        
        query = """
            IF OBJECT_ID('UpdateUserScores', 'P') IS NOT NULL
            DROP PROCEDURE UpdateUserScores;
            """
            
        self.dbCursor.execute(query)
        
        query = """    
            CREATE PROCEDURE UpdateUserScores
            AS
            BEGIN
                -- Declare variables to hold the calculated scores with higher precision
                DECLARE @userId INT, @weeklyScore DECIMAL(18, 4), @monthlyScore DECIMAL(18, 4), @yearlyScore DECIMAL(18, 4);

                -- Cursor to iterate through each user
                DECLARE user_cursor CURSOR FOR
                SELECT userId FROM users WHERE degreeUser = 0;

                OPEN user_cursor;
                FETCH NEXT FROM user_cursor INTO @userId;

                WHILE @@FETCH_STATUS = 0
                BEGIN
                    -- Calculate weekly score
                    SELECT @weeklyScore = ISNULL(CAST(SUM(score * importance) AS DECIMAL(18, 4)) / NULLIF(SUM(importance), 0), 0)
                    FROM works
                    WHERE w_employee_do = @userId
                    AND w_start_datetime >= DATEADD(week, DATEDIFF(week, 0, GETDATE()), 0)
                    AND w_start_datetime < DATEADD(week, DATEDIFF(week, 0, GETDATE()) + 1, 0);

                    -- Calculate monthly score
                    SELECT @monthlyScore = ISNULL(CAST(SUM(score * importance) AS DECIMAL(18, 4)) / NULLIF(SUM(importance), 0), 0)
                    FROM works
                    WHERE w_employee_do = @userId
                    AND w_start_datetime >= DATEADD(month, DATEDIFF(month, 0, GETDATE()), 0)
                    AND w_start_datetime < DATEADD(month, DATEDIFF(month, 0, GETDATE()) + 1, 0);

                    -- Calculate yearly score
                    SELECT @yearlyScore = ISNULL(CAST(SUM(score * importance) AS DECIMAL(18, 4)) / NULLIF(SUM(importance), 0), 0)
                    FROM works
                    WHERE w_employee_do = @userId
                    AND w_start_datetime >= DATEADD(year, DATEDIFF(year, 0, GETDATE()), 0)
                    AND w_start_datetime < DATEADD(year, DATEDIFF(year, 0, GETDATE()) + 1, 0);

                    -- Update the user table with the calculated scores, rounding to 2 decimal places
                    UPDATE users
                    SET weeklyScore = ROUND(@weeklyScore, 4),
                        monthlyScore = ROUND(@monthlyScore, 4),
                        yearlyScore = ROUND(@yearlyScore, 4)
                    WHERE userId = @userId;

                    FETCH NEXT FROM user_cursor INTO @userId;
                END;

                CLOSE user_cursor;
                DEALLOCATE user_cursor;
            END;
            """
        self.dbCursor.execute(query)
        self.dbCursor.commit()

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
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(5)
        for row in works:
            partWidget = QWidget()
            partWidget.setProperty('class', 'title')
            partLayout = QHBoxLayout()
            partLayout.setDirection(QHBoxLayout.Direction.RightToLeft)
            partLayout.setSpacing(2)
            for i in range(len(row)):
                label = None
                if i == len(row) - 1 and type(row[i]) != str:
                    massage = None
                    if row[i] == 0:
                        massage = "عدم بررسی"
                        partWidget.setProperty('class', 'noSeeRecords')
                    elif row[i] == 2:
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
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
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
                        isManager = True
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
        # 0 for not checked, 1 for rejected, 2 for accepted
        workTypeToShow = self.workStatusSelect.currentIndex()

        query = ''
        # if check show just 50 lastest work (sort by update date)
        if self.showNum.isChecked():
            if workTypeToShow == 0:
                query = """SELECT TOP 50 w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_employee_do, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 0
                            ORDER BY w_id DESC;
                        """
            elif workTypeToShow == 1:
                query = """SELECT TOP 50 w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_employee_do, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 1
                            ORDER BY w_id DESC;
                        """
            else:
                query = """SELECT TOP 50 w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_employee_do, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 2
                            ORDER BY w_id DESC;
                        """
        else:
            if workTypeToShow == 0:
                query = """SELECT w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_employee_do, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 0
                            ORDER BY w_id DESC;
                        """
            elif workTypeToShow == 1:
                query = """SELECT w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_employee_do, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 1
                            ORDER BY w_id DESC;
                        """
            else:
                query = """SELECT w_id, w_name, updateDateTime, w_start_datetime,
                            w_end_datetime, importance, score, w_employee_do, w_manager_do, w_status
                            FROM works
                            WHERE w_status = 2
                            ORDER BY w_id DESC;
                        """
            
        self.dbCursor.execute(query)
        rows = self.dbCursor.fetchall()
        
        jalaliRows = []
        for row in rows:
            jalali_row = list(row)
            jalali_row[2] = jdatetime.datetime.fromgregorian(datetime=row[2]).strftime('%d %b %Y\n%H:%M:%S')
            jalali_row[3] = jdatetime.datetime.fromgregorian(datetime=row[3]).strftime('%d %b %Y\n%H:%M:%S')
            jalali_row[4] = jdatetime.datetime.fromgregorian(datetime=row[4]).strftime('%d %b %Y\n%H:%M:%S')
            jalaliRows.append(jalali_row)
        
        workInfoTitles = ("شماره کار", "نام کار", "زمان ویرایش", "شروع","پایان", "اهمیت کار", "نمره کار", "کارمند انجام دهنده", "مدیر آخرین ویرایش", "وضیعت تایید")
        jalaliRows.insert(0, workInfoTitles)
        return jalaliRows

    def getUsers(self):
        # 0 for not checked, 1 for rejected, 2 for accepted
        userTypeToShow = self.usersType.currentIndex()

        query = ''
        # if check show just 50 lastest work (sort by update date)
        if self.showNum.isChecked():
            if userTypeToShow == 0:
                query = """SELECT TOP 50 userId, firstName, lastName,
                            workType, weeklyScore, monthlyScore, yearlyScore, degreeUser
                            FROM users
                            WHERE degreeUser = 0
                            ORDER BY userId;
                        """
            elif userTypeToShow == 1:
                query = """SELECT TOP 50 userId, firstName, lastName,
                            workType, weeklyScore, monthlyScore, yearlyScore, degreeUser
                            FROM users
                            WHERE degreeUser = 1
                            ORDER BY userId;
                        """
            else:
                query = """SELECT TOP 50 userId, firstName, lastName,
                            workType, weeklyScore, monthlyScore, yearlyScore, degreeUser
                            FROM users
                            WHERE degreeUser = 2
                            ORDER BY userId;
                        """
        else:
            if userTypeToShow == 0:
                query = """SELECT TOP 50 userId, firstName, lastName,
                            workType, weeklyScore, monthlyScore, yearlyScore, degreeUser
                            FROM users
                            WHERE degreeUser = 0
                            ORDER BY userId;
                        """
            elif userTypeToShow == 1:
                query = """SELECT TOP 50 userId, firstName, lastName,
                            workType, weeklyScore, monthlyScore, yearlyScore, degreeUser
                            FROM users
                            WHERE degreeUser = 1
                            ORDER BY userId;
                        """
            else:
                query = """SELECT TOP 50 userId, firstName, lastName,
                            workType, weeklyScore, monthlyScore, yearlyScore, degreeUser
                            FROM users
                            WHERE degreeUser = 2
                            ORDER BY userId;
                        """
            
        self.dbCursor.execute(query)
        rows = self.dbCursor.fetchall()
        
        userInfoTitle = ("شماره کاربر", "نام کاربر", "نام خانوادگی کاربر", "نوع کار کاربر","امتیاز هفتگی", "امتیاز ماهانه", "امتیاز سالانه", "نوع کاربر")
        rows.insert(0, userInfoTitle)
        return rows

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
        self.addUserWindow = self.AddUserWindow(self.updateTable, self.dbCursor)
        self.addUserWindow.show()

    def editUser(self, userID):
        self.editUserWindow = self.EditUserWindow(userID, self.updateTable, self.dbCursor)
        self.editUserWindow.idLabel.setText(f"شماره کاربر: {userID}")
        self.editUserWindow.idLabel.setHidden(False)
        self.editUserWindow.show()

    def showUserWork(self, userID):
        self.employeeWindow = EmployeeWindow(userID, self.dbCursor, self.removeUserEditWork)
        self.employeeWindow.show()
        self.employeeWindow.addWorkBtn.setHidden(True)
    
    def removeUserEditWork(self, employeeWindow):
        for buttons in employeeWindow.findChildren(QPushButton, 'employeeWorkEditBtn'):
            buttons.setHidden(True)
        for label in employeeWindow.findChildren(QLabel, 'employeeWorkEditBtn'):
            label.setHidden(True)
    
    def updateScores(self):
        query = "EXEC UpdateUserScores;"
        self.dbCursor.execute(query)
        self.dbCursor.commit()
        self.updateTable()

    def showMeanOfScores(self):
        self.scoresMeanWindow = ShowScoreWindow(self.dbCursor)
        self.scoresMeanWindow.show()

if __name__ == '__main__':
    # Define the connection parameters
    server = 'localhost'
    database = 'workManager'
    username = 'SA'
    password = 'YourStrong@Passw0rd'

    # Create the connection string
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = None
    cursor = None
    try:
        # Establish the connection
        conn = pyodbc.connect(connection_string)
        print("Connected to SQL Server successfully!")

        # Create a cursor object
        cursor = conn.cursor()
    except pyodbc.Error as e:
        print("Error connecting to SQL Server:", e)
        exit(1)
    themeList = list_themes()
    app = QApplication(sys.argv)
    
    if cursor is not None:  
        window = LoginWindow(cursor)
        window.show()
        
    
    apply_stylesheet(app, theme=themeList[11], css_file='custom.css')

    exitCode = app.exec()

    if cursor is not None and conn is not None:  
        cursor.close()
        conn.close()
    print(f"program finished, status code {exitCode}")
    sys.exit(exitCode)
    
    
    
    
    
    
    
    
    
    
    