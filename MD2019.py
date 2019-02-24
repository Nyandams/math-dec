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

# The maximum time a group can take to run their script, in seconds
max_compute_time = 8.5

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

# Check that the folder exists
if not os.path.isdir(resultat_folder):
    raise FileNotFoundError("Resultat folder not found in: " + resultat_folder)

# Construct the path to the preference file
preference_path = data_folder + "/preferences" + ext + ".csv"

# Construct the path to the group file
group_path = resultat_folder + "/groupes" + ext + ".csv"

# List all the folder in the project folder
directory_list = os.listdir(project_folder)
directory_list.remove("DONNEES")
directory_list.remove("RESULTATS")

# For each group run thir script
for group_acronym in directory_list:
    print("Processing group " + group_acronym+ ": ")
    prog_path = project_folder + "/" + group_acronym + "/" + group_acronym + ".py"

    # Check that the file to run exists
    if not os.path.isfile(prog_path):
        print("The file " + group_acronym + ".py doesn't exists")
        continue

    args = [ "python", prog_path, "-" + ext]
    process = subprocess.Popen(args)

    out, err = process.communicate()
    print(out, err)
