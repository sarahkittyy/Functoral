import sys
from interpreter.util import error, cleancode
from interpreter.util import cleancode
from interpreter.interpret import interpret

def main():
	# assert arguments are of correct size
	if len(sys.argv) != 2:
		error("Incorrect CLI args.")
	
	# get code
	code = ""
	with open(sys.argv[1], "r") as file:
		code = file.readlines()
		file.close()
	
	# clean up code
	clean_code = cleancode(code)
	
	# interpret the code
	interpret(clean_code)
	
	return 0
	

# init program
if __name__ == "__main__":
	main()