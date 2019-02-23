import csv

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


def retrieveAppreciations():
    with open('preferences.csv') as preferences:
        csv_reader = csv.reader(preferences, delimiter=',')
        line_count = 0
        nameCorrelation = {0: ''}
        appreciations = []

        for row in csv_reader:
            if line_count == 0:  # Retrieve student names
                for pos, name in enumerate(row):
                    nameCorrelation[pos - 1] = name
                line_count += 1
            else:
                row.pop(0)
                appreciations.append(row)
                line_count += 1
        del nameCorrelation[-1]
        return nameCorrelation, appreciations


nameCorrelation, appreciations = retrieveAppreciations()

print(appreciations)