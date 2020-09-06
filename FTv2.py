from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pynput.keyboard import Key, Controller
import sqlite3
import os
import shutil

conn = sqlite3.connect('MainDatabase.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS tableTracker(
            TABLENAME TEXT)''')
conn.commit()
conn.close()

def createTable(tableName):
    conn = sqlite3.connect('MainDatabase.db')
    c = conn.cursor()
    createTableString = '''CREATE TABLE IF NOT EXISTS "{}"(
        CHK TEXT,
        ORDER_DATE TEXT, 
        DESCR TEXT,
        AMOUNT REAL)'''
    tempTabStr = createTableString.format(tableName)
    c.execute(tempTabStr)
    tempTabStr = "INSERT INTO tableTracker (TABLENAME) VALUES ('{}')".format(tableName)
    c.execute(tempTabStr)
    conn.commit()
    conn.close()
    return True


def tableListFiller():
    conn = sqlite3.connect('MainDatabase.db')
    c = conn.cursor()
    data = c.execute('SELECT TABLENAME FROM tableTracker')
    data = c.fetchall()
    set = []
    for i in range(len(data)):
        set.append(data[i][0])
    return set


def FixSyntax(m):
    p = str(round(m, 2))
    n = p.replace("-", "")
    if '.' in n:
        dollars, cents = n.split('.')
    else:
        dollars = n
        cents = None

    r = []
    for i, c in enumerate(str(dollars)[::-1]):
        if i and (not(i % 3)):
            r.insert(0, ',')
        r.insert(0,c)
    fixer = ''.join(r)
    if cents:
        fixer += '.' + cents

    if m > 0:
        output = fixer
    else:
        output = "(" + fixer + ")"

    if fixer.find(".01") < 0 and fixer.find(".02") < 0 and fixer.find(".03") < 0:
        if fixer.find(".04") < 0 and fixer.find(".05") < 0 and fixer.find(".06") < 0 and fixer.find(".07") < 0:
            if fixer.find(".08") < 0 and fixer.find(".09") < 0:
                if fixer.find(".0") > 0:
                    if m > 0:
                        output = fixer + "0"
                    else:
                        output = "(" + fixer + "0)"

    if '.' in fixer:
        dollars, cents = fixer.split('.')
    else:
        dollars, cents = fixer, None

    if cents == "1":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    if cents == "2":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    if cents == "3":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    if cents == "4":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    if cents == "5":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    if cents == "6":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    if cents == "7":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    if cents == "8":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    if cents == "9":
        if m > 0:
            output = fixer + "0"
        else:
            output = "(" + fixer + "0" + ")"

    return output


def FixDate(tempDate):
    month, day, year = tempDate.split('/')

    month = int(month)
    day = int(day)

    if month > 0 and month < 10:
        month = str(month)
        month = '0' + month

    if day > 0 and day < 10:
        day = str(day)
        day = '0' + day

    month = str(month)
    day = str(day)

    final = month + '/' + day + '/' + year
    return final


def SyntaxCorrectorList(dataList, coloumn):
    newList = []
    for i in range(len(dataList)):
        templist = []
        for j in range(len(dataList[i])):
            temp = str(dataList[i][j])
            templist.append(temp)
        newList.append(templist)

    for k in range(len(dataList)):
        tempAmt = dataList[k][coloumn]
        amt = FixSyntax(tempAmt)
        newList[k][coloumn] = amt

    for p in range(len(dataList)):
        dateStr = FixDate(dataList[p][1])
        newList[p][1] = dateStr

    return newList


def dateFilter(dateRange, dataList):
    indexList = []
    returnList = []
    tempRange = dateRange.replace(' ', '')
    startDate, endDate = tempRange.split('-')
    Smonth, Sday, Syear = startDate.split('/')
    Emonth, Eday, Eyear = endDate.split('/')
    Smonth = int(Smonth)
    Sday = int(Sday)
    Syear = int(Syear)
    Emonth = int(Emonth)
    Eday = int(Eday)
    Eyear = int(Eyear)

    for i in range(len(dataList)):
        tempComparedDate = dataList[i][1]
        Tmonth, Tday, Tyear = tempComparedDate.split('/')
        Tmonth = int(Tmonth)
        Tday = int(Tday)
        Tyear = int(Tyear)
        if Syear < Tyear and Tyear < Eyear:
            indexList.append(i)
        elif Syear == Tyear or Tyear == Eyear:
            if Smonth < Tmonth and Tmonth < Emonth:
                indexList.append(i)
            elif Tmonth < Smonth:
                if Tyear > Syear:
                    indexList.append(i)
            elif Tmonth > Emonth:
                if Tyear < Eyear:
                    indexList.append(i)
            elif Smonth == Tmonth or Emonth == Tmonth:
                if Sday < Tday and Tday < Eday:
                    indexList.append(i)
                elif Sday == Tday or Tday == Eday:
                    indexList.append(i)

    for i in indexList:
        returnList.append(dataList[i])

    return returnList


def findIndex(tableName):
    conn = sqlite3.connect('MainDatabase.db')
    c = conn.cursor()
    data = c.execute('SELECT TABLENAME FROM tableTracker')
    data = c.fetchall()
    set = []
    for i in range(len(data)):
        set.append(data[i][0])

    returner = 99999

    for i in range(len(set)):
        if set[i] == tableName:
            returner = i

    return returner

def createDataTableListRAW(currentTable, keyword):
    conn = sqlite3.connect('MainDatabase.db')
    c = conn.cursor()
    if currentTable == "":
        data = []
        return data

    if len(keyword) == 0:
        tempString = "SELECT * FROM '{}'"
        data = c.execute(tempString.format(currentTable))
        data = c.fetchall()
    else:
        tempString = "SELECT * FROM '{}' WHERE DESCR LIKE '%" + keyword + "%'"
        data = c.execute(tempString.format(currentTable))
        data = c.fetchall()

    return data


class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignRight

class UpdateAccWindow(QtWidgets.QWidget):

    finder = QtCore.pyqtSignal(str)

    def __init__(self, currentAccount):
        super().__init__()
        self.setObjectName("UpdateAccNameWin")
        self.resize(487, 150)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.AccNameLab = QtWidgets.QLabel(self.centralwidget)
        self.AccNameLab.setGeometry(QtCore.QRect(40, 30, 110, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.AccNameLab.setFont(font)
        self.AccNameLab.setObjectName("startDateLab")
        self.NameHolder = QtWidgets.QLabel(self.centralwidget)
        self.NameHolder.setGeometry(QtCore.QRect(1000, 1000, 1000, 1000))
        self.NameHolder.setFont(font)
        self.NameHolder.setObjectName("NameHolder")
        self.AccNameText = QtWidgets.QLineEdit(self.centralwidget)
        self.AccNameText.setGeometry(QtCore.QRect(170, 28, 281, 22))
        self.AccNameText.setObjectName("startDateText")
        self.AccNameText.returnPressed.connect(self.onSubmit)
        self.UpdateButton = QtWidgets.QPushButton(self.centralwidget)
        self.UpdateButton.setGeometry(QtCore.QRect(152, 80, 201, 45))
        self.UpdateButton.clicked.connect(self.onSubmit)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.UpdateButton.setFont(font)
        self.UpdateButton.setObjectName("selectButton")
        self.retranslateUi(self, currentAccount)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.AccNameText.setText(currentAccount)

    def EmptyTableAddEr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please enter an account name.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def newTableNameEr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Account Name already in use.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def onSubmit(self):
        AccNameString = self.NameHolder.text()
        AccNameFix = AccNameString.replace(" ", "_")
        newType = self.AccNameText.text()
        newTypeFix = newType.replace(" ", "_")
        comparethisName = AccNameString.replace(" ", "_")

        if newTypeFix != AccNameFix:
            length = len(newType)
            if length == 0:
                self.EmptyTableAddEr()
                return
            tableNameList = tableListFiller()
            indexedAcc = findIndex(AccNameFix)
            if indexedAcc != 99999:
                tableNameList[indexedAcc] = "__BLANK__!"
            for i in tableNameList:
                if i == newTypeFix:
                    self.newTableNameEr()
                    return

            self.finder.emit(newType)

        self.close()

    def closer(self):
        self.close()

    def retranslateUi(self, UpdateAccNameWin, name):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("UpdateAccNameWin", "Update Account Name"))
        self.AccNameLab.setText(_translate("UpdateAccNameWin", "Account Name:"))
        self.UpdateButton.setText(_translate("UpdateAccNameWin", "Update"))
        self.NameHolder.setText(_translate("UpdateAccNameWin", name))


class DialogWindow(QtWidgets.QWidget):

    submitted = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setObjectName("rangeWindow")
        self.resize(487, 225)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.startDateLab = QtWidgets.QLabel(self.centralwidget)
        self.startDateLab.setGeometry(QtCore.QRect(40, 30, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.startDateLab.setFont(font)
        self.startDateLab.setObjectName("startDateLab")
        self.endDateLab = QtWidgets.QLabel(self.centralwidget)
        self.endDateLab.setGeometry(QtCore.QRect(40, 80, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.endDateLab.setFont(font)
        self.endDateLab.setObjectName("endDateLab")
        self.startDateText = QtWidgets.QLineEdit(self.centralwidget)
        self.startDateText.setGeometry(QtCore.QRect(170, 30, 281, 22))
        self.startDateText.setObjectName("startDateText")
        self.startDateText.returnPressed.connect(self.tabNext2)
        self.endDateText = QtWidgets.QLineEdit(self.centralwidget)
        self.endDateText.setGeometry(QtCore.QRect(170, 80, 281, 22))
        self.endDateText.setObjectName("endDateText")
        self.endDateText.returnPressed.connect(self.onSubmit)
        self.selectButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectButton.setGeometry(QtCore.QRect(152, 140, 201, 51))
        self.selectButton.clicked.connect(self.onSubmit)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.selectButton.setFont(font)
        self.selectButton.setObjectName("selectButton")
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def badDateMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Check Date Syntax.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def fakeDateMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Invalid date.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def timeIssue(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Verify logic of given time range.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def tabNext2(self):
        keyboard = Controller()
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)

    def retranslateUi(self, DialogWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("rangeWindow", "Select Range"))
        self.startDateLab.setText(_translate("rangeWindow", "Start Date:"))
        self.endDateLab.setText(_translate("rangeWindow", "End Date:"))
        self.selectButton.setText(_translate("rangeWindow", "Select"))

    def checkTime(self, startDate, endDate):
        if '/' in startDate:
            Smonth, Sday, Syear = startDate.split('/')

        if '/' in endDate:
            Emonth, Eday, Eyear = endDate.split('/')

        if Eyear < Syear:
            self.timeIssue()
            return True

        if Eyear == Syear:
            if Emonth < Smonth:
                self.timeIssue()
                return True
            if Emonth == Smonth:
                if Eday < Sday:
                    self.timeIssue()
                    return True

        return False


    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        startDate = str(self.startDateText.text())
        endDate = str(self.endDateText.text())

        if len(startDate) == 0 or len(endDate) == 0:
            startDate = "None"
            endDate = "None"

        self.submitted.emit(startDate, endDate)


    def onSubmit(self):
        startDate = str(self.startDateText.text())
        endDate = str(self.endDateText.text())

        if len(startDate) == 0 or len(endDate) == 0:
            Ui_win.syntaxEr(self)
            return

        if Ui_win.dateSyntax(self, startDate):
            return
        if Ui_win.dateSyntax(self, endDate):
            return

        if self.checkTime(startDate, endDate):
            return

        self.submitted.emit(startDate, endDate)
        self.close()


class Ui_win(object):

    def updateDates(self, startDateTest, endDateTest):
        if startDateTest == "None":
            self.rangeLabel.setText("")
            self.dateRangeBox.toggle()
            return
        self.STARTdate = FixDate(startDateTest)
        self.ENDdate = FixDate(endDateTest)
        string = self.STARTdate + " - " + self.ENDdate
        self.rangeLabel.setText(string)
        self.loadData()

    def updateAccName(self, AccNameString):
        newAccountString = AccNameString.replace(" ", "_")
        oldTableName = self.ChkDropList.currentText()
        oldTableNameFix = oldTableName.replace(" ", "_")

        conn = sqlite3.connect('MainDatabase.db')
        c = conn.cursor()
        executeString = "ALTER TABLE " + oldTableNameFix + " RENAME TO " + newAccountString
        data = c.execute(executeString)
        conn.commit()
        conn.close()
        self.updatey(newAccountString, oldTableNameFix)
        self.UpdateTableDrops()

    def updatey(self, newName, oldName):
        conn = sqlite3.connect('MainDatabase.db')
        c = conn.cursor()
        executeString = "UPDATE tableTracker SET TABLENAME=? WHERE TABLENAME=?"
        data = c.execute(executeString, (newName, oldName))
        conn.commit()
        conn.close()

    def callAccNameUpdate(self):
        tempCurrTable = self.ChkDropList.currentText()
        self.dialog = UpdateAccWindow(tempCurrTable)
        self.dialog.finder.connect(self.updateAccName)
        self.dialog.show()

    def createRangeWindow(self):
        if self.dateRangeBox.isChecked():
            self.dialog = DialogWindow()
            self.STARTdate = ""
            self.ENDdate = ""
            self.dialog.submitted.connect(self.updateDates)
            self.dialog.show()
        else:
            self.rangeLabel.setText("")


    def EmptyTableAddEr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please enter an account name.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def BackupMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Sucess")
        msg.setText("Information is successfully backed-up.")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def IdUsedEr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("ID is already in use for this account.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def chooseExistingIdEr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Choose an existing ID to select. ")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def emptyIdEr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Enter a ID.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def badDateMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Check Date Syntax.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def fakeDateMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Invalid date.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def goodInsertMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Successfully saved entry!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def goodUpdateMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Successfully updated entry!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def goodDelTableMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Successfully deleted account!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def goodDeleteMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Successfully deleted entry!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def tableAddedMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Successfully added account!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    def syntaxEr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Check Syntax or make sure fields are filled.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def badYearMsg(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Check year syntax.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def newTableNameEr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Account Name already in use.")
        msg.setIcon(QMessageBox.Warning)
        x = msg.exec_()

    def showAskAgain(self):
        tempCurrTable = self.ChkDropList.currentText()
        msg = QMessageBox()
        msg.setWindowTitle("Delete Table?")
        msg.setText("Are you sure you want to delete account: " + tempCurrTable +"?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        msg.buttonClicked.connect(self.deleteTable)
        x = msg.exec_()

    def tabNext(self):
        keyboard = Controller()

        keyboard.press(Key.tab)
        keyboard.release(Key.tab)

    def isIdUsed(self, tableName, id):
        conn = sqlite3.connect('MainDatabase.db')
        c = conn.cursor()
        tempStr = "SELECT CHK FROM '{}'"
        compare = c.execute(tempStr.format(tableName))
        compare = c.fetchall()
        counter = 0
        for i in range(len(compare)):
            idComp = compare[i][0]
            if idComp == id:
                return True
        return False

    def syntaxRestCheck(self):
        tempId = str(self.chkText.text())
        tempDate = str(self.dateText.text())
        tempAmt = str(self.amtText.text())
        tempDesc = str(self.descText.text())

        if len(tempId) == 0:
            return True
        if len(tempDate) == 0:
            return True
        if len(tempAmt) == 0:
            return True
        if len(tempDesc) == 0:
            return True

        new = tempAmt.replace(".", "")
        for i in new:
            if i.isdigit() == False:
                if i != '-':
                    return True
        return False

    def clearEntries(self):
        self.chkText.clear()
        self.dateText.clear()
        self.amtText.clear()
        self.descText.clear()

    def UpdateTableDrops(self):
        tempCurrTable = self.ChkDropList.currentText()
        currTable = tempCurrTable.replace(" ", "_")
        counter = 0
        savedIndex = 999999

        List = tableListFiller()
        for i in range(len(List)):
            compared = List[i]
            if compared == currTable:
                savedIndex = i
                counter = 1

        if counter != 1:
            self.ChkDropList.clear()
            for i in range(len(List)):
                temp = List[i]
                tempName = temp.replace("_", " ")
                self.ChkDropList.addItem("")
                self.ChkDropList.setItemText(i, tempName)
        elif counter == 1:
            self.ChkDropList.clear()
            for i in range(len(List)):
                temp = List[i]
                tempName = temp.replace("_", " ")
                self.ChkDropList.addItem("")
                self.ChkDropList.setItemText(i, tempName)
                if savedIndex != 999999:
                    self.ChkDropList.setCurrentIndex(savedIndex)



    def AddTable(self):
        tableName = str(self.addTableText.text())
        fixedTableName = tableName.replace(" ", "_")
        length = len(fixedTableName)
        if length == 0:
            self.EmptyTableAddEr()
            return
        tableNameList = tableListFiller()
        for i in tableNameList:
            if i == fixedTableName:
                self.newTableNameEr()
                return
        createTable(fixedTableName)
        self.UpdateTableDrops()
        self.tableAddedMsg()
        self.addTableText.clear()

    def refixCol(self):
        self.DataDisplay.setRowCount(0)
        self.DataDisplay.setRowCount(10000)

        for i in range(10000):
            self.DataDisplay.setRowHeight(i,5)

        self.DataDisplay.setColumnWidth(0, 100)
        self.DataDisplay.setColumnWidth(1, 120)
        self.DataDisplay.setColumnWidth(2, 360)
        self.DataDisplay.setColumnWidth(3, 170)

    def findBal(self, data):
        bal = 0
        for i in range(len(data)):
            bal += data[i][3]
        return bal

    def loadData(self):
        tempCurrTable = self.ChkDropList.currentText()
        currTable = tempCurrTable.replace(" ", "_")
        keyword = str(self.keywordText.text())

        rawData = createDataTableListRAW(currTable, keyword)

        rangeSet = self.rangeLabel.text()
        if self.dateRangeBox.isChecked():
            dateFilteredData = dateFilter(rangeSet, rawData)
            rawData = dateFilteredData

        data = SyntaxCorrectorList(rawData, 3)

        self.refixCol()
        for i in range(len(data)):
            for j in range(len(data[i])):
                display = QtWidgets.QTableWidgetItem(str(data[i][j]))
                self.DataDisplay.setItem(i, j, display)

        raw_bal = self.findBal(rawData)
        printBal = FixSyntax(raw_bal)

        if printBal[0] == "(":
            printBalNew = printBal.replace('(' , '($')
        else:
            printBalNew = "$" + printBal

        self.balanceText.setText(printBalNew)

    def reloadButtonfunc(self):
        self.loadData()

        index = self.DataDisplay.model().index(0, 0)
        self.DataDisplay.scrollTo(index)

    def totalLoad(self):
        self.UpdateTableDrops()
        self.loadData()

    def dateSyntax(self, dateString):
        normMonthDayList = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        leapMonthDayList = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        splitCounter = 0

        for i in dateString:
            if i.isdigit() == False:
                if i != '/':
                    self.badDateMsg()
                    return True
                else:
                    splitCounter = splitCounter + 1

        if splitCounter != 2:
            self.badDateMsg()
            return True

        if '/' in dateString:
            month, day, year = dateString.split('/')

        if len(year) != 2:
            self.badYearMsg()
            return True

        month = int(month)
        day = int(day)
        year = int(year)

        leapYear = False
        if (year % 4) == 0:
            leapYear = True

        if month < 1 or month > 12:
            self.fakeDateMsg()
            return True

        if leapYear == True:
            endDate = leapMonthDayList[month - 1]
        else:
            endDate = normMonthDayList[month - 1]

        if day < 1 or day > endDate:
            self.fakeDateMsg()
            return True

        return False

    def saveFunc(self):
        tempCurrTable = self.ChkDropList.currentText()
        currTable = tempCurrTable.replace(" ", "_")
        id = str(self.chkText.text())
        dateStr = str(self.dateText.text())

        if self.isIdUsed(currTable,id):
            self.IdUsedEr()
            self.chkText.clear()
            return

        if self.dateSyntax(dateStr):
            return

        if self.syntaxRestCheck():
            self.syntaxEr()
            return

        tempId = str(self.chkText.text())
        tempDate = str(self.dateText.text())
        tempAmt = float(self.amtText.text())
        tempDesc = str(self.descText.text())

        conn = sqlite3.connect('MainDatabase.db')
        c = conn.cursor()
        temptableStr = "INSERT INTO '{}' (CHK, ORDER_DATE, DESCR, AMOUNT) VALUES (?,?,?,?)"
        c.execute(temptableStr.format(currTable), (tempId, tempDate, tempDesc, tempAmt))
        conn.commit()
        c.close()
        self.goodInsertMsg()
        self.clearEntries()
        self.totalLoad()
        self.scrollBottom()

    def selectIdFunc(self):
        tempCurrTable = self.ChkDropList.currentText()
        currTable = tempCurrTable.replace(" ", "_")
        id = str(self.chkText.text())

        if len(id) == 0:
            self.emptyIdEr()
            return

        if self.isIdUsed(currTable,id) == False:
            self.chooseExistingIdEr()
            self.chkText.clear()
            return

        conn = sqlite3.connect('MainDatabase.db')
        c = conn.cursor()
        tempStr = "SELECT * FROM '{}' WHERE CHK LIKE '" + id + "'"
        compare = c.execute(tempStr.format(currTable))
        compare = c.fetchall()
        self.dateText.setText(str(compare[0][1]))
        self.descText.setText(str(compare[0][2]))
        self.amtText.setText(str(compare[0][3]))

    def updateFunc(self):
        tempCurrTable = self.ChkDropList.currentText()
        currTable = tempCurrTable.replace(" ", "_")
        id = str(self.chkText.text())
        dateStr = str(self.dateText.text())

        if len(id) == 0:
            self.emptyIdEr()
            return

        if self.isIdUsed(currTable,id) == False:
            self.chooseExistingIdEr()
            self.chkText.clear()
            return

        if self.dateSyntax(dateStr):
            return

        if self.syntaxRestCheck():
            self.syntaxEr()
            return

        tempDate = str(self.dateText.text())
        tempChk = str(self.chkText.text())
        tempAmt = str(self.amtText.text())
        tempDesc = str(self.descText.text())

        conn = sqlite3.connect('MainDatabase.db')
        c = conn.cursor()
        tempString = "UPDATE '{}' SET ORDER_DATE=(?),DESCR=(?),AMOUNT=(?) WHERE CHK=(?)"
        c.execute(tempString.format(currTable), (tempDate, tempDesc,tempAmt, tempChk))
        conn.commit()
        c.close()
        self.clearEntries()
        self.goodUpdateMsg()
        self.totalLoad()

    def deleteFunc(self):
        tempCurrTable = self.ChkDropList.currentText()
        currTable = tempCurrTable.replace(" ", "_")
        id = str(self.chkText.text())

        if len(id) == 0:
            self.emptyIdEr()
            return

        if self.isIdUsed(currTable,id) == False:
            self.chooseExistingIdEr()
            self.chkText.clear()
            return

        conn = sqlite3.connect('MainDatabase.db')
        c = conn.cursor()
        tempString = "DELETE FROM '{}' WHERE CHK=?"
        c.execute(tempString.format(currTable), (id,))
        conn.commit()
        c.close()
        self.clearEntries()
        self.goodDeleteMsg()
        self.loadData()

    def deleteTable(self, i):
        answer = (str(i.text())).replace("&", "")

        if answer == "Yes":
            tempCurrTable = self.ChkDropList.currentText()
            currTable = tempCurrTable.replace(" ", "_")
            list = tableListFiller()
            for table in list:
                if table == currTable:
                    conn = sqlite3.connect('MainDatabase.db')
                    c = conn.cursor()
                    tempString = "DROP TABLE IF EXISTS '{}'"
                    c.execute(tempString.format(currTable))
                    tempString = "DELETE FROM tableTracker WHERE TABLENAME=?"
                    c.execute(tempString, (currTable,))
                    conn.commit()
                    c.close()
                    self.goodDelTableMsg()
                    self.totalLoad()
                    self.scrollBottom()
                    self.clearEntries()
        elif answer == "No":
            return

    def scrollBottom(self):
        tempCurrTable = self.ChkDropList.currentText()
        currTable = tempCurrTable.replace(" ", "_")
        keyword = str(self.keywordText.text())

        rawData = createDataTableListRAW(currTable, keyword)

        rangeSet = self.rangeLabel.text()
        if self.dateRangeBox.isChecked():
            dateFilteredData = dateFilter(rangeSet, rawData)
            rawData = dateFilteredData

        data = SyntaxCorrectorList(rawData, 3)
        length = len(data)

        if (length > 18) and (length < 9995):
            index = self.DataDisplay.model().index(length+5, 0)
            self.DataDisplay.scrollTo(index)
        else:
            index = self.DataDisplay.model().index(0, 0)
            self.DataDisplay.scrollTo(index)



    def openPdf(self):
        import os
        os.startfile('pdfTable.pdf')

    def exportFunc(self, reportlab=None):
        tempCurrTable = self.ChkDropList.currentText()
        currTable = tempCurrTable.replace(" ", "_")
        keyword = str(self.keywordText.text())

        rawData = createDataTableListRAW(currTable, keyword)

        rangeSet = self.rangeLabel.text()
        if self.dateRangeBox.isChecked():
            dateFilteredData = dateFilter(rangeSet, rawData)
            rawData = dateFilteredData

        # FINAL NICE DATA
        data = SyntaxCorrectorList(rawData, 3)

        self.refixCol()
        for i in range(len(data)):
            for j in range(len(data[i])):
                display = QtWidgets.QTableWidgetItem(str(data[i][j]))
                self.DataDisplay.setItem(i, j, display)

        raw_bal = self.findBal(rawData)
        # FINAL BALANCE
        printBal = FixSyntax(raw_bal)

        header = [['  Check ID  ', '    Date    ', ' Description ', '   Amount   ']]
        ender = [['-', '-', '-', 'Total: ' + printBal]]
        printInfo = header + data + ender

        fileName = 'pdfTable.pdf'

        from reportlab.platypus import SimpleDocTemplate
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import Table

        pdf = SimpleDocTemplate(
            fileName,
            pagesize=letter
        )

        table = Table(printInfo, repeatRows=1)

        # add style
        from reportlab.platypus import TableStyle
        from reportlab.lib import colors

        # Basic Coloring
        style = TableStyle([
            ('BACKGROUND', (0, 0), (3, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('ALIGN', (0, -1), (3, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (2, -1), 'LEFT'),

            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ])
        table.setStyle(style)

        ts = TableStyle(
            [
                ('BOX', (0, 0), (-1, -1), 2, colors.black),

                ('LINEBEFORE', (2, 1), (2, -1), 2, colors.red),
                ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),

                ('GRID', (0, 1), (-1, -1), 2, colors.black),
            ]
        )
        table.setStyle(ts)

        elems = []
        elems.append(table)

        pdf.build(elems)
        self.openPdf()

    def ClearOldBackup(self, currentDir):
        try:
            shutil.rmtree(currentDir + "/BackupData")
        except:
            pass

    def backupFunc(self):

        DATA = "MainDatabase.db"
        NEWNAME = "BACKUP.db"

        # Remove the old BackupData Folder/set current Directory
        currentDir = os.getcwd()

        # Some String Clearing
        self.ClearOldBackup(currentDir)

        # Create the fresh BackupData in Folder
        try:
            backupLocation = os.mkdir('BackupData')
        except:
            pass

        os.listdir()

        # Creation of the location of the BackupLocation Link
        backupLocation = currentDir + "/BackupData"

        # This is the link of what we want to copy
        origFile = os.path.join(currentDir, DATA)

        # We copy what we want to the Backup Location
        shutil.copy(origFile, backupLocation)

        # The Link of the Backup copy
        backupFile = os.path.join(backupLocation, DATA)

        # We use a preemptive link rename for the Backup location link
        backupFileName = os.path.join(backupLocation, NEWNAME)

        # We push through the rename
        os.rename(backupFile, backupFileName)

        self.BackupMsg()

    def setupUi(self, win):
        win.setObjectName("win")
        win.resize(1362, 754)
        self.centralwidget = QtWidgets.QWidget(win)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 50, 491, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(32)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 180, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 240, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(80, 300, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(70, 360, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(60, 420, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.ChkDropList = QtWidgets.QComboBox(self.centralwidget)
        self.ChkDropList.setGeometry(QtCore.QRect(190, 180, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.ChkDropList.setFont(font)
        self.ChkDropList.setObjectName("ChkDropList")
        self.ChkDropList.activated.connect(self.reloadButtonfunc)
        self.SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveButton.setGeometry(QtCore.QRect(70, 480, 91, 51))
        self.SaveButton.clicked.connect(self.saveFunc)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.SaveButton.setFont(font)
        self.SaveButton.setObjectName("SaveButton")
        self.UpdateButton = QtWidgets.QPushButton(self.centralwidget)
        self.UpdateButton.setGeometry(QtCore.QRect(220, 480, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.UpdateButton.setFont(font)
        self.UpdateButton.setObjectName("UpdateButton")
        self.UpdateButton.clicked.connect(self.updateFunc)
        self.DeleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteButton.setGeometry(QtCore.QRect(370, 480, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DeleteButton.setFont(font)
        self.DeleteButton.setObjectName("DeleteButton")
        self.DeleteButton.clicked.connect(self.deleteFunc)
        self.DataDisplay = QtWidgets.QTableWidget(self.centralwidget)
        self.DataDisplay.setGeometry(QtCore.QRect(510, 190, 821, 451))
        self.DataDisplay.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.DataDisplay.setObjectName("DataDisplay")
        self.DataDisplay.setColumnCount(4)
        self.DataDisplay.setRowCount(0)
        delegate = AlignDelegate(self.DataDisplay)
        self.DataDisplay.setItemDelegateForColumn(3, delegate)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        item.setFont(font)
        self.DataDisplay.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        item.setFont(font)
        self.DataDisplay.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        item.setFont(font)
        self.DataDisplay.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        item.setFont(font)
        self.DataDisplay.setHorizontalHeaderItem(3, item)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1070, 120, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setGeometry(QtCore.QRect(510, 130, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.refreshButton.setFont(font)
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButton.clicked.connect(self.reloadButtonfunc)
        self.scrollButton = QtWidgets.QPushButton(self.centralwidget)
        self.scrollButton.setGeometry(QtCore.QRect(510, 650, 145, 51))
        self.scrollButton.setFont(font)
        self.scrollButton.setObjectName("scrollButton")
        self.scrollButton.clicked.connect(self.scrollBottom)
        self.selectIdButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectIdButton.setGeometry(QtCore.QRect(390, 230, 91, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.selectIdButton.setFont(font)
        self.selectIdButton.setObjectName("selectIdButton")
        self.selectIdButton.clicked.connect(self.selectIdFunc)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(1080, 660, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.balanceText = QtWidgets.QLabel(self.centralwidget)
        self.balanceText.setGeometry(QtCore.QRect(1220, 660, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.balanceText.setFont(font)
        self.balanceText.setText("")
        self.balanceText.setObjectName("balanceText")
        self.exportButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportButton.setGeometry(QtCore.QRect(1260, 20, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.exportButton.setFont(font)
        self.exportButton.setObjectName("exportButton")
        self.exportButton.clicked.connect(self.exportFunc)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(20, 580, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(60, 615, 181, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.AddAccButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddAccButton.setGeometry(QtCore.QRect(370, 611, 95, 31))
        self.AddAccButton.clicked.connect(self.AddTable)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.AddAccButton.setFont(font)
        self.AddAccButton.setObjectName("AddAccButton")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.DelAccButton = QtWidgets.QPushButton(self.centralwidget)
        self.DelAccButton.setGeometry(QtCore.QRect(220, 660, 95, 39))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.DelAccButton.setFont(font)
        self.DelAccButton.setObjectName("DelAccButton")
        self.DelAccButton.clicked.connect(self.showAskAgain)
        self.EditAccButton = QtWidgets.QPushButton(self.centralwidget)
        self.EditAccButton.setGeometry(QtCore.QRect(370, 660, 95, 39))
        self.EditAccButton.setObjectName("EditAccButton")
        self.EditAccButton.setFont(font)
        self.EditAccButton.clicked.connect(self.callAccNameUpdate)
        self.BackupButton = QtWidgets.QPushButton(self.centralwidget)
        self.BackupButton.setGeometry(QtCore.QRect(70, 660, 95, 39))
        self.BackupButton.setObjectName("BackupButton")
        self.BackupButton.setFont(font)
        self.BackupButton.clicked.connect(self.backupFunc)
        self.chkText = QtWidgets.QLineEdit(self.centralwidget)
        self.chkText.setGeometry(QtCore.QRect(190, 240, 161, 22))
        self.chkText.setObjectName("chkText")
        self.chkText.returnPressed.connect(self.selectIdFunc)
        self.dateText = QtWidgets.QLineEdit(self.centralwidget)
        self.dateText.setGeometry(QtCore.QRect(190, 300, 161, 22))
        self.dateText.setObjectName("dateText")
        self.dateText.returnPressed.connect(self.tabNext)
        self.amtText = QtWidgets.QLineEdit(self.centralwidget)
        self.amtText.setGeometry(QtCore.QRect(190, 360, 161, 22))
        self.amtText.setObjectName("amtText")
        self.amtText.returnPressed.connect(self.tabNext)
        self.descText = QtWidgets.QLineEdit(self.centralwidget)
        self.descText.setGeometry(QtCore.QRect(190, 420, 271, 22))
        self.descText.setObjectName("descText")
        self.keywordText = QtWidgets.QLineEdit(self.centralwidget)
        self.keywordText.setGeometry(QtCore.QRect(1070, 150, 251, 22))
        self.keywordText.setObjectName("keywordText")
        self.keywordText.returnPressed.connect(self.reloadButtonfunc)
        self.addTableText = QtWidgets.QLineEdit(self.centralwidget)
        self.addTableText.setGeometry(QtCore.QRect(167, 616, 191, 22))
        self.addTableText.setObjectName("addTableText")
        self.addTableText.returnPressed.connect(self.AddTable)
        self.dateRangeBox = QtWidgets.QCheckBox(self.centralwidget)
        self.dateRangeBox.setGeometry(QtCore.QRect(850, 120, 81, 20))
        self.dateRangeBox.setText("")
        self.dateRangeBox.setObjectName("dateRangeBox")
        self.dateRangeBox.stateChanged.connect(self.createRangeWindow)
        self.dateRangeLabel = QtWidgets.QLabel(self.centralwidget)
        self.dateRangeLabel.setGeometry(QtCore.QRect(873, 120, 131, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.dateRangeLabel.setFont(font)
        self.dateRangeLabel.setObjectName("dateRangeLabel")
        self.rangeLabel = QtWidgets.QLabel(self.centralwidget)
        self.rangeLabel.setGeometry(QtCore.QRect(860, 150, 201, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.rangeLabel.setFont(font)
        self.rangeLabel.setObjectName("rangeLabel")
        win.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(win)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1362, 21))
        self.menubar.setObjectName("menubar")
        win.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(win)
        self.statusbar.setObjectName("statusbar")
        win.setStatusBar(self.statusbar)

        self.retranslateUi(win)
        QtCore.QMetaObject.connectSlotsByName(win)

    def retranslateUi(self, win):
        _translate = QtCore.QCoreApplication.translate
        win.setWindowTitle(_translate("win", "Finance Tracker"))
        self.label.setText(_translate("win", "Financial Tracker"))
        self.label_2.setText(_translate("win", "Checking Account:"))
        self.label_3.setText(_translate("win", "Check ID:"))
        self.label_4.setText(_translate("win", "Date:"))
        self.label_5.setText(_translate("win", "Amount:"))
        self.label_6.setText(_translate("win", "Description:"))
        self.SaveButton.setText(_translate("win", "Save"))
        self.UpdateButton.setText(_translate("win", "Update"))
        self.DeleteButton.setText(_translate("win", "Delete"))
        item = self.DataDisplay.horizontalHeaderItem(0)
        item.setText(_translate("win", "Check ID"))
        item = self.DataDisplay.horizontalHeaderItem(1)
        item.setText(_translate("win", "Date"))
        item = self.DataDisplay.horizontalHeaderItem(2)
        item.setText(_translate("win", "Description"))
        item = self.DataDisplay.horizontalHeaderItem(3)
        item.setText(_translate("win", "Amount"))
        self.label_7.setText(_translate("win", "Keyword:"))
        self.refreshButton.setText(_translate("win", "Refresh Table"))
        self.scrollButton.setText(_translate("win", "Scroll to Bottom"))
        self.selectIdButton.setText(_translate("win", "Select ID"))
        self.label_8.setText(_translate("win", "Balance: "))
        self.exportButton.setText(_translate("win", "Export"))
        self.label_9.setText(_translate("win", "Account Management"))
        self.label_10.setText(_translate("win", "Account Name:"))
        self.AddAccButton.setText(_translate("win", "Add"))
        self.DelAccButton.setText(_translate("win", "Delete"))
        self.EditAccButton.setText(_translate("win", "Edit Name"))
        self.dateRangeLabel.setText(_translate("win", "Date Range"))
        self.BackupButton.setText(_translate("win", "Backup Info"))
        self.rangeLabel.setText(_translate("win", ""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = Ui_win()
    ui.setupUi(win)
    win.show()
    ui.totalLoad()
    sys.exit(app.exec_())
