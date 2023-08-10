from gui import *
from PyQt6.QtWidgets import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Initialization function.
        """
        super().__init__()
        self.setupUi(self)
        self.addStudent_button.clicked.connect(lambda : self.addStudent())
        self.clear_button.clicked.connect(lambda : self.clear())
        self.addAssign_button.clicked.connect(lambda : self.addAssign())
        self.change_button.clicked.connect(lambda : self.changeScore())
        self.removeStudent_button.clicked.connect(lambda : self.removeStudent())
        self.removeAssign_button.clicked.connect(lambda : self.removeAssign())
        self.updateTable()
        self.updateDropdowns()

    def updateTable(self) -> None:
        """
        Function to update table widget.
        """
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)

        data = []
        with open('data.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)

        for n in range(len(data[0])):
            self.tableWidget.insertColumn(n)

        for n in range(len(data)-1):
            self.tableWidget.insertRow(n)

        vert_labels = []
        horizontal_labels = data[0]
        for n in range(len(data)):
            if n == 0:
                continue
            vert_labels.append(data[n][0])

        self.tableWidget.setHorizontalHeaderLabels(horizontal_labels)

        data = data[1:]
        
        for x in range(len(data)):
            total = 0
            total_count = 0
            first_col = True
            for y in range(len(data[x])):
                if first_col == True:
                    first_col = False
                    continue
                if data[x][y] != '-':
                    total += float(data[x][y])
                    total_count += 1
                else:
                    continue
            if total_count != 0:
                total = total/total_count
                data[x][-2] = f'{total:.2f}'
            
                match total:
                    case total if total >= 98:
                        data[x][-1] = 'A+'
                    case total if total >= 93:
                        data[x][-1] = 'A'
                    case total if total >= 90:
                        data[x][-1] = 'A-'
                    case total if total >= 88:
                        data[x][-1] = 'B+'
                    case total if total >= 83:
                        data[x][-1] = 'B'
                    case total if total >= 80:
                        data[x][-1] = 'B-'
                    case total if total >= 78:
                        data[x][-1] = 'C+'
                    case total if total >= 73:
                        data[x][-1] = 'C'
                    case total if total >= 70:
                        data[x][-1] = 'C-'
                    case total if total >= 68:
                        data[x][-1] = 'D+'
                    case total if total >= 63:
                        data[x][-1] = 'D'
                    case total if total >= 60:
                        data[x][-1] = 'D-'
                    case _:
                        data[x][-1] = 'F'

        for x in range(len(data)):
            for y in range(len(data[x])):
                self.tableWidget.setItem(x,y,QTableWidgetItem(data[x][y]))

    def addStudent(self) -> None:
        """
        Function to add a new student.
        """
        try:
            studentName = self.addStudent_input.text()
            if studentName == '':
                raise TypeError
            with open('data.csv','a+',newline='') as f:
                f.seek(0)
                content = f.readlines()
                content[0] = content[0].split(',')
                for n in range(len(content)):
                    if n == 0:
                        continue
                    r = content[n].split(',')
                    if studentName in r:
                        raise ValueError
                row = [studentName]
                for n in range(len(content[0])-1):
                    row.append('-')
                writer = csv.writer(f)
                f.seek(len(content))
                writer.writerow(row)
            self.clearText()
            self.updateTable()
            self.updateDropdowns()
        except ValueError:
            self.addStudent_label.setText(f'Student already\n exists!')
        except TypeError:
            self.addStudent_label.setText('Enter student name')

    def addAssign(self) -> None:
        """
        Function to add a new assignment.
        """
        try:
            assignName = self.addAssign_input.text()
            if assignName == '':
                raise TypeError
            if assignName == 'Total' or assignName == 'Grade' or assignName == 'Student Name':
                raise TypeError
            with open('data.csv','r') as f:
                reader = csv.reader(f)
                first_row = True
                content = []
                for row in reader:
                    if first_row == True:
                        top_row = row
                        if assignName in top_row:
                            raise ValueError
                        top_row.insert(-2,assignName)
                        content.append(top_row)
                        first_row = False
                    else:
                        new_row = row
                        new_row.insert(-2,'-')
                        content.append(row)
            with open('data.csv','w',newline='') as f:
                writer = csv.writer(f)
                for row in content:
                    writer.writerow(row)

            self.updateTable()
            self.updateDropdowns()
            self.clearText()

        except ValueError:
            self.addAssign_label.setText(f'Assignment already\n exists!')
        except TypeError:
            self.addAssign_label.setText(f'Enter valid\n assignment name')
            
    def clear(self) -> None:
        """
        Function to clear table and all text.
        """
        with open('data.csv','w',newline='') as f:
            top_row = ['Student Name','Total','Grade']
            writer = csv.writer(f)
            writer.writerow(top_row)

        self.updateTable()
        self.updateDropdowns()
        self.addStudent_input.clear()
        self.addStudent_label.clear()
        self.addAssign_input.clear()
        self.addAssign_label.clear()
        self.removeAssign_label.clear()
        self.removeAssign_input.clear()
        self.removeStudent_label.clear()
        self.removeStudent_input.clear()
        self.change_label.clear()
        

    def updateDropdowns(self) -> None:
        """
        Function to update all dropdown boxes.
        """
        self.student_combobox.clear()
        self.assign_combobox.clear()
        
        student_names = []       
        with open('data.csv','r') as f:
            content = f.readlines()
            assign_names = content[0].split(',')
            if len(assign_names) > 3:
                assign_names = assign_names[1:-2]
                for assign in assign_names:
                    self.assign_combobox.addItem(assign)
            if len(content) > 1:
                first_row = True
                for row in content:
                    if first_row == True:
                        first_row = False
                        continue
                    x = row.split(',')
                    student_names.append(x[0])
                for name in student_names:
                    self.student_combobox.addItem(name)
    
    def changeScore(self) -> None:
        """
        Function to change the score value of an assignment.
        """
        assignName = self.assign_combobox.currentText()
        studentName = self.student_combobox.currentText()
        newGrade = self.score_input.text()
        try:
            if assignName == '' or studentName == '':
                raise ValueError
            newGrade = float(newGrade)

            with open('data.csv','r') as f:
                data = f.readlines()
                assign_names = data[0]
                assign_names = assign_names.split(',')
                content = []
                for n in range(len(assign_names)):
                    if assign_names[n] == assignName:
                        col = n
                        break
                for n in data:
                    row = n.strip()
                    row = row.split(',') 
                    if studentName in row:      
                        row[col] = newGrade
                        content.append(row)
                    else:
                        content.append(row)

            with open('data.csv','w',newline='') as f:
                writer = csv.writer(f)
                for line in content:
                    writer.writerow(line)

            self.updateTable()
            self.clearText()       
                        
        except ValueError:
            self.change_label.setText('Please enter score as a percentage')

    def removeStudent(self) -> None:
        """
        Function to remove a student.
        """
        try:
            studentName = self.removeStudent_input.text()
            if studentName == '':
                raise TypeError
           
            content = []
            with open('data.csv','r') as f:
                data = f.readlines()
                student_found = False
                for line in data:
                    line = line.strip()
                    line = line.split(',')
                    if studentName in line:
                        student_found = True
                        continue
                    else:
                        content.append(line)
                if student_found == False:
                    raise ValueError
                
            with open('data.csv','w',newline='') as f:
                writer = csv.writer(f)
                for line in content:
                    writer.writerow(line)

            self.clearText()
            self.updateTable()
            self.updateDropdowns()
        
        except ValueError:
            self.removeStudent_label.setText(f'Student not found')
        except TypeError:
            self.removeStudent_label.setText('Enter student name')

    def removeAssign(self) -> None:
        """
        Function to remove an assignment.
        """
        try:
            assignName = self.removeAssign_input.text()
            if assignName == '':
                raise TypeError
            if assignName == 'Total' or assignName == 'Grade' or assignName == 'Student Name':
                raise TypeError

            content = []
            with open('data.csv', 'r') as f:
                data = f.readlines()
                assign_names = data[0]
                assign_names.split(',')
                if assignName not in assign_names:
                    raise ValueError
                col = 0
                for line in data:
                    line = line.strip()
                    line = line.split(',')
                    for n in range(len(line)):
                        if line[n] == assignName:
                            col = n
                    line.pop(col)
                    content.append(line)

            with open('data.csv','w',newline='') as f:
                writer = csv.writer(f)
                for line in content:
                    writer.writerow(line)

            self.clearText()
            self.updateTable()
            self.updateDropdowns()

        except ValueError:
            self.removeAssign_label.setText(f'Assignment not found')
        except TypeError:
            self.removeAssign_label.setText('Enter valid\n assignment name')

    def clearText(self) -> None:
        """
        Function to clear all text on the window.
        """
        self.addStudent_input.clear()
        self.addStudent_label.clear()
        
        self.addAssign_input.clear()
        self.addAssign_label.clear()
       
        self.removeAssign_label.clear()
        self.removeAssign_input.clear()
        
        self.removeStudent_label.clear()
        self.removeStudent_input.clear()
        
        self.change_label.clear()
        self.score_input.clear()