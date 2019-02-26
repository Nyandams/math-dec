import csv
import itertools
import time


def printSatisfactionRepartition(repartition):
    """
    Print the satisfaction of each group in a repartition
    :param repartition: a repartion
    :type repartition: Repartition
    """
    for group in repartition.repartition:
        pref = []
        students = []
        for student in group:
            students.append(student)

        if len(group) == 2:
            pref1 = repartition.appreciations.getAppreciation(students[0], students[1])
            pref2 = repartition.appreciations.getAppreciation(students[1], students[0])
            pref.append((pref1, pref2))
        else:
            pref1 = repartition.appreciations.getAppreciation(students[0], students[1])
            pref2 = repartition.appreciations.getAppreciation(students[1], students[0])
            pref3 = repartition.appreciations.getAppreciation(students[2], students[0])
            pref4 = repartition.appreciations.getAppreciation(students[0], students[2])
            pref5 = repartition.appreciations.getAppreciation(students[1], students[2])
            pref6 = repartition.appreciations.getAppreciation(students[2], students[1])

            pref.append((pref1, pref2, pref3, pref4, pref5, pref6))
        print(pref)

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

        # in order to retrieve only the number of student we want
        subStudentNumbers = {}
        for key in range(number_of_student):
            subStudentNumbers[key] = studentNumbers[key]

        del appreciations[number_of_student:]

        return Appreciations(subStudentNumbers, appreciations)


def removeTripletFromCombinaison(combinaisons, triplet):
    """
    Remove all the combinaisons that contains one element of the triplet
    :param combinaisons: the list of combinaison where we want to delete some combinaisons
    :param triplet: the triplet of element we want to remove from combinaisons
    :type combinaisons: list
    :type triplet: tuple
    :return: a list of combinaisons
    :rtype: list
    """
    i = 0
    while i < len(combinaisons):
        if triplet[0] in combinaisons[i] or triplet[1] in combinaisons[i] or triplet[2] in combinaisons[i]:
            combinaisons.remove(combinaisons[i])
        else:
            i += 1
    return combinaisons


def removeCoupleFromCombinaison(combinaisons, triplet):
    """
    Remove all the combinaisons that contains one element of the couple
    :param combinaisons: the list of combinaison where we want to delete some combinaisons
    :param triplet: the couple of element we want to remove from combinaisons
    :type combinaisons: list
    :type triplet: tuple
    :return: a list of combinaisons
    :rtype: list
    """
    i = 0
    while i < len(combinaisons):
        if triplet[0] in combinaisons[i] or triplet[1] in combinaisons[i]:
            combinaisons.remove(combinaisons[i])
        else:
            i += 1
    return combinaisons


def generateAllGroups(combinaisons, nbGroup):
    """
    Generate all the repartition possible from a list and with a number of group defined
    :param combinaisons: All the combinaison
    :param nbGroup: the number of group in each repartition
    :type combinaisons: list
    :type nbGroup: int
    :return: all the repartition
    :rtype: list
    """
    repartitions = []
    if nbGroup != 0:
        for gp in combinaisons:
            rep_tmp = []
            rep_tmp.append(gp)
            remaining_combi_tmp = combinaisons.copy()
            if (len(gp) == 3):
                removeTripletFromCombinaison(remaining_combi_tmp, gp)
            else:
                removeCoupleFromCombinaison(remaining_combi_tmp, gp)
            sub_repartitions_tmp = generateAllGroups(remaining_combi_tmp, nbGroup - 1)
            if len(sub_repartitions_tmp) == 0:
                repartitions.append(rep_tmp)
            else:
                for sub_rep in sub_repartitions_tmp:
                    repartitions.append(rep_tmp + sub_rep)


    return repartitions


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


def superior_appreciation(appreciation1, appreciation2):
    """
    Return true if appreciation1 >= appreciation2
    :param appreciation1: first appreciation
    :param appreciation2: second appreciation
    :type appreciation1: str
    :type appreciation2: str
    :return: The Appreciations in order
    :rtype: bool
    """
    order = orderRelationship(appreciation1, appreciation2)

    return order[0] == appreciation1


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
        self.appreciations = appreciations

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
        self.students = students
        self.combination_2 = list(itertools.combinations(self.students, 2))
        self.combination_3 = list(itertools.combinations(self.students, 3))

