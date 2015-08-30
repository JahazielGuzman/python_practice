import csv
import re

"""
	This script will read in test.csv, cleanse it by normalizing 
	its bio field, changing state abbreviations
	to full state names, and write the cleansed csv to the file solution.csv
"""

# normalize text in the bio field by extracting all strings which dont include whitespace characters
def normalize(s):

	return re.findall("\S+",s)


# open test.csv as test_file and state_abbreviations.csv as state_file
# create a list named solution which will hold the cleansed csv file and
# a dictionary named state_abbrevs which will contain state_abbr:state_name key, value pairs.
def cleanse_csv():

	with open("test.csv","rb") as test_file:
     
		with open("state_abbreviations.csv", 'rb') as state_file:
			
			test_csv = csv.DictReader(test_file)
			state_dict = csv.DictReader(state_file)
			solution = []
			state_abbrevs = {}

			for row in state_dict:
       
				if row["state_abbr"] not in state_abbrevs:
					state_abbrevs[row["state_abbr"]] = row["state_name"]

			for row in test_csv:
       
				string_list = normalize(row["bio"])
				row["bio"] = " ".join(string_list)		# return space delimited words
				row["state"] = state_abbrevs[row["state"]]
				solution += [row]

	return solution, test_csv.fieldnames	# return a copy of the cleansed csv file and its field names

def main():

	solution, fields = cleanse_csv()

	# write the cleansed csv file to solution.csv
	with open("solution.csv", 'w') as solution_file:
		solution_writer = csv.DictWriter(solution_file, fieldnames = fields)
		solution_writer.writeheader()
    		for row in solution:
    			solution_writer.writerow(row)


# if script is run from the command line
if __name__ == "__main__":

		main()
