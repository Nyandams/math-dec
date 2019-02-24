import os
import sys
import subprocess

"""
    This script run other groups script.

    :author: Lucas Sardois
    :version: 1.0.0
"""

# The report number beeing processed
report_number = 4

# The maximum time a group can take to run their script
max_compute_time = 8.5

# Check that the script is run with the -EXT argument
if len(sys.argv) < 2:
    raise RuntimeError("You must specify the -EXT")

# Remove the "-" to just keep the EXT
ext = sys.argv[1][1:]

# Construct the path to the project folder
project_folder = "PROJET_PIFE_" + str(report_number)

# Construct the path to the preference file
preference_path = project_folder + "/DONNEES/preferences" + ext + ".csv"

# Construct the path to the group file
group_path = project_folder + "/RESULTATS/groupes" + ext + ".csv"

# List all the folder in the project folder
directory_list = os.listdir(project_folder)
directory_list.remove("DONNEES")
directory_list.remove("RESULTATS")

# For each group run thir script
for group_acronym in directory_list:
    print("Processing group " + group_acronym+ ": ")
    prog_path = group_acronym + "/" + group_acronym + ".py -" + ext

    # Check that the file to run exists
    if not os.path.isfile(prog_path):
        print("The file " + group_acronym + ".py doesn't exists")
        continue

    process = subprocess.Popen(prog_path)
