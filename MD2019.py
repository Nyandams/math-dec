import os
import sys
import csv
import subprocess

"""
    This script run other groups script.

    :reference: Rendu numéro 4.

    :author: Lucas Sardois
    :date: 24/02/2019
    :version: 1.0.0
"""

# ==================================================================== #

# The report number beeing processed
report_number = 4

# The maximum time a group can take to run their script, in seconds
max_compute_time = 8.5

# ==================================================================== #

# Check that the script is run with the -EXT argument
if len(sys.argv) < 2:
    raise RuntimeError("You must specify the -EXT")

# Remove the "-" to just keep the EXT
ext = sys.argv[1][1:]

# Construct the path to the project folder
project_folder = "PROJET_PIFE_" + str(report_number)

# The python executable name it must python or python3
python_exec = "python3"

# Construct the data folder
data_folder = project_folder + "/DONNEES"
data_folder = os.path.join(project_folder, "DONNEES")

# Check that the folder exists
if not os.path.isdir(data_folder):
    raise FileNotFoundError("Data folder not found in: " + data_folder)

# Construct the resultat folder
resultat_folder = project_folder + "/RESULTATS"

# Construct the resultat path
resultat_path = resultat_folder + "/resultat" + ext + ".csv"

# Check that the folder exists
if not os.path.isdir(resultat_folder):
    raise FileNotFoundError("Resultat folder not found in: " + resultat_folder)

# Construct the path to the preference file
preference_path = data_folder + "/preferences" + ext + ".csv"

# Construct the path to the group file
group_path = resultat_folder + "/groupes" + ext + ".csv"

# Group assignment for all groups
result = { }

# List all the folder in the project folder
directory_list = os.listdir(project_folder)
directory_list.remove("DONNEES")
directory_list.remove("RESULTATS")

# For each group run thir script
for group_acronym in directory_list:
    print("Processing group " + group_acronym + ": ")
    group_folder = project_folder + "/" + group_acronym
    prog_path = group_folder + "/" + group_acronym + ".py"

    if not os.path.exists(prog_path):
        print("Can't load the script at: " + prog_path)
        continue

    # Run the group' script
    args = [python_exec, group_acronym + ".py", "-" + ext]
    try:
        process = subprocess.Popen(args, stderr=subprocess.PIPE, cwd=group_folder)
    except IOError:
        _, value, traceback = sys.exc_info()
        print('Error opening %s: %s' % (value.filename, value.strerror))
        continue

    stderr = None

    # Try to get errors back from the script with a timeout
    try:
        stdout, stderr = process.communicate(timeout=max_compute_time)
    except subprocess.TimeoutExpired:
        # In the case where the script was too long,
        # just kill it and process the next group
        process.kill()
        print("Script was too long")
        continue
    except:
        process.kill()
        print("Script crashed")
        continue

    # If stderr is not None then an error occured in
    # print the error and pass to the next script
    if stderr is not None and len(stderr) > 0:
        print(stderr.decode("utf-8"))
        continue

    process.kill()

    # Create the group acronym result set
    result[group_acronym] = []

    # Read the csv and save data for later
    group_csv_path = project_folder + "/" + group_acronym + "/" + group_acronym + ".csv"
    try:
        with open(group_csv_path, newline='') as group_file:
            result_reader = csv.reader(group_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            for row in result_reader:
                result[group_acronym].append(row)

            # print(result[group_acronym])
            group_file.close()

            print("\nGROUP OK")
    except IOError:
        _, value, traceback = sys.exc_info()
        print('Error opening the csv file %s: %s' % (value.filename, value.strerror))
        continue

ext = sys.argv[1][1:]

# Write in the CSV the result
with open(resultat_path, mode="w+", newline="") as result_file:
    result_writer = csv.writer(result_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for group_acronym in result:
        assignments = result[group_acronym]
        for assignment in assignments:
            # Add the group acronym
            assignment = [group_acronym] + assignment
            result_writer.writerow(assignment)
        
        result_writer.writerow("")

    result_file.close()