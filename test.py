from PySide.QtCore import *
from PySide.QtGui import *
import sys
import person
import worker
import spouse
import csv_handle
import re
import datetime

class MainDialog(QMainWindow, worker.Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.setupUi(self)

        self.people = csv_handle.load('Family tree test.csv')

        for a in sorted(self.people):
            self.peoplelist.addItem(a + ' - ' + self.people[a].nick_name)

        self.label_ID.setAlignment(Qt.AlignRight)
        self.label_bday.setAlignment(Qt.AlignRight)
        self.label_children.setAlignment(Qt.AlignRight)
        self.label_dday.setAlignment(Qt.AlignRight)
        self.label_father.setAlignment(Qt.AlignRight)
        self.label_gender.setAlignment(Qt.AlignRight)
        self.label_marriage.setAlignment(Qt.AlignRight)
        self.label_mother.setAlignment(Qt.AlignRight)
        self.label_nickname.setAlignment(Qt.AlignRight)
        self.label_notes.setAlignment(Qt.AlignRight)
        self.label_realname.setAlignment(Qt.AlignRight)

        self.peoplelist.currentItemChanged.connect(self.select_in_list)
        self.nicknameEdit.textChanged.connect(self.update_nick_name)
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
        self.actionParents.triggered.connect(self.create_parents)
        self.actionSpouse.triggered.connect(self.create_spouse)
        self.actionChildren.triggered.connect(self.create_child)
        self.actionExit.triggered.connect(self.exitApp)
        self.actionEdit_Spouse.triggered.connect(self.spouse_window)

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
            print("Unexpected error:", sys.exc_info())
            raise

        try:
            self.motherButton.setText(self.people[self.key].mother_id + ' - '
                                    + self.people[self.people[self.key].mother_id].nick_name)
        except KeyError:
            self.motherButton.setText('')
        except:
            print("Unexpected error:", sys.exc_info())
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
            self.spouselist.setCurrentItem(self.spouselist.findItems(a, Qt.MatchExactly)[0])

        self.childrenlist.clear()
        for a in self.process_kids(self.key):
            self.childrenlist.addItem(a)

    def process_marriage(self, key):
        result = []
        if self.people[key].marriage[0][0] == 'S':
            return result
        else:
            for l in self.people[key].marriage:
                print(l)
                if l[0] == 'D':
                    ret = l[1:4] + ' - ' + self.people[l[1:4]].nick_name + " (Divorced)"
                elif l[0] == 'E':
                    ret = l[1:4] + ' - ' + self.people[l[1:4]].nick_name + " (Engaged)"
                elif self.people[l[1:4]].death and not self.people[key].death:
                    ret = l[1:4] + ' - ' + self.people[l[1:4]].nick_name + " (Deceased)"
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
        nck = self.nicknameEdit.text()
        self.people[self.key].update('nick_name', nck)
        self.peoplelist.currentItem().setText(self.key + ' - ' + nck)

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
                    except ValueError:
                        pass

        if self.people[self.key].age > 1:
            self.bdayEdit.setText(self.people[self.key].birth + ' ({} years)'.format(self.people[self.key].age))
        else:
            self.bdayEdit.setText(self.people[self.key].birth)


    def update_gender(self):
        if self.maleRadio.isChecked() and self.sender().text() == 'Male':
            self.people[self.key].update('gender', 'M')
        elif self.femaleRadio.isChecked() and self.sender().text() == 'Female':
            self.people[self.key].update('gender', 'F')

    def update_death(self):
        if not self.ddayRadio.isChecked():
            self.people[self.key].update('dday', 0)
        else:
            formats = ['%Y%m%d', '%Y%m', '%Y', '%m%d']
            birth = self.people[self.key].bday
            death = self.ddayEdit.text()
            m = re.match('^[0-9]{8}$|'
                         '^[0-9]{6}$|'
                         '^[0-9]{4}$|', birth)
            n = re.match('^[0-9]{8}$|'
                         '^[0-9]{6}$|'
                         '^[0-9]{4}$|', death)

            if m.group() and n.group():
                for frmt1 in formats:
                    for frmt2 in formats:
                        # print(frmt1, frmt2)
                        try:
                            if datetime.datetime.strptime(birth, frmt1) and datetime.datetime.strptime(death, frmt2):

                                b = datetime.datetime.strptime(birth, frmt1)
                                d = datetime.datetime.strptime(death, frmt2)

                                if b < d:
                                    self.people[self.key].update('dday', self.ddayEdit.text())
                                else:
                                    print('invalid')
                        except ValueError:
                            pass
                        except:
                            print(sys.exc_info())
            else:
                self.people[self.key].update('dday', self.ddayEdit.text())

            if self.people[self.key].age > 1:
                self.bdayEdit.setText(self.people[self.key].birth + ' ({} years)'.format(self.people[self.key].age))
            else:
                self.bdayEdit.setText(self.people[self.key].birth)
            self.ddayEdit.setText(self.people[self.key].death)

    def update_impflg(self):
        if self.impRadio.isChecked():
            self.people[self.key].update('imp_flg', '1')
        else:
            self.people[self.key].update('imp_flg', '')

    def update_notes(self):
        self.people[self.key].update('notes', self.notesEdit.toPlainText())

    def get_next_number(self):
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        text = sorted(self.people.keys())

        for a in alphabet:
            for b in alphabet:
                for c in alphabet:
                    test = a+b+c
                    if test not in text and test != '000':
                        return test

    def create_parents(self):
        print(self.people[self.key].father_id, self.people[self.key].mother_id)
        father = self.people[self.key].father_id
        if not father:
            k = self.get_next_number()
            self.people[k] = person.person(k, '', '', '', 'M', '', '', ['S000'], [self.key], '', '', '')
            self.people[self.key].update('father_id', k)
            self.peoplelist.addItem(k + ' - ' + self.people[k].nick_name)
            father = k

        mother = self.people[self.key].mother_id
        if not mother:
            k = self.get_next_number()
            self.people[k] = person.person(k, '', '', '', 'F', '', '', ['S000'], [self.key], '', '', '')
            self.people[self.key].update('mother_id', k)
            self.peoplelist.addItem(k + ' - ' + self.people[k].nick_name)
            mother = k

        print(father, mother)
        self.people[father].update('marriage', ['M' + mother])
        self.people[mother].update('marriage', ['M' + father])

    def create_spouse(self):
        # TODO add keys to marriage attribute
        k = self.get_next_number()
        self.people[k] = person.person(k, '', '', '', '', '', '', ['M' + self.key], '', '', '', '')
        self.peoplelist.addItem(k + ' - ' + self.people[k].nick_name)
        if self.people[self.key].marriage[0][0] == 'S':
            self.people[self.key].marriage = ['M' + k]
        else:
            self.people[self.key].marriage.append('M' + k)

        self.peoplelist.setCurrentItem(self.peoplelist.findItems(k + ' - ' + self.people[k].nick_name, Qt.MatchExactly)[0])

        self.spouse_window()

    def create_child(self):
        try:
            spouse = self.spouselist.currentItem().text()[:3]
            if self.marital_check_for_create_child(self.key, spouse):
                k = self.get_next_number()

                if self.people[self.key].gender == 'M':
                    self.people[k] = person.person(k, '', '', '', '', self.key, spouse, ['S000'], '', '', '', '')
                elif self.people[self.key].gender == 'F':
                    self.people[k] = person.person(k, '', '', '', '', spouse, self.key, ['S000'], '', '', '', '')

                self.people[self.key].children.append(k)
                self.people[spouse].children.append(k)

                self.peoplelist.addItem(k + ' - ' + self.people[k].nick_name)

                self.peoplelist.setCurrentItem(self.peoplelist.findItems(k + ' - ' + self.people[k].nick_name, Qt.MatchExactly)[0])

        except AttributeError:
            pass

    def marital_check_for_create_child(self, person, spouse):
        for a in self.people[self.key].marriage:
                if a[1:4] == spouse and a[0] in ['M', 'D']:
                    return True
        return False

    def spouse_window(self):
        try:
            self.spouseWindow = SpouseDialog(self.key, self.spouselist.currentItem().text()[:3], self.people)
            self.spouseWindow.show()
        except AttributeError:
            pass


    def delete_person(self):
        father = self.people[self.key].father_id
        mother = self.people[self.key].mother_id
        spouse = self.people[self.key].marriage
        children = self.people[self.key].children

        if father:
            self.people[father].children.remove(self.key)
        if mother:
            self.people[mother].children.remove(self.key)

        if spouse:
            for sp in spouse:
                for m in self.people[sp[1:4]].marriage:
                    if m[1:4] == self.key:
                        self.people[sp[1:4]].marriage.remove(m)
                        if self.people[sp[1:4]].marriage == []:
                            self.people[sp[1:4]].marriage = ['S000']

        if children[0]:
            print(children)
            for child in children:
                if self.people[self.key].gender == 'M':
                    self.people[child].father_id = ''
                elif self.people[self.key].gender == 'F':
                    self.people[child].mother_id = ''
        self.people.pop(self.key)
        self.peoplelist.takeItem(self.peoplelist.row(self.peoplelist.currentItem()))
        print(sorted(self.people.keys()))

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

class SpouseDialog(QMainWindow, spouse.Ui_MainWindow):
    status = ''
    marriage = ''
    m_out = ''
    divorce = ''
    d_out = ''
    people = {}
    key = ''
    spouse = ''

    months = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May',
          '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct',
          '11':'Nov', '12':'Dec'}

    def __init__(self, key, spouse, people, parent=None):
        super().__init__()
        self.setupUi(self)

        # print(key, spouse, people[key].marriage)
        self.people = people
        self.key = key
        self.spouse = spouse
        for a in people[key].marriage:
            if a[1:4] == spouse:
                self.status = a[0]
                try:
                    self.marriage = a.split('_')[1].split('*')[0]
                except IndexError:
                    self.marriage = ''
                try:
                    self.divorce = a.split('_')[1].split('*')[1]
                except IndexError:
                    pass
                # print(self.marriage)

        # print(self.marriage, self.divorce)
        self.init_fields()

        self.engagedButton.toggled.connect(self.update_status)
        self.marriedButton.toggled.connect(self.update_status)
        self.divorcedButton.toggled.connect(self.update_status)

        self.marriageEdit.editingFinished.connect(self.update_marriage)
        self.separationEdit.editingFinished.connect(self.update_divorce)

        self.buttonBox.clicked.connect(self.close_spouse_window)

    def init_fields(self):
        if self.marriage:
            self.dates()
        self.engagedButton.setChecked(self.status == 'E')
        self.marriedButton.setChecked(self.status == 'M')
        self.divorcedButton.setChecked(self.status == 'D')
        if self.status != 'D':
            self.separationEdit.setEnabled(False)

        self.marriageEdit.setText(self.m_out)
        self.separationEdit.setText(self.d_out)


    def dates(self):
        l = []
        m_year = ''
        m_month = ''
        m_day = ''
        d_year = ''
        d_month = ''
        d_day = ''
        if len(self.marriage) >= 4 and self.marriage[0:4] != 'xxxx':
            m_year = int(self.marriage[0:4])
            l.append(self.marriage[0:4])
        if len(self.marriage)>= 6:
            m_month = int(self.marriage[4:6])
            l.append(self.months[self.marriage[4:6]])
        if len(self.marriage) >= 8:
            m_day = int(self.marriage[6:8])
            l.append(self.marriage[6:8])

        self.m_out = '-'.join(l)

        if self.status == 'D':
            l = []
            if len(self.divorce) >= 4:
                d_year = int(self.divorce[0:4])
                l.append(self.divorce[0:4])
            if len(self.divorce)>= 6:
                d_month = int(self.divorce[4:6])
                if len(l) == 1:
                    l.append(months[self.divorce[4:6]])
            if len(self.divorce) >= 8:
                d_day = int(self.divorce[6:8])
                if len(l) == 2:
                    l.append(self.divorce[6:8])

            self.d_out = '-'.join(l)

        # if m_year and d_year:
        #     if m_month and d_month:
        #         if m_day and d_day:
        #             if (d_month > m_month) or (d_month == m_month and d_day >= m_day):
        #                 self.age = d_year - m_year
        #             else:
        #                 self.age = d_year - m_year - 1
        #         else:
        #             if d_month >= m_month:
        #                 self.age = d_year - m_year
        #             else:
        #                 self.age = d_year - m_year - 1
        #     else:
        #         self.age = d_year - m_year
        # else:
        #     now = datetime.datetime.now()
        #     if m_year:
        #         if m_month:
        #             if m_day:
        #                 if (now.month > m_month) or (now.month == m_month and now.day >= m_day):
        #                     self.age = now.year - m_year
        #                 else:
        #                     self.age = now.year - m_year - 1
        #             else:
        #                 if now.month >= m_month:
        #                     self.age = now.year - m_year
        #                 else:
        #                     self.age = now.year - m_year - 1
        #         else:
        #             self.age = now.year - m_year


    def update_status(self):
        if self.engagedButton.isChecked() and self.sender().text() == 'Engaged':
            self.status = 'E'
            self.separationEdit.setEnabled(False)
        elif self.marriedButton.isChecked() and self.sender().text() == 'Married':
            self.status = 'M'
            self.separationEdit.setEnabled(False)
        elif self.divorcedButton.isChecked() and self.sender().text() == 'Divorced':
            self.status = 'D'
            self.separationEdit.setEnabled(True)
        else:
            pass

    def update_marriage(self):
        if self.status in ['M', 'D']:
            formats = ['%Y%m%d', '%Y%m', '%Y', '%m%d']
            start = self.marriageEdit.text()
            m = re.match('^[0-9]{8}$|'
                         '^[0-9]{6}$|'
                         '^[0-9]{4}$|', start)

            if m:
                for frmt in formats:
                    try:
                        if datetime.datetime.strptime(start, frmt):
                            self.marriage = start
                            self.dates()
                    except ValueError:
                        pass
                # for n, p in enumerate(self.people[self.key].marriage):
                #     m = re.match('^[DMW]' + self.spouse + '[_a-zA-Z0-9]*', p)
                #     if p == m.group():
                #         self.people[self.key].marriage[n] = self.status + self.spouse + '_' + txt
                # print(self.marriageEdit.text(), m.group())

            self.marriageEdit.setText(self.m_out)
            # self.separationEdit.setText(self.d_out)


    def update_divorce(self):
        if self.status == 'D':
            formats = ['%Y%m%d', '%Y%m', '%Y', '%m%d']
            start = self.marriage
            end = self.separationEdit.text()
            m = re.match('^[0-9]{8}$|'
                         '^[0-9]{6}$|'
                         '^[0-9]{4}$|', start)
            n = re.match('^[0-9]{8}$|'
                         '^[0-9]{6}$|'
                         '^[0-9]{4}$|', end)

            if m and n:
                for frmt1 in formats:
                    for frmt2 in formats:
                        # print(frmt1, frmt2)
                        try:
                            if datetime.datetime.strptime(start, frmt1) and datetime.datetime.strptime(end, frmt2):

                                b = datetime.datetime.strptime(start, frmt1)
                                d = datetime.datetime.strptime(end, frmt2)

                                if b < d:
                                    self.divorce = end
                                    self.dates()
                                else:
                                    print('invalid')
                        except ValueError:
                            pass
                        except:
                            print(sys.exc_info())

        # print(self.divorce)

    def close_spouse_window(self, button):
        # print(self.marriage, self.divorce)
        if button.text().lower() == 'save':
            for n, p in enumerate(self.people[self.key].marriage):
                m = re.match('^[DM]' + self.spouse + '[_*a-zA-Z0-9]*', p)
                try:
                    if p == m.group():
                        self.people[self.key].marriage[n] = self.status + self.spouse
                        if self.marriage:
                            self.people[self.key].marriage[n] += '_' + self.marriage
                        if self.divorce:
                            self.people[self.key].marriage[n] += '*' + self.divorce
                except AttributeError:
                    pass
                    # print('close_spouse_window attribute error')

            for n, p in enumerate(self.people[self.spouse].marriage):
                m = re.match('^[DM]' + self.key + '[_*a-zA-Z0-9]*', p)
                try:
                    if p == m.group():
                        self.people[self.spouse].marriage[n] = self.status + self.key
                        if self.marriage:
                            self.people[self.spouse].marriage[n] += '_' + self.marriage
                        if self.divorce:
                            self.people[self.spouse].marriage[n] += '*' + self.divorce
                except AttributeError:
                    pass
                    # print('close_spouse_window attribute error')

        self.close()

def main():
    app = QApplication(sys.argv)
    form = MainDialog()

    form.show()
    app.exec_()

if __name__ == '__main__':
    main()