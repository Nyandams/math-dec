import sys

"""
    This script run other groups script.

    :author: Lucas Sardois
    :version: 1.0.0
"""

# The report number beeing processed
report_number = 0

# The maximum time a group can take to run their script
max_compute_time = 8.5

# Check that the script is run with the -EXT argument
if len(sys.argv) < 2:
    raise RuntimeError("You must specify the -EXT")

# Remove the "-" to just keep the EXT
ext = sys.argv[1][1:]

# Construct the path to the preference file
preference_path = "IG4/PROJET_PIFE_" + str(report_number) + "/DONNEES/preferences" + ext + ".csv"

# Construct the path to the group file
group_path = "IG4/PROJET_PIFE_" + str(report_number) + "/RESULTATS/groupes" + ext + ".csv"

