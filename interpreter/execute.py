from interpreter.expr import executeCall, getCalls

# executes all code
def execute(code, functions):
	# get an ordered list of calls
	calls = getCalls(code)
	
	# execute the calls
	executeCalls(calls, functions)
	
# executes a function
def executeCalls(calls, functions):
	# for every call
	for call in calls:
		# call it
		executeCall(call, functions)