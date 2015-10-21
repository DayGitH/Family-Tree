from PySide.QtCore import *
from PySide.QtGui import *
import sys
import worker
import csv_handle
import re
import datetime

class MainDialog(QMainWindow, worker.Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        self.people = csv_handle.load('Family tree test.csv')

        for a in sorted(self.people):
            self.peoplelist.addItem(a + ' - ' + self.people[a].nick_name)

        self.peoplelist.currentItemChanged.connect(self.select_in_list)
        self.nicknameEdit.editingFinished.connect(self.update_nick_name)
        self.realnameEdit.editingFinished.connect(self.update_real_name)
        self.bdayEdit.editingFinished.connect(self.update_bday)
        self.femaleRadio.toggled.connect(self.update_gender)
        self.maleRadio.toggled.connect(self.update_gender)
        self.ddayRadio.toggled.connect(self.update_death)
        self.ddayEdit.editingFinished.connect(self.update_death)
        self.impRadio.toggled.connect(self.update_impflg)
        self.notesEdit.textChanged.connect(self.update_notes)
        self.fatherButton.pressed.connect(self.open_father)
        self.motherButton.pressed.connect(self.open_mother)
        self.spouselist.itemDoubleClicked.connect(self.open_spouse)
        self.childrenlist.itemDoubleClicked.connect(self.open_child)

        self.actionDelete_Person.triggered.connect(self.delete_person)
        self.actionExit.triggered.connect(self.exitApp)

        self.fatherButton.setFlat(True)
        self.motherButton.setFlat(True)

        self.peoplelist.setCurrentItem(self.peoplelist.findItems(sorted(list(self.people.keys()))[0] + ' - ' + self.people[sorted(list(self.people.keys()))[0]].nick_name, Qt.MatchExactly)[0])

    def select_in_list(self, cur, prev):
        self.key = cur.text()[:3]
        self.keyEdit.setText(self.key)
        self.nicknameEdit.setText(self.people[self.key].nick_name)

        if self.people[self.key].age > 1:
            self.bdayEdit.setText(self.people[self.key].birth + ' ({} years)'.format(self.people[self.key].age))
        else:
            self.bdayEdit.setText(self.people[self.key].birth)
        self.realnameEdit.setText(self.people[self.key].real_name)
        self.ddayEdit.setText(self.people[self.key].death)

        try:
            self.fatherButton.setText(self.people[self.key].father_id + ' - '
                                    + self.people[self.people[self.key].father_id].nick_name)
        except KeyError:
            self.fatherButton.setText('')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        try:
            self.motherButton.setText(self.people[self.key].mother_id + ' - '
                                    + self.people[self.people[self.key].mother_id].nick_name)
        except KeyError:
            self.motherButton.setText('')
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        if self.people[self.key].dday:
            self.ddayRadio.setChecked(True)
        else:
            self.ddayRadio.setChecked(False)

        if self.people[self.key].gender == 'F':
            self.femaleRadio.setChecked(True)
        elif self.people[self.key].gender == 'M':
            self.maleRadio.setChecked(True)

        if self.people[self.key].imp_flg:
            self.impRadio.setChecked(True)
        else:
            self.impRadio.setChecked(False)

        self.notesEdit.setText(self.people[self.key].notes)

        self.spouselist.clear()
        for a in self.process_marriage(self.key):
            self.spouselist.addItem(a)

        self.childrenlist.clear()
        for a in self.process_kids(self.key):
            self.childrenlist.addItem(a)

    def process_marriage(self, key):
        result = []
        if self.people[key].marriage[0][0] == 'S':
            return result
        else:
            for l in self.people[key].marriage:
                if l[0] == 'W' and not self.people[key].death:
                    ret = l[1:4] + ' - ' + self.people[l[1:4]].nick_name + " (Deceased)"
                elif l[0] == 'D':
                    ret = l[1:4] + ' - ' + self.people[l[1:4]].nick_name + " (Divorced)"
                elif l[0] == 'E':
                    ret = l[1:4] + ' - ' + self.people[l[1:4]].nick_name + " (Engaged)"
                else:
                    ret = l[1:4] + ' - ' + self.people[l[1:4]].nick_name

                result.append(ret)

            return result

    def process_kids(self, key):
        result = []
        for l in self.people[key].children:
            if l:
                result.append(l + ' - ' + self.people[l].nick_name)
        return result

    def update_nick_name(self):
        self.people[self.key].update('nick_name', self.nicknameEdit.text())

    def update_real_name(self):
        self.people[self.key].update('real_name', self.realnameEdit.text())

    def update_bday(self):
        formats = ['%Y%m%d', '%Y%m', '%Y', '%m%d']
        txt = self.bdayEdit.text()
        m = re.match('^[0-9]{8}$|'
                     '^[0-9]{6}$|'
                     '^[0-9]{4}$|'
                     '^[x]{4}[0-9]{4}$', txt)

        if m:
            for frmt in formats:
                try:
                    if datetime.datetime.strptime(txt, frmt):
                        self.people[self.key].update('bday', self.bdayEdit.text())
                        break
                except ValueError:
                    try:
                        if datetime.datetime.strptime(txt.replace('x', ''), frmt):
                            self.people[self.key].update('bday', self.bdayEdit.text())
                            break
                    except:
                        print(sys.exc_info()[0])
                except:
                    print(sys.exc_info()[0])

    def update_gender(self):
        if self.maleRadio.isChecked() and self.sender().text() == 'Male':
            self.people[self.key].update('gender', 'M')
        elif self.femaleRadio.isChecked() and self.sender().text() == 'Female':
            self.people[self.key].update('gender', 'F')

    def update_death(self):
        if not self.ddayRadio.isChecked():
            self.people[self.key].update('dday', 0)
        else:
            self.people[self.key].update('dday', self.ddayEdit.text())

    def update_impflg(self):
        if self.impRadio.isChecked():
            self.people[self.key].update('imp_flg', '1')
        else:
            self.people[self.key].update('imp_flg', '')

    def update_notes(self):
        self.people[self.key].update('notes', self.notesEdit.toPlainText())

    def delete_person(self):
        # TODO delete from other people's data as well
        # print(self.)
        self.people.pop(self.key)
        self.peoplelist.takeItem(self.peoplelist.row(self.peoplelist.currentItem()))

    def open_father(self):
        try:
            self.peoplelist.setCurrentItem(self.peoplelist.findItems(self.fatherButton.text(), Qt.MatchExactly)[0])
        except IndexError:
            pass

    def open_mother(self):
        try:
            self.peoplelist.setCurrentItem(self.peoplelist.findItems(self.motherButton.text(), Qt.MatchExactly)[0])
        except IndexError:
            pass

    def open_spouse(self, item):
        try:
            self.peoplelist.setCurrentItem(self.peoplelist.findItems(item.text(), Qt.MatchExactly)[0])
        except IndexError:
            self.peoplelist.setCurrentItem(self.peoplelist.findItems(item.text()[:item.text().index(' (')], Qt.MatchExactly)[0])

    def open_child(self, item):
        self.peoplelist.setCurrentItem(self.peoplelist.findItems(item.text(), Qt.MatchExactly)[0])

    def exitApp(self):
        sys.exit(0)

def main():
    app = QApplication(sys.argv)
    form = MainDialog()

    form.show()
    app.exec_()

if __name__ == '__main__':
    main()