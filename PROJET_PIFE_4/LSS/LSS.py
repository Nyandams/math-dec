import json
import sys

t = [ [ [1, 2, 3], [4, 5, 6] ] , [ [ 7, 8, 9], [ 10, 11, 12 ] ] ]

json_str = json.dumps(t)

sys.stdout.write(json_str)