from PySide.QtCore import *
from PySide.QtGui import *
import sys
import person
import worker
# import spouse
# import attacher
import csv_handle
import re
import datetime

class MainDialog(QMainWindow, worker.Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.setupUi(self)


        self.peopleList.currentItemChanged.connect(self.select_in_list)
        self.spouseList.currentItemChanged.connect(self.marital_info)
        self.nicknameEdit.textChanged.connect(self.update_nick_name)
        self.realnameEdit.editingFinished.connect(self.update_real_name)
        self.bdayEdit.editingFinished.connect(self.update_bday)
        self.femaleRadio.toggled.connect(self.update_gender)
        self.maleRadio.toggled.connect(self.update_gender)
        self.ddayRadio.toggled.connect(self.update_death)
        self.ddayEdit.editingFinished.connect(self.update_death)
        self.impRadio.toggled.connect(self.update_impflg)
        self.notesEdit.textChanged.connect(self.update_notes)
        self.fatherButton.clicked.connect(self.open_father)
        self.motherButton.clicked.connect(self.open_mother)
        self.spouseList.itemDoubleClicked.connect(self.open_spouse)
        self.childrenList.itemDoubleClicked.connect(self.open_child)
        self.newFamilyButton.clicked.connect(self.new_family)
        self.saveFamilyButton.clicked.connect(self.save_family)
        self.loadFamilyButton.clicked.connect(self.open_family)
        self.actionAttach.triggered.connect(self.attacher_window)
        self.deletePersonButton.clicked.connect(self.delete_person)
        self.createParentsButton.clicked.connect(self.create_parents)
        self.createSpouseButton.clicked.connect(self.create_spouse)
        self.createChildButton.clicked.connect(self.create_child)
        self.attachParentsButton.clicked.connect(self.attach_parents)
        self.attachSpouseButton.clicked.connect(self.attach_spouse)
        self.attachChildButton.clicked.connect(self.attach_child)
        self.unattachParentsButton.clicked.connect(self.unattach_parents)
        self.unattachSpouseButton.clicked.connect(self.unattach_spouse)
        self.unattachChildButton.clicked.connect(self.unattach_child)
        self.actionUnAll.triggered.connect(self.unattach_all)  # remove out
        self.exitButton.clicked.connect(self.exitApp)
        self.actionEdit_Spouse.triggered.connect(self.spouse_window)
        self.firstStatusRadio.toggled.connect(self.update_status)
        self.secondStatusRadio.toggled.connect(self.update_status)
        self.thirdStatusRadio.toggled.connect(self.update_status)
        self.spouseInfo.editingFinished.connect(self.update_anniversary)
        self.secondaryList.currentItemChanged.connect(self.select_in_secondary)
        self.saveBox.clicked.connect(self.save_attached)
        self.moveUpSpouse.clicked.connect(self.move_spouse_up)
        self.moveDnSpouse.clicked.connect(self.move_spouse_down)
        self.moveUpChild.clicked.connect(self.move_child_up)
        self.moveDnChild.clicked.connect(self.move_child_down)

        self.fatherButton.setFlat(True)
        self.motherButton.setFlat(True)
        self.primaryList.hide()
        self.primaryListLabel.hide()
        self.secondaryList.hide()
        self.secondaryListLabel.hide()
        self.saveBox.hide()

        # self.new_family()

        self.people = csv_handle.load('save4.csv')

        for a in sorted(self.people):
            self.peopleList.addItem(a + ' - ' + self.people[a].nick_name)

        self.peopleList.setCurrentRow(0)

    def new_family(self):
        self.people = {}
        self.peopleList.clear()
        k = self.get_next_number()

        self.people[k] = person.person(k, gender='M')
        self.peopleList.addItem(k + ' - ' + self.people[k].nick_name)
        self.peopleList.setCurrentRow(0)

    def save_family(self):
        try:
            fname, _ = QFileDialog.getSaveFileName(self, 'Save Family File', '.', '*.csv')
            csv_handle.save(fname, self.people)
        except FileNotFoundError:
            pass

    def open_family(self):
        try:
            fname, _ = QFileDialog.getOpenFileName(self, 'Open Family File', '.', '*.csv')

            self.people = {}
            self.peopleList.clear()
            self.people = csv_handle.load(fname)

            for a in sorted(self.people):
                self.peopleList.addItem(a + ' - ' + self.people[a].nick_name)
        except FileNotFoundError:
            pass

    def select_in_list(self, cur, prev):
        try:
            self.key = cur.text()[:3]
            self.spouse = ''
        except AttributeError:
            print('attribute error in select_in_list')
            return
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

        self.spouseList.clear()
        for a in self.process_marriage(self.key):
            self.spouseList.addItem(a)
            self.spouseList.setCurrentRow(0)

        self.childrenList.clear()
        for a in self.process_kids(self.key):
            self.childrenList.addItem(a)
            self.childrenList.setCurrentRow(0)

    def process_marriage(self, key):
        result = []
        if self.people[key].marriage[0][0] == 'S':
            self.firstStatusRadio.setChecked(True)
            self.secondStatusRadio.hide()
            self.thirdStatusRadio.hide()
            return result
        else:
            for l in self.people[key].marriage:
                # print(l)
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
        self.peopleList.currentItem().setText(self.key + ' - ' + nck)

    def update_real_name(self):
        self.people[self.key].update('real_name', self.realnameEdit.text())

    def update_bday(self):
        formats = ['%Y%m%d', '%Y%m', '%Y', '%m%d']
        txt = self.bdayEdit.text()
        m = re.match('^[0-9]{8}$|'
                     '^[0-9]{6}$|'
                     '^[0-9]{4}$|'
                     '^[x]{4}[0-9]{2}$|'
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
            elif n.group():
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
        # print(self.people[self.key].father_id, self.people[self.key].mother_id)
        father = self.people[self.key].father_id
        if not father:
            k = self.get_next_number()
            self.people[k] = person.person(k, gender='M', children=[self.key])
            self.people[self.key].update('father_id', k)
            self.peopleList.addItem(k + ' - ' + self.people[k].nick_name)
            father = k

        mother = self.people[self.key].mother_id
        if not mother:
            k = self.get_next_number()
            self.people[k] = person.person(k, gender='F', children=[self.key])
            self.people[self.key].update('mother_id', k)
            self.peopleList.addItem(k + ' - ' + self.people[k].nick_name)
            mother = k

        # print(father, mother)
        self.people[father].update('marriage', ['M' + mother])
        self.people[mother].update('marriage', ['M' + father])

        self.select_in_list(self.peopleList.currentItem(), '')

    def create_spouse(self):
        k = self.get_next_number()
        g = 'F' if self.people[self.key].gender == 'M' else 'M'
        self.people[k] = person.person(k, gender=g, marriage=['M' + self.key])
        self.peopleList.addItem(k + ' - ' + self.people[k].nick_name)
        if self.people[self.key].marriage[0][0] == 'S':
            self.people[self.key].marriage = ['M' + k]
        else:
            self.people[self.key].marriage.append('M' + k)
        self.peopleList.setCurrentItem(self.peopleList.findItems(k + ' - ' + self.people[k].nick_name, Qt.MatchExactly)[0])

    def create_child(self):
        try:
            spouse = self.spouseList.currentItem().text()[:3]
            if self.marital_check_for_create_child(self.key, spouse):
                k = self.get_next_number()

                if self.people[self.key].gender == 'M':
                    self.people[k] = person.person(k, gender='M', father_id=self.key, mother_id=spouse)
                elif self.people[self.key].gender == 'F':
                    self.people[k] = person.person(k, gender='F', father_id=spouse, mother_id=self.key)

                if self.people[self.key].children:
                    self.people[self.key].children.append(k)
                else:
                    self.people[self.key].children = [k]

                if self.people[spouse].children:
                    self.people[spouse].children.append(k)
                else:
                    self.people[spouse].children = [k]

                self.peopleList.addItem(k + ' - ' + self.people[k].nick_name)

                self.peopleList.setCurrentItem(self.peopleList.findItems(k + ' - ' + self.people[k].nick_name, Qt.MatchExactly)[0])
        except AttributeError:
            pass

    def marital_check(self, person):
        for a in self.people[person].marriage:
                if a[0] in ['M', 'D']:
                    return True
        return False

    def enable_inputs(self, bool):
        self.nicknameEdit.setEnabled(bool)
        self.realnameEdit.setEnabled(bool)
        self.bdayEdit.setEnabled(bool)
        self.maleRadio.setEnabled(bool)
        self.femaleRadio.setEnabled(bool)
        self.firstStatusRadio.setEnabled(bool)
        self.secondStatusRadio.setEnabled(bool)
        self.thirdStatusRadio.setEnabled(bool)
        self.ddayRadio.setEnabled(bool)
        self.ddayEdit.setEnabled(bool)
        self.notesEdit.setEnabled(bool)
        self.fatherButton.setEnabled(bool)
        self.motherButton.setEnabled(bool)
        self.spouseList.setEnabled(bool)
        self.spouseInfo.setEnabled(bool)
        self.childrenList.setEnabled(bool)
        self.newFamilyButton.setEnabled(bool)
        self.saveFamilyButton.setEnabled(bool)
        self.loadFamilyButton.setEnabled(bool)
        self.createSpouseButton.setEnabled(bool)
        self.createChildButton.setEnabled(bool)
        self.createParentsButton.setEnabled(bool)
        self.deletePersonButton.setEnabled(bool)
        self.attachChildButton.setEnabled(bool)
        self.attachParentsButton.setEnabled(bool)
        self.attachSpouseButton.setEnabled(bool)
        self.unattachChildButton.setEnabled(bool)
        self.unattachParentsButton.setEnabled(bool)
        self.unattachSpouseButton.setEnabled(bool)



    def attach_parents(self):
        if self.people[self.key].father_id or self.people[self.key].mother_id:
            return

        self.enable_inputs(False)
        self.secondaryList.show()
        self.secondaryListLabel.show()
        self.secondaryListLabel.setText('Select First Parent:')
        self.primaryList.show()
        self.primaryListLabel.show()
        self.primaryListLabel.setText('Select Second Parent:')
        self.saveBox.show()

        self.secondaryList.clear()
        for a in sorted(self.people):
            if self.marital_check(a):
                self.secondaryList.addItem(a + ' - ' + self.people[a].nick_name)

        self.secondaryList.setCurrentRow(0)
        self.attach = 'parents'
        # self.secondaryList.clear()
        # for a in sorted(self.people):
        #     if not (self.people[a].father_id or self.people[a].mother_id):
        #         self.secondaryList.addItem(a + ' - ' + self.people[a].nick_name)
        #
        # self.secondaryList.setCurrentRow(0)

    def select_in_secondary(self, cur, prev):
        if cur:
            parentone = cur.text()[:3]
            self.primaryList.clear()
            for a in self.people[parentone].marriage:
                if a[0] in ['M', 'D']:
                    self.primaryList.addItem(a[1:4] + ' - ' + self.people[a[1:4]].nick_name)
            self.primaryList.setCurrentRow(0)

    def attach_spouse(self):
        self.enable_inputs(False)
        self.primaryList.show()
        self.primaryListLabel.show()
        self.primaryListLabel.setText('Select Spouse:')
        self.saveBox.show()

        gender = 'F' if self.people[self.key].gender == 'M' else 'M'
        for a in sorted(self.people):
            if self.people[a].gender == gender:
                self.primaryList.addItem(a + ' - ' + self.people[a].nick_name)

        self.primaryList.setCurrentRow(0)
        self.attach = 'spouse'

    def attach_child(self):
        if not self.spouseList.currentItem():
            return
        elif self.secondStatusRadio.isChecked():
            return

        self.enable_inputs(False)
        self.primaryList.show()
        self.primaryListLabel.show()
        self.primaryListLabel.setText('Select Child:')
        self.saveBox.show()

        for a in sorted(self.people):
            if not self.people[a].father_id and not self.people[a].mother_id and a != self.key:
                self.primaryList.addItem(a + ' - ' + self.people[a].nick_name)

        self.primaryList.setCurrentRow(0)
        self.attach = 'child'

    def save_attached(self, button):
        if button.text().lower() == 'save':
            if self.attach == 'spouse':
                spouse = self.primaryList.currentItem().text()[:3]
                if self.people[self.key].marriage[0][0] == 'S':
                    self.people[self.key].marriage = ['M' + spouse]
                else:
                    self.people[self.key].marriage.append('M' + spouse)

                if self.people[spouse].marriage[0][0] == 'S':
                    self.people[spouse].marriage = ['M' + self.key]
                else:
                    self.people[spouse].marriage.append('M' + self.key)

                self.spouseList.clear()
                for a in self.process_marriage(self.key):
                    self.spouseList.addItem(a)
                    self.spouseList.setCurrentRow(0)
            elif self.attach == 'parents':
                parentone = self.secondaryList.currentItem().text()[:3]
                pone_gender = self.people[parentone].gender
                parenttwo = self.primaryList.currentItem().text()[:3]
                ptwo_gender = self.people[parenttwo].gender

                if pone_gender == 'M' and ptwo_gender == 'F':
                    self.people[self.key].father_id = parentone
                    self.people[self.key].mother_id = parenttwo
                elif pone_gender == 'F' and ptwo_gender == 'M':
                    self.people[self.key].mother_id = parentone
                    self.people[self.key].father_id = parenttwo
                else:
                    raise Exception('Gender error in attaching parents')

                if self.people[parentone].children:
                    self.people[parentone].children.append(self.key)
                else:
                    self.people[parentone].children = [self.key]

                if self.people[parenttwo].children:
                    self.people[parenttwo].children.append(self.key)
                else:
                    self.people[parenttwo].children = [self.key]

                self.fatherButton.setText(self.people[self.key].father_id + ' - ' +
                                          self.people[self.people[self.key].father_id].nick_name)
                self.motherButton.setText(self.people[self.key].mother_id + ' - ' +
                                          self.people[self.people[self.key].mother_id].nick_name)

            elif self.attach == 'child':
                self_gender = self.people[self.key].gender
                spouse = self.spouseList.currentItem().text()[:3]
                spouse_gender = self.people[spouse].gender
                child = self.primaryList.currentItem().text()[:3]

                if self.people[self.key].children:
                    self.people[self.key].children.append(child)
                else:
                    self.people[self.key].children = [child]

                if self.people[spouse].children:
                    self.people[spouse].children.append(child)
                else:
                    self.people[spouse].children = [child]

                if self_gender == 'M' and spouse_gender == 'F':
                    self.people[child].father_id = self.key
                    self.people[child].mother_id = spouse
                elif self_gender == 'F' and spouse_gender == 'M':
                    self.people[child].father_id = spouse
                    self.people[child].mother_id = self.key
                else:
                    raise Exception('Gender error in attaching parents')

                self.childrenList.clear()
                for a in self.process_kids(self.key):
                    self.childrenList.addItem(a)
                    self.childrenList.setCurrentRow(0)

        self.enable_inputs(True)
        self.primaryList.clear()
        self.primaryList.hide()
        self.primaryListLabel.hide()
        self.secondaryList.clear()
        self.secondaryList.hide()
        self.secondaryListLabel.hide()
        self.saveBox.hide()

    def unattach_parents(self):
        father = self.people[self.key].father_id
        mother = self.people[self.key].mother_id

        if father:
            self.people[self.key].update('father_id', '')
            self.people[father].children.remove(self.key)
        if mother:
            self.people[self.key].update('mother_id', '')
            self.people[mother].children.remove(self.key)

    def unattach_spouse(self, spouse = ''):
        if not spouse:
            spouse = child = self.spouseList.currentItem().text()[:3]
        if self.have_common_children(self.key, spouse):
            print('Common children. Cannot unattach')
        else:
            for p in self.people[self.key].marriage:
                try:
                    m = re.match('^[DM]' + spouse + '[_*a-zA-Z0-9]*', p)
                    mine = m.group()
                    yours = m.group()[0] + self.key + m.group()[4:]
                    self.people[self.key].marriage.remove(mine)
                    if not self.people[self.key].marriage:
                        self.people[self.key].marriage = 'S000'
                    self.people[spouse].marriage.remove(yours)
                    if not self.people[spouse].marriage:
                        self.people[spouse].marriage = 'S000'
                except AttributeError:
                    pass

    def have_common_children(self, key, spouse):
        for ch1 in self.people[key].children:
            for ch2 in self.people[spouse].children:
                if ch1 and ch1 == ch2:
                    return True
        return False

    def unattach_child(self, child = ''):
        if not child:
            child = self.childrenList.currentItem().text()[:3]
        if self.people[child].father_id == self.key:
            other_parent = self.people[child].mother_id
        elif self.people[child].mother_id == self.key:
            other_parent = self.people[child].father_id
        else:
            print('booboo in unattach_child')

        self.people[child].update('father_id', '')
        self.people[child].update('mother_id', '')
        self.people[self.key].children.remove(child)
        self.people[other_parent].children.remove(child)

    def unattach_all(self):
        self.unattach_parents()
        for a in self.people[self.key].children[:]:
            self.unattach_child(a)
        for a in self.people[self.key].marriage[:]:
            self.unattach_spouse(a[1:4])


    def marital_check_for_create_child(self, person, spouse):
        for a in self.people[person].marriage:
                if a[1:4] == spouse and a[0] in ['M', 'D']:
                    return True
        return False

    def spouse_window(self):
        try:
            self.spouseWindow = SpouseDialog(self.key, self.spouseList.currentItem().text()[:3], self.people)
            self.spouseWindow.show()
        except AttributeError:
            pass

    def attacher_window(self):
        self.attacherWindow = AttacherDialog(self.key, self.people)
        self.attacherWindow.show()

    def delete_person(self):
        if len(self.people) < 2:
            print('Cannot delete last person')
            return

        father = self.people[self.key].father_id
        mother = self.people[self.key].mother_id
        spouse = self.people[self.key].marriage
        children = self.people[self.key].children

        if father:
            self.people[father].children.remove(self.key)
        if mother:
            self.people[mother].children.remove(self.key)

        if spouse != ['S000']:
            for sp in spouse:
                for m in self.people[sp[1:4]].marriage:
                    if m[1:4] == self.key:
                        self.people[sp[1:4]].marriage.remove(m)
                        if self.people[sp[1:4]].marriage == []:
                            self.people[sp[1:4]].marriage = ['S000']

        if children:
            for child in children:
                if self.people[self.key].gender == 'M':
                    self.people[child].father_id = ''
                elif self.people[self.key].gender == 'F':
                    self.people[child].mother_id = ''
        self.people.pop(self.key)
        self.peopleList.takeItem(self.peopleList.row(self.peopleList.currentItem()))

    def open_father(self):
        try:
            self.peopleList.setCurrentItem(self.peopleList.findItems(self.fatherButton.text(), Qt.MatchExactly)[0])
        except IndexError:
            pass

    def open_mother(self):
        try:
            self.peopleList.setCurrentItem(self.peopleList.findItems(self.motherButton.text(), Qt.MatchExactly)[0])
        except IndexError:
            pass

    def open_spouse(self, item):
        try:
            self.peopleList.setCurrentItem(self.peopleList.findItems(item.text(), Qt.MatchExactly)[0])
        except IndexError:
            self.peopleList.setCurrentItem(self.peopleList.findItems(item.text()[:item.text().index(' (')], Qt.MatchExactly)[0])

    def open_child(self, item):
        self.peopleList.setCurrentItem(self.peopleList.findItems(item.text(), Qt.MatchExactly)[0])


    def get_marital_death(self):
        d1 = self.people[self.key].dday
        d2 = self.people[self.spouse].dday

        d1 = '' if d1 == '0' else d1
        d2 = '' if d2 == '0' else d2

        if d1 and not d2:
            return d1
        if d2 and not d1:
            return d2
        if not d1 and not d2:
            return ''

        if int(d1[:4]) < int(d2[:4]):
            return d1
        if int(d2[:4]) < int(d1[:4]):
            return d2
        if int(d1[4:6]) < int(d2[4:6]):
            return d1
        if int(d2[4:6]) < int(d1[4:6]):
            return d2
        if int(d1[6:]) < int(d2[6:]):
            return d1
        if int(d2[6:]) < int(d1[6:]):
            return d2


    def marital_info(self, cur, prev):
        months = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May',
          '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct',
          '11':'Nov', '12':'Dec'}

        single = False
        self.spouse = ''
        try:
            # self.spouse = self.spouseList.currentItem().text()[:3]
            self.spouse = cur.text()[:3]
        except AttributeError:
            self.spouseInfo.clear()
            # self.statusToEdit.clear()
            single = True
            status = 'S'


        m = d = ''
        for a in self.people[self.key].marriage:
            if a[1:4] == self.spouse:
                status = a[0]
                try:
                    m = a.split('_')[1].split('*')[0]
                except IndexError:
                    m = ''
                # try:
                #     d = a.split('_')[1].split('*')[1]
                # except IndexError:
                #     d = ''
        try:
            d = self.get_marital_death
        except KeyError as e:
            if e.args[0] == '':
                pass
            else:
                print("Unexpected error:", sys.exc_info())
                raise

        print(m,d)

        if status == 'S':
            self.firstStatusRadio.setText('Single')
            self.secondStatusRadio.hide()
            self.thirdStatusRadio.hide()
            # self.statusToEdit.setReadOnly(True)

            self.firstStatusRadio.setChecked(True)
        elif status in ['E', 'M', 'D']:
            self.firstStatusRadio.setText('Married')
            self.secondStatusRadio.setText('Engaged')
            self.thirdStatusRadio.setText('Divorced')
            self.secondStatusRadio.show()
            self.thirdStatusRadio.show()

            self.firstStatusRadio.setChecked(status == 'M')
            self.secondStatusRadio.setChecked(status == 'E')
            self.thirdStatusRadio.setChecked(status == 'D')
        else:
            raise Exception('Error in marital status retrieval in marital_info(self, cur, prev)')

        if single:
            return

        m_year = d_year = ''
        m_month = d_month = ''
        m_day = d_day = ''

        l = []
        if len(m) >= 4 and m[0:4] != 'xxxx':
            m_year = int(m[0:4])
            l.append(m[0:4])
        if len(m) >= 6:
            m_month = int(m[4:6])
            l.append(months[m[4:6]])
        if len(m) >= 8:
            l.append(m[6:8])

        m_out = '-'.join(l)

        l = []
        if len(d) >= 4:
            d_year = int(d[0:4])
            l.append(d[0:4])
        if len(d)>= 6:
            d_month = int(d[4:6])
            if len(l) == 1:
                    l.append(months[d[4:6]])
        if len(d) >= 8:
            d_day = int(d[6:8])
            if len(l) == 2:
                    l.append(d[6:8])

        d_out = '-'.join(l)

        age = -1
        if m_year and d_year:
            if m_month and d_month:
                if m_day and d_day:
                    if (d_month > m_month) or (d_month == m_month and d_day >= m_day):
                        age = d_year - m_year
                    else:
                        age = d_year - m_year - 1
                else:
                    if d_month >= m_month:
                        age = d_year - m_year
                    else:
                        age = d_year - m_year - 1
            else:
                age = d_year - m_year
        else:
            now = datetime.datetime.now()
            if m_year:
                if m_month:
                    if m_day:
                        if (now.month > m_month) or (now.month == m_month and now.day >= m_day):
                            age = now.year - m_year
                        else:
                            age = now.year - m_year - 1
                    else:
                        if now.month >= m_month:
                            age = now.year - m_year
                        else:
                            age = now.year - m_year - 1
                else:
                    age = now.year - m_year

        p = ''
        # if age >= 0:
        #     p = '{} years'.format(age)
        #
        # if m_out:
        #     if p:
        #         p += ' - {}'.format(m_out)
        #     else:
        #         p = m_out
        #     if d_out:
        #         p += ' to {}'.format(d_out)
        #     else:
        #         if self.spouse and not (self.people[self.key].death or self.people[self.spouse].death):
        #             p += ' to present'
        if m_out:
            p = m_out
            if age >= 0 and status == 'M':
                p += ' ({} years)'.format(age)
        self.spouseInfo.setText(p)

        if d_out:
            pass
            # self.statusToEdit.setText(d_out)
        elif status == 'M' and m_out:
            pass
            # self.statusToEdit.setText('present')
        else:
            pass
            # self.statusToEdit.clear()

    def move_spouse_up(self):
        spouse = self.spouseList.currentItem().text()[:3]
        for n, p in enumerate(self.people[self.key].marriage):
            m = re.match('^[EDM]' + self.spouse + '[_*a-zA-Z0-9]*', p)
            try:
                if p == m.group():
                    self.people[self.key].marriage[n], self.people[self.key].marriage[n-1] = self.people[self.key].marriage[n-1], self.people[self.key].marriage[n]
                    break
            except AttributeError:
                # print(sys.exc_info())
                pass

        # for n, p in enumerate(self.people[self.spouse].marriage):
        #     m = re.match('^[EDM]' + self.key + '[_*a-zA-Z0-9]*', p)
        #     try:
        #         if p == m.group():
        #             self.people[self.spouse].marriage[n] = status + self.people[self.spouse].marriage[n][1:]
        #             break
        #     except AttributeError:
        #         # print(sys.exc_info())
        #         pass
        self.spouseList.clear()
        for a in self.process_marriage(self.key):
            self.spouseList.addItem(a)
            self.spouseList.setCurrentRow(0)

    def move_spouse_down(self):
        spouse = self.spouseList.currentItem().text()[:3]
        for n, p in enumerate(self.people[self.key].marriage):
            m = re.match('^[EDM]' + self.spouse + '[_*a-zA-Z0-9]*', p)
            try:
                if p == m.group():
                    self.people[self.key].marriage[n], self.people[self.key].marriage[n+1] = self.people[self.key].marriage[n+1], self.people[self.key].marriage[n]
                    break
            except AttributeError:
                # print(sys.exc_info())
                pass

        self.spouseList.clear()
        for a in self.process_marriage(self.key):
            self.spouseList.addItem(a)
            self.spouseList.setCurrentRow(0)

    def move_child_up(self):
        child = self.childrenList.currentItem().text()[:3]
        for n, p in enumerate(self.people[self.key].children):
            if child == p:
                self.people[self.key].children[n], self.people[self.key].children[n-1] = self.people[self.key].children[n-1], self.people[self.key].children[n]
                c1 = self.people[self.key].children[n]
                c2 = self.people[self.key].children[n-1]
                break

        if self.people[c1].father_id == self.people[c2].father_id and self.people[c1].mother_id == self.people[c2].mother_id:
            parent = self.people[c1].mother_id if self.people[c1].father_id == self.key else self.people[c1].father_id
            i1 = self.people[parent].children.index(c1)
            i2 = self.people[parent].children.index(c2)
            self.people[parent].children[i1], self.people[parent].children[i2] = self.people[parent].children[i2], self.people[parent].children[i1]

        self.childrenList.clear()
        for a in self.process_kids(self.key):
            self.childrenList.addItem(a)

    def move_child_down(self):
        child = self.childrenList.currentItem().text()[:3]
        for n, p in enumerate(self.people[self.key].children):
            if child == p:
                c1 = self.people[self.key].children[n]
                c2 = self.people[self.key].children[n+1]
                self.people[self.key].children[n], self.people[self.key].children[n+1] = self.people[self.key].children[n+1], self.people[self.key].children[n]
                break

        if self.people[c1].father_id == self.people[c2].father_id and self.people[c1].mother_id == self.people[c2].mother_id:
            parent = self.people[c1].mother_id if self.people[c1].father_id == self.key else self.people[c1].father_id
            i1 = self.people[parent].children.index(c1)
            i2 = self.people[parent].children.index(c2)
            self.people[parent].children[i1], self.people[parent].children[i2] = self.people[parent].children[i2], self.people[parent].children[i1]

        self.childrenList.clear()
        for a in self.process_kids(self.key):
            self.childrenList.addItem(a)

    def update_status(self):
        if self.firstStatusRadio.isChecked() and self.sender().text() == 'Married':
            status = 'M'
            # self.statusToEdit.setReadOnly(True)
        elif self.secondStatusRadio.isChecked() and self.sender().text() == 'Engaged':
            status = 'E'
            # self.statusToEdit.setReadOnly(True)
        elif self.thirdStatusRadio.isChecked() and self.sender().text() == 'Divorced':
            status = 'D'
            # self.statusToEdit.setReadOnly(False)
        else:
            # self.statusToEdit.setReadOnly(True)
            return

        for n, p in enumerate(self.people[self.key].marriage):
            m = re.match('^[EDM]' + self.spouse + '[_*a-zA-Z0-9]*', p)
            try:
                if p == m.group():
                    self.people[self.key].marriage[n] = status + self.people[self.key].marriage[n][1:]
                    break
            except AttributeError:
                # print(sys.exc_info())
                pass

        for n, p in enumerate(self.people[self.spouse].marriage):
            m = re.match('^[EDM]' + self.key + '[_*a-zA-Z0-9]*', p)
            try:
                if p == m.group():
                    self.people[self.spouse].marriage[n] = status + self.people[self.spouse].marriage[n][1:]
                    break
            except AttributeError:
                # print(sys.exc_info())
                pass

    def update_anniversary(self):
        txt = self.spouseInfo.text()
        formats = ['%Y%m%d', '%Y%m', '%Y', '%m%d', '%m']
        m = re.match('^[0-9]{8}$|'
                     '^[0-9]{6}$|'
                     '^[0-9]{4}$|'
                     '^[x]{4}[0-9]{2}$|'
                     '^[x]{4}[0-9]{4}$', txt)

        if m:
            for frmt in formats:
                try:
                    if datetime.datetime.strptime(txt, frmt):
                        date = txt
                        break
                except ValueError:
                    try:
                        if datetime.datetime.strptime(txt.replace('x', ''), frmt):
                            date = txt
                            break
                    except ValueError:
                        pass

        for n, p in enumerate(self.people[self.key].marriage):
            m = re.match('^[DM]' + self.spouse + '[_*a-zA-Z0-9]*', p)
            try:
                if p == m.group():
                    start_i = end_i = ''
                    try:
                        start_i = self.people[self.key].marriage[n].index('_') + 1
                    except ValueError:
                        pass
                    try:
                        end_i = self.people[self.key].marriage[n].index('*')
                    except ValueError:
                        pass

                    if start_i and end_i:
                        self.people[self.key].marriage[n] = self.people[self.key].marriage[n][:start_i] + \
                            txt + self.people[self.key].marriage[n][end_i:]
                    elif start_i:
                        self.people[self.key].marriage[n] = self.people[self.key].marriage[n][:start_i] + txt
                    else:
                        self.people[self.key].marriage[n] = self.people[self.key].marriage[n] + '_' + txt

                    print(self.people[self.key].marriage[n])
                break
            except AttributeError:
                pass
                # print('close_spouse_window attribute error')

        for n, p in enumerate(self.people[self.spouse].marriage):
            m = re.match('^[DM]' + self.key + '[_*a-zA-Z0-9]*', p)
            try:
                if p == m.group():
                    start_i = end_i = ''
                    try:
                        start_i = self.people[self.spouse].marriage[n].index('_') + 1
                    except ValueError:
                        pass
                    try:
                        end_i = self.people[self.spouse].marriage[n].index('*')
                    except ValueError:
                        pass

                    if start_i and end_i:
                        self.people[self.spouse].marriage[n] = self.people[self.spouse].marriage[n][:start_i] + \
                            txt + self.people[self.spouse].marriage[n][end_i:]
                    elif start_i:
                        self.people[self.spouse].marriage[n] = self.people[self.spouse].marriage[n][:start_i] + txt
                    else:
                        self.people[self.spouse].marriage[n] = self.people[self.spouse].marriage[n] + '_' + txt
                break
            except AttributeError:
                pass

        self.marital_info(self.spouseList.currentItem(), None)

    def update_end_marriage(self):
        # txt = self.statusToEdit.text()
        formats = ['%Y%m%d', '%Y%m', '%Y']
        m = re.match('^[0-9]{8}$|'
                     '^[0-9]{6}$|'
                     '^[0-9]{4}$', txt)

        if m:
            for frmt in formats:
                try:
                    if datetime.datetime.strptime(txt, frmt):
                        date = txt
                        break
                except ValueError:
                    pass

        for n, p in enumerate(self.people[self.key].marriage):
            m = re.match('^[D]' + self.spouse + '[_*a-zA-Z0-9]*', p)
            try:
                if p == m.group():
                    start_i = ''
                    try:
                        start_i = self.people[self.key].marriage[n].index('*') + 1
                    except ValueError:
                        pass

                    if start_i:
                        self.people[self.key].marriage[n] = self.people[self.key].marriage[n][:start_i] + txt
                    else:
                        self.people[self.key].marriage[n] = self.people[self.key].marriage[n] + '*' + txt

                    print(self.people[self.key].marriage[n])
                break
            except AttributeError:
                pass
                # print('close_spouse_window attribute error')

        for n, p in enumerate(self.people[self.spouse].marriage):
            m = re.match('^[D]' + self.key + '[_*a-zA-Z0-9]*', p)
            try:
                if p == m.group():
                    start_i = ''
                    try:
                        start_i = self.people[self.spouse].marriage[n].index('*') + 1
                    except ValueError:
                        pass

                    if start_i:
                        self.people[self.spouse].marriage[n] = self.people[self.spouse].marriage[n][:start_i] + txt
                    else:
                        self.people[self.spouse].marriage[n] = self.people[self.spouse].marriage[n] + '*' + txt

                    print(self.people[self.spouse].marriage[n])
                break
            except AttributeError:
                pass

    def exitApp(self):
        sys.exit(0)

#
# class SpouseDialog(QMainWindow, spouse.Ui_MainWindow):
#     status = ''
#     marriage = ''
#     m_out = ''
#     divorce = ''
#     d_out = ''
#     people = {}
#     key = ''
#     spouse = ''
#
#     months = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May',
#           '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct',
#           '11':'Nov', '12':'Dec'}
#
#     def __init__(self, key, spouse, people, parent=None):
#         super().__init__()
#         self.setupUi(self)
#
#         # print(key, spouse, people[key].marriage)
#         self.people = people
#         self.key = key
#         self.spouse = spouse
#         for a in people[key].marriage:
#             if a[1:4] == spouse:
#                 self.status = a[0]
#                 try:
#                     self.marriage = a.split('_')[1].split('*')[0]
#                 except IndexError:
#                     self.marriage = ''
#                 try:
#                     self.divorce = a.split('_')[1].split('*')[1]
#                 except IndexError:
#                     pass
#                 # print(self.marriage)
#
#         # print(self.marriage, self.divorce)
#         self.init_fields()
#
#         self.engagedButton.toggled.connect(self.update_status)
#         self.marriedButton.toggled.connect(self.update_status)
#         self.divorcedButton.toggled.connect(self.update_status)
#
#         self.marriageEdit.editingFinished.connect(self.update_marriage)
#         self.separationEdit.editingFinished.connect(self.update_divorce)
#
#         self.buttonBox.clicked.connect(self.close_spouse_window)
#
#     def init_fields(self):
#         if self.marriage:
#             self.dates()
#         self.engagedButton.setChecked(self.status == 'E')
#         self.marriedButton.setChecked(self.status == 'M')
#         self.divorcedButton.setChecked(self.status == 'D')
#         if self.status != 'D':
#             self.separationEdit.setEnabled(False)
#
#         self.marriageEdit.setText(self.m_out)
#         self.separationEdit.setText(self.d_out)
#
#
#     def dates(self):
#         l = []
#         m_year = ''
#         m_month = ''
#         m_day = ''
#         d_year = ''
#         d_month = ''
#         d_day = ''
#         if len(self.marriage) >= 4 and self.marriage[0:4] != 'xxxx':
#             m_year = int(self.marriage[0:4])
#             l.append(self.marriage[0:4])
#         if len(self.marriage)>= 6:
#             m_month = int(self.marriage[4:6])
#             l.append(self.months[self.marriage[4:6]])
#         if len(self.marriage) >= 8:
#             m_day = int(self.marriage[6:8])
#             l.append(self.marriage[6:8])
#
#         self.m_out = '-'.join(l)
#
#         if self.status == 'D':
#             l = []
#             if len(self.divorce) >= 4:
#                 d_year = int(self.divorce[0:4])
#                 l.append(self.divorce[0:4])
#             if len(self.divorce)>= 6:
#                 d_month = int(self.divorce[4:6])
#                 if len(l) == 1:
#                     l.append(self.months[self.divorce[4:6]])
#             if len(self.divorce) >= 8:
#                 d_day = int(self.divorce[6:8])
#                 if len(l) == 2:
#                     l.append(self.divorce[6:8])
#
#             self.d_out = '-'.join(l)
#
#
#     def update_status(self):
#         if self.engagedButton.isChecked() and self.sender().text() == 'Engaged':
#             self.status = 'E'
#             self.separationEdit.setEnabled(False)
#         elif self.marriedButton.isChecked() and self.sender().text() == 'Married':
#             self.status = 'M'
#             self.separationEdit.setEnabled(False)
#         elif self.divorcedButton.isChecked() and self.sender().text() == 'Divorced':
#             self.status = 'D'
#             self.separationEdit.setEnabled(True)
#         else:
#             pass
#
#     def update_marriage(self):
#         if self.status in ['M', 'D']:
#             formats = ['%Y%m%d', '%Y%m', '%Y', '%m%d']
#             start = self.marriageEdit.text()
#             m = re.match('^[0-9]{8}$|'
#                          '^[0-9]{6}$|'
#                          '^[0-9]{4}$|', start)
#
#             if m:
#                 for frmt in formats:
#                     try:
#                         if datetime.datetime.strptime(start, frmt):
#                             self.marriage = start
#                             self.dates()
#                     except ValueError:
#                         pass
#                 # for n, p in enumerate(self.people[self.key].marriage):
#                 #     m = re.match('^[DMW]' + self.spouse + '[_a-zA-Z0-9]*', p)
#                 #     if p == m.group():
#                 #         self.people[self.key].marriage[n] = self.status + self.spouse + '_' + txt
#                 # print(self.marriageEdit.text(), m.group())
#
#             self.marriageEdit.setText(self.m_out)
#             # self.separationEdit.setText(self.d_out)
#
#
#     def update_divorce(self):
#         if self.status == 'D':
#             formats = ['%Y%m%d', '%Y%m', '%Y', '%m%d']
#             start = self.marriage
#             end = self.separationEdit.text()
#             m = re.match('^[0-9]{8}$|'
#                          '^[0-9]{6}$|'
#                          '^[0-9]{4}$|', start)
#             n = re.match('^[0-9]{8}$|'
#                          '^[0-9]{6}$|'
#                          '^[0-9]{4}$|', end)
#
#             if m and n:
#                 for frmt1 in formats:
#                     for frmt2 in formats:
#                         # print(frmt1, frmt2)
#                         try:
#                             if datetime.datetime.strptime(start, frmt1) and datetime.datetime.strptime(end, frmt2):
#
#                                 b = datetime.datetime.strptime(start, frmt1)
#                                 d = datetime.datetime.strptime(end, frmt2)
#
#                                 if b < d:
#                                     self.divorce = end
#                                     self.dates()
#                                 else:
#                                     print('invalid')
#                         except ValueError:
#                             pass
#                         except:
#                             print(sys.exc_info())
#
#         # print(self.divorce)
#
#     def close_spouse_window(self, button):
#         # print(self.marriage, self.divorce)
#         if button.text().lower() == 'save':
#             for n, p in enumerate(self.people[self.key].marriage):
#                 m = re.match('^[DM]' + self.spouse + '[_*a-zA-Z0-9]*', p)
#                 try:
#                     if p == m.group():
#                         self.people[self.key].marriage[n] = self.status + self.spouse
#                         if self.marriage:
#                             self.people[self.key].marriage[n] += '_' + self.marriage
#                         if self.divorce:
#                             self.people[self.key].marriage[n] += '*' + self.divorce
#                 except AttributeError:
#                     pass
#                     # print('close_spouse_window attribute error')
#
#             for n, p in enumerate(self.people[self.spouse].marriage):
#                 m = re.match('^[DM]' + self.key + '[_*a-zA-Z0-9]*', p)
#                 try:
#                     if p == m.group():
#                         self.people[self.spouse].marriage[n] = self.status + self.key
#                         if self.marriage:
#                             self.people[self.spouse].marriage[n] += '_' + self.marriage
#                         if self.divorce:
#                             self.people[self.spouse].marriage[n] += '*' + self.divorce
#                 except AttributeError:
#                     pass
#                     # print('close_spouse_window attribute error')
#
#         self.hide()
#
# class AttacherDialog(QMainWindow, attacher.Ui_MainWindow):
#     def __init__(self, key, people, parent=None):
#         super().__init__()
#         self.setupUi(self)
#
#         self.key = key
#         self.people = people
#
#         self.radioSpouse.toggled.connect(self.spouse_mode)
#         self.radioParents.toggled.connect(self.parents_mode)
#         self.radioChild.toggled.connect(self.child_mode)
#
#         self.primarylist.currentItemChanged.connect(self.select_in_list)
#         self.secondarylist.currentItemChanged.connect(self.select_in_second_list)
#
#         self.buttonBox.clicked.connect(self.close_attacher_window)
#
#         self.radioSpouse.setChecked(True)
#
#     def select_in_list(self, cur, prev):
#         if cur:
#             self.key = cur.text()[:3]
#             self.secondarylist.clear()
#
#             if self.radioSpouse.isChecked():
#                 gender = 'F' if self.people[self.key].gender == 'M' else 'M'
#                 for a in sorted(self.people):
#                     if self.people[a].gender == gender:
#                         self.secondarylist.addItem(a + ' - ' + self.people[a].nick_name)
#
#                 self.secondarylist.setCurrentRow(0)
#
#             if self.radioParents.isChecked():
#                 self.secondparentlist.clear()
#                 for a in sorted(self.people):
#                     if self.marital_check(a):
#                         self.secondarylist.addItem(a + ' - ' + self.people[a].nick_name)
#
#                 self.secondarylist.setCurrentRow(0)
#
#             if self.radioChild.isChecked():
#                 self.spouseList.clear()
#                 for a in self.people[self.key].marriage:
#                     if a[0] in ['M', 'D']:
#                         self.spouseList.addItem(a[1:4] + ' - ' + self.people[a[1:4]].nick_name)
#                 self.spouseList.setCurrentRow(0)
#
#                 self.secondarylist.clear()
#                 for a in sorted(self.people):
#                     if not self.people[a].father_id and not self.people[a].mother_id and a != self.key:
#                         self.secondarylist.addItem(a + ' - ' + self.people[a].nick_name)
#
#     def select_in_second_list(self, cur, prev):
#         if cur:
#             if self.radioParents.isChecked():
#                 parent = cur.text()[:3]
#                 self.secondparentlist.clear()
#                 for a in self.people[parent].marriage:
#                     if a[0] in ['M', 'D']:
#                         self.secondparentlist.addItem(a[1:4] + ' - ' + self.people[a[1:4]].nick_name)
#                 self.secondparentlist.setCurrentRow(0)
#
#     def marital_check(self, person):
#         for a in self.people[person].marriage:
#                 if a[0] in ['M', 'D']:
#                     return True
#         return False
#
#     def spouse_mode(self):
#         if self.radioSpouse.isChecked() and self.sender().text() == 'Spouse':
#             self.spouselabel.hide()
#             self.spouseList.clear()
#             self.spouseList.hide()
#             self.parentlabel.hide()
#             self.secondparentlist.clear()
#             self.secondparentlist.hide()
#             self.radioEngaged.show()
#             self.radioMarried.show()
#             self.radioDivorced.show()
#             self.relationGroup.setFlat(False)
#
#             self.radioMarried.setChecked(True)
#
#             self.primarylist.clear()
#             for a in sorted(self.people):
#                 self.primarylist.addItem(a + ' - ' + self.people[a].nick_name)
#
#             self.primarylist.setCurrentRow(0)
#
#     def parents_mode(self):
#         if self.radioParents.isChecked() and self.sender().text() == 'Parents':
#             self.spouselabel.hide()
#             self.spouseList.clear()
#             self.spouseList.hide()
#             self.parentlabel.show()
#             self.secondparentlist.show()
#             self.radioEngaged.hide()
#             self.radioMarried.hide()
#             self.radioDivorced.hide()
#             self.relationGroup.setFlat(True)
#
#             self.primarylist.clear()
#             for a in sorted(self.people):
#                 if not (self.people[a].father_id or self.people[a].mother_id):
#                     self.primarylist.addItem(a + ' - ' + self.people[a].nick_name)
#             self.primarylist.setCurrentRow(0)
#
#     def child_mode(self):
#         if self.radioChild.isChecked() and self.sender().text() == 'Child':
#             self.spouselabel.show()
#             self.spouseList.show()
#             self.parentlabel.hide()
#             self.secondparentlist.clear()
#             self.secondparentlist.hide()
#             self.radioEngaged.hide()
#             self.radioMarried.hide()
#             self.radioDivorced.hide()
#             self.relationGroup.setFlat(True)
#
#             self.primarylist.clear()
#             for a in sorted(self.people):
#                 if self.marital_check(a):
#                     self.primarylist.addItem(a + ' - ' + self.people[a].nick_name)
#
#             self.primarylist.setCurrentRow(0)
#
#     def close_attacher_window(self, button):
#         # print(self.marriage, self.divorce)
#         if button.text().lower() == 'ok':
#             if self.radioSpouse.isChecked():
#                 if self.radioMarried.isChecked():
#                     status = 'M'
#                 elif self.radioEngaged.isChecked():
#                     status = 'E'
#                 elif self.radioDivorced.isChecked():
#                     status = 'D'
#                 else:
#                     raise Exception('error in getting status for spouse attacher')
#
#                 spouse = self.secondarylist.currentItem().text()[:3]
#                 if self.people[self.key].marriage[0][0] == 'S':
#                     self.people[self.key].marriage = [status + spouse]
#                 else:
#                     self.people[self.key].marriage.append(status + spouse)
#
#                 if self.people[spouse].marriage[0][0] == 'S':
#                     self.people[spouse].marriage = [status + self.key]
#                 else:
#                     self.people[spouse].marriage.append(status + self.key)
#
#             if self.radioParents.isChecked():
#                 parentone = self.secondarylist.currentItem().text()[:3]
#                 pone_gender = self.people[parentone].gender
#                 parenttwo = self.secondparentlist.currentItem().text()[:3]
#                 ptwo_gender = self.people[parenttwo].gender
#
#                 if pone_gender == 'M' and ptwo_gender == 'F':
#                     self.people[self.key].father_id = parentone
#                     self.people[self.key].mother_id = parenttwo
#                 elif pone_gender == 'F' and ptwo_gender == 'M':
#                     self.people[self.key].mother_id = parentone
#                     self.people[self.key].father_id = parenttwo
#                 else:
#                     raise Exception('Gender error in attaching parents')
#
#                 self.people[parentone].children.append(self.key)
#                 self.people[parenttwo].children.append(self.key)
#
#
#             if self.radioChild.isChecked():
#                 self_gender = self.people[self.key].gender
#                 spouse = self.spouseList.currentItem().text()[:3]
#                 spouse_gender = self.people[spouse].gender
#                 child = self.secondarylist.currentItem().text()[:3]
#
#                 self.people[self.key].children.append(child)
#                 self.people[spouse].children.append(child)
#
#                 if self_gender == 'M' and spouse_gender == 'F':
#                     self.people[child].father_id = self.key
#                     self.people[child].mother_id = spouse
#                 elif self_gender == 'F' and spouse_gender == 'M':
#                     self.people[child].father_id = spouse
#                     self.people[child].mother_id = self.key
#                 else:
#                     raise Exception('Gender error in attaching parents')
#
#         self.hide()
#
#     # def spouse_window(self):
#     #     try:
#     #         self.spouseWindow = SpouseDialog(self.key, self.spouseList.currentItem().text()[:3], self.people)
#     #         self.spouseWindow.show()
#     #     except AttributeError:
#     #         pass


def main():
    app = QApplication(sys.argv)
    form = MainDialog()

    form.show()
    app.exec_()

if __name__ == '__main__':
    main()