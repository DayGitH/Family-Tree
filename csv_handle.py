import csv
import person
import string

def load(file_name):
    ppl_list = {}
    
    with open(file_name, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        first_row = False
        for row in filereader:
            if not first_row:
                first_row = True
            else:
                [id, nick_name, real_name, bday, gender, father, mother, mar, chi, death_dte, notes] = row
                
                marriage = mar.split('-')
                
                if chi == '-':
                    children = chi
                else:
                    children = chi.split('-')
                    
                ppl_list[id] = person.person(id, nick_name, real_name, bday, gender, father, mother, marriage, children, death_dte, notes)
                
    return ppl_list

def save(file_name,ppl_list):
    with open(file_name, 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        filewriter.writerow(['ID','Spoken Name','Full Name','Bday','Gender','Father ID','Mother ID','Marriage','Children ID','Death dte','Notes'])
        for ppl in sorted(ppl_list):
            print(ppl)
            [id, nick_name, real_name, bday, gender, father_id, mother_id, mar, chi, death_dte, notes] = ppl_list[ppl].fetch()
            
            marriage = '-'.join(mar)
            children = '-'.join(chi)
            
            filewriter.writerow([id, nick_name, real_name, bday, gender, father_id, mother_id, marriage, children, death_dte, notes])

if __name__ == '__main__':
    people = load('Family tree test.csv')
    people['005'].display()
    
    save('Family 2.csv',people)