class Repartition:
    """
    Class Repartition correspond to one of the Repartition that exists
    """

    def __init__(self, appreciations, repartition=None):
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

        # We get the list of all the appreciations of this repartition
        for group in self.repartition:
            for student in group:
                for otherStudent in group:
                    if student != group:
                        listAppreciation.append(self.appreciations.getAppreciation(student, otherStudent))

        while median < 0.5:
            currentMention += 1
            median += (listAppreciation.count(appreciation[currentMention]) / len(listAppreciation))

        return appreciation[currentMention]

    def get_lower_appreciation(self, appreciation):
        """
        Return the percentage of appreciation lower than the argument
        :param appreciation: an appreciation
        :return: a percentage
        :rtype: float
        """
        count_lower_appreciation = 0
        count_total = 0
        for group in self.repartition:
            for student in group:
                for otherStudent in group:
                    if student != otherStudent:
                        count_total += 1
                        if superior_appreciation(self.appreciations.getAppreciation(student, otherStudent), appreciation) == False:
                            count_lower_appreciation += 1

        return count_lower_appreciation/count_total


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
        :return: a list of repartition with the students number
        """
        students = []
        for key, value in appreciations.studentNumbers.items():
            students.append(key)
        self.students = students
        self.combinations = Combinations(students)
        self.appreciations = appreciations
        self.repartitions = []
        self.nb_g2 = nb_project - (len(students) - 2 * nb_project)
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

        max_appreciation = 'AR'
        # we get all the combinaison of group of 3 people
        repartitions_g3 = generateAllGroups(self.combinations.combination_3, self.nb_g3)

        if self.nb_g3 == 0:  # case where we don't have groups of 3
            remaining_students = self.students.copy()
            combi_remaining_g2 = list(itertools.combinations(remaining_students, 2))
            repartitions_g2 = generateAllGroups(combi_remaining_g2, int(self.nb_g2))
            for rep_g2 in repartitions_g2:
                repartition_tmp = Repartition(self.appreciations, list(rep_g2))
                medianAppreciation = repartition_tmp.getMedianAppreciation()

                if superior_appreciation(medianAppreciation, max_appreciation):
                    if medianAppreciation == max_appreciation:
                        self.repartitions.append(repartition_tmp)
                    else:
                        self.repartitions.clear()
                        self.repartitions.append(repartition_tmp)
                        max_appreciation = medianAppreciation

        else:  # case where we have groups of 3
            for rep_g3 in repartitions_g3:

                if int(self.nb_g2) == 0:  # case where we have only group of 3
                    repartition_tmp = Repartition(self.appreciations, list(rep_g3))
                    medianAppreciation = repartition_tmp.getMedianAppreciation()

                    if superior_appreciation(medianAppreciation, max_appreciation):
                        if medianAppreciation == max_appreciation:
                            self.repartitions.append(repartition_tmp)
                        else:
                            self.repartitions.clear()
                            self.repartitions.append(repartition_tmp)
                            max_appreciation = medianAppreciation
                else:
                    remaining_students = self.students.copy()
                    for gp in rep_g3:
                        for student in gp:
                            remaining_students.remove(student)

                    # and we complete the repartition with groups of 2
                    combi_remaining_g2 = list(itertools.combinations(remaining_students, 2))
                    repartitions_g2 = generateAllGroups(combi_remaining_g2, int(self.nb_g2))
                    for rep_g2 in repartitions_g2:
                        repartition_tmp = Repartition(self.appreciations, list(rep_g3) + list(rep_g2))
                        medianAppreciation = repartition_tmp.getMedianAppreciation()

                        if superior_appreciation(medianAppreciation, max_appreciation):
                            if medianAppreciation == max_appreciation:
                                self.repartitions.append(repartition_tmp)
                            else:
                                self.repartitions.clear()
                                self.repartitions.append(repartition_tmp)
                                max_appreciation = medianAppreciation

        min_lower_appreciation = 100

        #we share the equality, we keep the one with the lowest rate of appreciation under max_appreciation
        repartitions_equality_separation = []
        for repartition in self.repartitions:
            if repartition.get_lower_appreciation(max_appreciation) < min_lower_appreciation:
                repartitions_equality_separation.clear()
                min_lower_appreciation = repartition.get_lower_appreciation(max_appreciation)
                repartitions_equality_separation.append(repartition)
            elif repartition.get_lower_appreciation(max_appreciation) == min_lower_appreciation:
                repartitions_equality_separation.append(repartition)


        print(len(self.repartitions))

        # printSatisfactionRepartition(self.repartitions[0])
        # we gather the students numbers in order to send the results
        list_affichage = []
        for repartition in repartitions_equality_separation:
            repartition_numEtu = []
            for group in repartition.repartition:
                group_numEtu = []
                for idStudent in group:
                    group_numEtu.append(self.appreciations.studentNumbers[idStudent])
                repartition_numEtu.append(group_numEtu)

            list_affichage.append(repartition_numEtu)
        return list_affichage

def createCSVFile(repartitions):
    """
    Write the CSV file
    :param repartitions: list of repartitions to write
    """
    with open('LSS.csv', 'w', newline="") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for rep in repartitions:
            repartition = []
            for group in rep:
                groupP = ""
                for student in group:
                    groupP = groupP + ' ' + str(student)
                repartition.append(groupP)
            filewriter.writerow(repartition)

start_time = time.time()
appreciations = retrieveAppreciationsCSV('preferences.csv', 10)     # we define the number of students
repartitions = Repartitions(appreciations, 4)  # we define the number of group we need to form
repartitions_obtenues = repartitions.generateRepartitions()
print(str(len(repartitions_obtenues)) + " appreciations")
print(repartitions_obtenues)
# print(len(repartitions_obtenues))
# print(repartitions_obtenues)

createCSVFile(repartitions_obtenues)

print("--- %s seconds ---" % (time.time() - start_time))

