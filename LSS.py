import csv
import itertools
import operator as op
from functools import reduce

def ncr(n, k):
    """
    n choose k
    :param n:
    :param k:
    :return: the number of n choose r
    :rtype: int
    """
    k = min(k, n-k)
    numer = reduce(op.mul, range(n, n-k, -1), 1)
    denom = reduce(op.mul, range(1, k+1), 1)
    return numer / denom

def retrieveAppreciationsCSV(csv_file, number_of_student):
    """
    Retrieve the appreciations from a csv file
    :param csv_file: file location
    :param number_of_student: the number of student
    :type csv_file: str
    :type number_of_student: int
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

        #in order to retrieve only the number of student we want
        subStudentNumbers = {}
        for key in range(number_of_student):
            subStudentNumbers[key] = studentNumbers[key]

        del appreciations[number_of_student:]


        return Appreciations(subStudentNumbers, appreciations)


def orderRelationship(appreciation1, appreciation2):
    """
    Classify appreciations by the order relationship
    :param appreciation1: appreciation of the first student
    :param appreciation2: appreciation of the second student
    :type appreciation1: str
    :type appreciation2: str
    :return: The Appreciations in order
    :rtype: list
    """
    order = []

    if appreciation1 == 'TB':
        order = [appreciation1, appreciation2]
    elif appreciation2 == 'TB':
        order = [appreciation2, appreciation1]
    elif appreciation1 == 'AR':
        order = [appreciation2, appreciation1]
    elif appreciation2 == 'AR':
        order = [appreciation1, appreciation2]
    elif appreciation1 == 'B':
        order = [appreciation1, appreciation2]
    elif appreciation2 == 'B':
        order = [appreciation2, appreciation1]
    elif appreciation1 == 'AB':
        order = [appreciation1, appreciation2]
    elif appreciation2 == 'AB':
        order = [appreciation2, appreciation1]
    elif appreciation1 == 'P':
        order = [appreciation1, appreciation2]
    elif appreciation2 == 'P':
        order = [appreciation2, appreciation1]
    elif appreciation1 == 'I':
        order = [appreciation1, appreciation2]
    elif appreciation2 == 'I':
        order = [appreciation2, appreciation1]

    return order


class Appreciations:
    """
    Class Appreciations is responsible for access to the appreciation of one student on another
    """
    def __init__(self, studentNumbers, appreciations):
        """
        Initialize the Appreciations
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
        :rtype: list
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
        self.combination_2 = itertools.combinations(self.students, 2)
        self.combination_3 = itertools.combinations(self.students, 3)

class Repartition:
    """
    Class Repartition correspond to one of the Repartition that exists
    """

    def __init__(self, appreciations, repartition = None):
        """
        Initialize a new repartition
        :param appreciations: all the appreciations
        :param repartition: the repartition
        :type appreciations: Appreciations
        :type repartitions: list
        """
        self.appreciations = appreciations
        if repartitions is None:
            self.repartition = []
        else:
            self.repartition = repartition


    def addGroup(self, group):
        """
        Add a group to the repartition
        :param group: a group we want to add to the repartition
        :type group: list
        :return: nothing
        """
        self.repartition.append(group)

    def setRepartition(self, repartition):
        """
        Set the repartition
        :param repartition: set the repartition
        :type repartition: list
        """

    def getMedianAppreciation(self):
        """
        Get the median appreciation of the repartition
        :return: the appreciation (str)
        """
        appreciation = ['AR', 'I', 'P', 'AB', 'B', 'TB']
        listAppreciation = []
        median = 0.0
        currentMention = -1

        #We get the list of all the appreciations of this repartition
        for repart in self.repartition:
            for student in repart:
                for otherStudent in repart:
                    if student != otherStudent:
                        listAppreciation.append(self.appreciations.getAppreciation(student, otherStudent))

        while median < 0.5:
            currentMention += 1
            median += (listAppreciation.count(appreciation[currentMention]) / len(listAppreciation))

        return appreciation[currentMention]


class Repartitions:
    """
    Class Repartitions is responsible of the creation of all the Repartitions
    """

    def __init__(self, appreciations, nb_project):
        """
        Initialize the repartitions
        :param appreciations: All the appreciations retrieve
        :param nb_project: number of group we need to form
        :type appreciations: Appreciations
        :type nb_project: int
        """
        students = []
        for key, value in appreciations.studentNumbers.items():
            students.append(key)
        self.students = students
        self.combinations = Combinations(students)
        self.combinations.generateAllCombination()
        self.appreciations = appreciations
        self.repartitions = []
        self.nb_g2 = nb_project - (len(students) - 2*nb_project)
        self.nb_g3 = nb_project - self.nb_g2

    def addRepartition(self, repartition):
        """
        Add a repartition to the list of repartitions
        :param repartition: a repartition
        :type repartition: Repartition
        """
        self.repartitions.append(repartition)

    def generateRepartitions(self):
        """
        Generate all the repartitions
        """
        #we get all the combinaison of group of 3 people
        combi_g3 = itertools.combinations(self.combinations.combination_3, self.nb_g3)


        #then we get the combinaison of
        nb_combi2 = ncr(len(self.students) - 3*self.nb_g3,2)
        for repart_g3 in combi_g3:
            remaining_item = self.students.copy()
            for gp in repart_g3:
                for student in range(3):
                    remaining_item.remove(gp[student])

            remaining_combinations = itertools.combinations(remaining_item, 2)
            combi_remaining_g2 = itertools.combinations(remaining_combinations, int(self.nb_g2))

            for repart_g2 in combi_remaining_g2:
                repartition_tmp = Repartition(self.appreciations, list(repart_g3) + list(repart_g2))
                self.addRepartition(repartition_tmp)


appreciations = retrieveAppreciationsCSV('preferences.csv', 11)
repartitions  = Repartitions(appreciations, 5)
repartitions.generateRepartitions()

repartition = Repartition(appreciations, [[0,1,2], [3,4,5]])
print(repartition.getMedianAppreciation())
