import os
import sys
import csv
import json
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

# Construct the data folder
data_folder = project_folder + "/DONNEES"

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
    try:
        print("Processing group " + group_acronym+ ": ")
        prog_path = project_folder + "/" + group_acronym + "/" + group_acronym + ".py"

        # Check that the file to run exists
        if not os.path.isfile(prog_path):
            print("The file " + group_acronym + ".py doesn't exists")
            continue

        # Run the group' script
        args = [ "python3", prog_path, "-" + ext]
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=project_folder)

        stderr = None

        # Try to get errors back from the script with a timeout
        try:
            stdout, stderr = process.communicate(timeout=8.5)
            result[group_acronym] = []

            # Read the csv and save data for later
            try:
                group_path = project_folder + "/" + group_acronym + "/" + group_acronym + ".csv"
                with open(group_path, newline='') as group_file:
                    result_reader = csv.reader(group_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    
                    for row in result_reader:
                        result[group_acronym].append(row)

                    print(result[group_acronym])
                    group_file.close()
            except FileNotFoundError:
                print("The csv file was not found in: " + group_path)
                continue
            except:
                print("Error while reading the csv file in: " + group_path)
                continue

        except subprocess.TimeoutExpired:
            # In the case where the script was too long, 
            # just kill it and process the next group
            print("Script was too long")
            process.kill()
            continue

        # If stderr is not None then an error occured in
        # print the error and pass to the next script
        if stderr is not None:
            print(stderr.decode("utf-8"))
            continue
    except:
        print("Unknow error")
        continue

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