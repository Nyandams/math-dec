import csv
import itertools
import time
import sys

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

def retrieveAppreciationsCSV(csv_file, number_of_student = None):
    """
    Retrieve the appreciations from a csv file
    :param csv_file: file location
    :param number_of_student: the number of student
    :type csv_file: str
    :type number_of_student: int
    :return: The Appreciations retrieved from the CSV file
    :rtype: Appreciations
    """
    try:
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
            if number_of_student != None:
                # in order to retrieve only the number of student we want
                subStudentNumbers = {}
                for key in range(number_of_student):
                    subStudentNumbers[key] = studentNumbers[key]
                del appreciations[number_of_student:]
                return Appreciations(subStudentNumbers, appreciations)

            return Appreciations(studentNumbers, appreciations)
    except IOError:
        print("Error while loading the file")
        return None

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

    def get_threshold_appreciation(self, id_student, threshold):
        """
        Get the threshold appreciation of a student towards others students
        :param id_student: number of the student
        :param threshold: param of the euristic
        :type id_student: int
        :type threshold: float
        :return: an appreciation
        :rtype: str
        """
        appreciation = ['AR', 'I', 'P', 'AB', 'B', 'TB']
        list_appreciation = []
        th = 0.0
        current_mention = -1

        for i in range(len(self.studentNumbers)):
            if i != id_student:
                list_appreciation.append(self.getAppreciation(id_student, i))

        while th < threshold:
            current_mention += 1
            th += (list_appreciation.count(appreciation[current_mention]) / len(list_appreciation))

        return appreciation[current_mention]


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
                    if student != otherStudent:
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

    def __init__(self, appreciations, nb_project=None, threshold=None ):
        """
        Initialize the repartitions
        :param appreciations: All the appreciations retrieve
        :param nb_project: number of group we need to form
        :param threshold: parameter of the euristic: between 0 and 1
        :type appreciations: Appreciations
        :type nb_project: int
        :type threshold: float
        :return: a list of repartition with the students number
        """
        students = []
        for key, value in appreciations.studentNumbers.items():
            students.append(key)
        self.students = students
        self.combinations = Combinations(students)
        self.appreciations = appreciations
        self.repartitions = []
        #for the euristic
        self.blacklist2 = []
        self.blacklist3 = []
        self.threshold = threshold



        if threshold is not None:
            for id_student in range(len(self.appreciations.studentNumbers)):
                combinations_blacklist = self.blacklisting(id_student=id_student)

                # in order to remove duplicate
                blacklist2_student = [x for x in combinations_blacklist.combination_2 if x not in self.blacklist2]
                blacklist3_student = [x for x in combinations_blacklist.combination_3 if x not in self.blacklist3]
                #blacklist2_student = list(set(combinations_blacklist.combination_2) - set(self.blacklist2))
                #blacklist3_student = list(set(combinations_blacklist.combination_3) - set(self.blacklist3))
                self.blacklist2 = self.blacklist2 + blacklist2_student
                self.blacklist3 = self.blacklist3 + blacklist3_student


        print("nb combi de 2 avant : " + str(len(self.combinations.combination_2)))
        print("nb combi de 3 avant : " + str(len(self.combinations.combination_3)))
        self.combinations.combination_2 = [x for x in self.combinations.combination_2 if x not in self.blacklist2]
        self.combinations.combination_3 = [x for x in self.combinations.combination_3 if x not in self.blacklist3]

        print("nb combi de 2 après : " + str(len(self.combinations.combination_2)))
        print("nb combi de 3 après : " + str(len(self.combinations.combination_3)))
        if nb_project is None:
            modulo = len(appreciations.studentNumbers) % 2
            if modulo == 0:
                nb_project = len(appreciations.studentNumbers)/2
            elif modulo == 1:
                nb_project = (len(appreciations.studentNumbers) - 1)/2

        self.nb_g2 = nb_project - (len(students) - 2 * nb_project)
        self.nb_g3 = nb_project - self.nb_g2


    def blacklisting(self, id_student):
        """
        Return a blacklist for a specific student
        :param id_student: id of the student
        :type id_student: int
        :return: a black list
        :rtype: Combinations
        """
        threshold_mention = self.appreciations.get_threshold_appreciation(id_student=1, threshold=self.threshold)
        list_student_blacklist = []
        blacklist_group_2 = []
        blacklist_group_3 = []
        list_student_blacklist.append(id_student)
        for other_student in range(len(self.appreciations.studentNumbers)):
            if not superior_appreciation(self.appreciations.getAppreciation(id_student, other_student), threshold_mention) and id_student != other_student:
                group2_blacklisted = [id_student, other_student]
                group2_blacklisted.sort()
                blacklist_group_2.append(tuple(group2_blacklisted))

                for other_student_3 in range(len(self.appreciations.studentNumbers)):
                    if other_student_3 != id_student and other_student_3 != other_student:
                        group3_blacklisted = [id_student, other_student, other_student_3]
                        group3_blacklisted.sort()
                        blacklist_group_3.append(tuple(group3_blacklisted))

        list_student_blacklist.sort()
        blacklist_combinations = Combinations([])
        blacklist_combinations.combination_2 = blacklist_group_2
        blacklist_combinations.combination_3 = blacklist_group_3
        return blacklist_combinations


    def addRepartition(self, repartition):
        """
        Add a repartition to the list of repartitions
        :param repartition: a repartition
        :type repartition: Repartition
        """
        self.repartitions.append(repartition)

    def generateRepartitions(self, number_max_repartition = sys.maxsize):
        """
        Generate all the repartitions
        :param number_max_repartition: the number max of repartition we want to send
        :type number_max_repartition: int
        :return: list of Repartition
        :rtype: list
        """

        max_appreciation = 'AR'
        # we get all the combinaison of group of 3 people
        repartitions_g3 = generateAllGroups(self.combinations.combination_3, self.nb_g3)

        if self.nb_g3 == 0:  # case where we don't have groups of 3
            remaining_students = self.students.copy()
            combi_remaining_g2 = list(itertools.combinations(remaining_students, 2))
            combi_remaining_g2 = [x for x in combi_remaining_g2 if x not in self.blacklist2]
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
                    combi_remaining_g2 = [x for x in combi_remaining_g2 if x not in self.blacklist2]
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

        # printSatisfactionRepartition(self.repartitions[0])
        # we gather the students numbers in order to send the results
        list_affichage = []

        if len(repartitions_equality_separation) < number_max_repartition:
            for repartition in repartitions_equality_separation:
                repartition_num_etu = []
                for group in repartition.repartition:
                    group_num_etu = []
                    for idStudent in group:
                        group_num_etu.append(self.appreciations.studentNumbers[idStudent])
                    repartition_num_etu.append(group_num_etu)

                list_affichage.append(repartition_num_etu)
        else:
            for idRep in range(number_max_repartition):
                repartition_num_etu = []
                for group in repartitions_equality_separation[idRep].repartition:
                    group_num_etu = []
                    for idStudent in group:
                        group_num_etu.append(self.appreciations.studentNumbers[idStudent])
                    repartition_num_etu.append(group_num_etu)

                list_affichage.append(repartition_num_etu)

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
launch_mode = "exhaustif"
number_results_max = None
for arg in sys.argv[1:]:
    sub_arg = arg[2:]
    if sub_arg[:3] == "arg":
        launch_mode = sub_arg[4:]
    elif sub_arg[:3] == "num":
        number_results_max = int(float(sub_arg[7:]))
    elif sub_arg[:3] == "ext":
        ext = sub_arg[4:]

appreciations = retrieveAppreciationsCSV('../DONNEES/preferences' + ext + '.csv', number_of_student= 11)     # we define the number of students

#we have to modify the threshold in order to configure the euristic
if launch_mode == "exhaustif":
    repartitions = Repartitions(appreciations=appreciations)  # we define the number of group we need to form
elif launch_mode == "reel":
    repartitions = Repartitions(appreciations=appreciations, threshold=0.5)  # we define the number of group we need to form

if number_results_max is None:
    repartitions_get = repartitions.generateRepartitions()
else:
    repartitions_get = repartitions.generateRepartitions(number_results_max)
print(str(len(repartitions_get)) + " répartitions")

createCSVFile(repartitions_get)

print("--- %s seconds ---" % (time.time() - start_time))

