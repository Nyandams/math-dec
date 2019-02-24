import csv
import itertools

def retrieveAppreciationsCSV(csv_file):
    """
    Retrieve the appreciations from a csv file
    :param csv_file: file location
    :type csv_file: str
    :return: The Appreciations retrieved from the CSV file
    :rtype: Appreciations
    """
    with open(csv_file) as preferences:
        csv_reader = csv.reader(preferences, delimiter=',')
        row_count = 0
        studentNumbers = {0: ''}
        appreciations = []

        for row in csv_reader:
            if row_count == 0:  # Retrieve student names
                for pos, name in enumerate(row):
                    studentNumbers[pos - 1] = name
                row_count += 1
            else:
                row.pop(0)
                appreciations.append(row)
                row_count += 1
        del studentNumbers[-1]
        return Appreciations(studentNumbers, appreciations)


class Appreciations:
    """
    Class Appreciations is responsible for access to the appreciation of one student on another
    """
    def __init__(self, studentNumbers, appreciations):
        """
        :param studentNumbers: A dictionary key:studentNumber
        :param appreciations: All the appreciations of the strudents
        :type studentNumbers: dict
        :type appreciations: list
        """
        self.studentNumbers = studentNumbers
        self.appreciations  = appreciations

    def getAppreciation(self, student1, student2):
        """
        Get the appreciation of student1 on student2
        :param student1: The student who gave his appreciation
        :param student2: The student on whom an appreciation has been given
        :type student1: int
        :type student2: int
        :return: The appreciation of student1 on student2
        :rtype: str
        """
        return self.appreciations[student1][student2]

class Combinations:
    """
    Class Combinaisons has the responsability to generate all the possible combination
    """
    def __init__(self, students):
        """
        :param students: A list of all the students
        :type students: list
        """
        self.students      = students
        self.combinaison_2 = []
        self.combinaison_3 = []

    def generateAllCombination(self):
        """
        Generate all the combinations possible
        :return:
        """
        self.combinaison_2 = itertools.combinations(self.students, 2)
        self.combinaison_3 = itertools.combinations(self.students, 3)

class Repartition:
    """
    Class Repartition correspond to one of the Repartition that exists
    """

    def __init__(self):
        """
        initialize a new repartition
        """
        self.repartition = []

    def addGroup(self, group):
        """
        Add a group to the repartition
        :param group: a group we want to add to the repartition
        :type group: list
        :return: nothing
        """
        self.repartition.append(group)





appreciations = retrieveAppreciationsCSV('preferences.csv')

students = []
for key, value in appreciations.studentNumbers.items():
    students.append(key)

combination = Combinations(students)
combination.generateAllCombination()
for comb in combination.combinaison_2:
    print(comb)

for comb in combination.combinaison_3:
    print(comb)