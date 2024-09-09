'''
Description: This script reads the before_and_after.txt file and extracts the 
before and after training outputs. It then calculates the BLEU score between 
the before and after outputs and writes the question, before, after, and 
BLEU score to a new file before_and_after.txt.
'''

# Import modules
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


# Function to calculate the BLEU score between the before and after outputs
'''
@params, question: str, before: str, after: str
@return: None
'''
def evaluate_bleu_score(question, before, after):
	# Calculate the BLEU score
	smooth_fn = SmoothingFunction().method1
	score = sentence_bleu([before.strip().split()], after.strip().split(), smoothing_function=smooth_fn)
	
	# If the BLEU score is less than 0.01, return
	if score < 0.01:
		return

	# Write the question, before, after, and BLEU score to a file
	with open('before_and_after.txt', 'a') as f:
		f.write(question[13:].strip() + '\n')
		f.write(before.strip() + '\n')
		f.write(after.strip() + '\n')
		f.write(str(score))
		f.write('\n\n')


# Function to extract the before and after outputs from the file
'''
@params, filename: str
'''
def extract_before_after(filename):
	# Initialize variables
	state = ""
	question = ""
	before = ""
	after = ""
	i = 0

	# Read the file line by line
	with open(filename, 'r') as file:
		for line in file:
			# Question
			if state == "" and "user prompt: " in line:
				question += line
				state = "question"
			# Before and after outputs
			elif state == "question" and len(line) == 2:
				state = "start" 
			if state == "start" and "BEFORE training" in line:
				state = "find start"
			elif state == "find start" and "==========" in line:
				state = "before"
			elif state == "before" and "==========" in line:
				state = "find after"
			elif state == "before":
				if len(line) != 2:
					before += line[:-1]
			elif state == "find after" and "==========" in line:
				state = "after"
			# Evaluate the BLEU score
			elif state == "after" and "==========" in line:
				state = ""
				evaluate_bleu_score(question, before, after)
				before = ""
				after = ""
				question = ""
			elif state == "after":
				if len(line) != 2:
					after += line[:-1]

extract_before_after('before_and_after.txt')
