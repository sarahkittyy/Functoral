import re
from interpreter.util import isGetOper, isNum, isIf, isGetCond, error, getInnerBlocks, callpredef

# asserts a value is a value, & evaluates it if it's not
def assertVal(val, functions, sub = {}):
	if isinstance(val, list):
		return evalExpr(val, functions, sub)
	else:
		if isinstance(val, dict):
			return executeCall(val, functions)
		elif not isNum(val):
			for name, num in sub.items():
				if name == val:
					return num
			else:
				error("Variable " + val + " not defined")
		else:
			return val

def executeCall(call, functions, sub = {}):
	# get the name & params...
	name = call['name']
	params = call['params']
	
	# if the name doesn't exist, error
	if name not in functions:
		success, ret = callpredef(name, params)
		if not success:
			error("Method " + str(name) + " not found")
		else:
			return ret
	
	# now we flatten parameters...
	if isinstance(params, str):
		params = [params]
	if not all(params):
		params = []
	params = flattenParams(params, functions, sub)
	
	# get the function out of the global function list
	func = functions.get(name)

	# get the function tags
	tags = func['tags']
	
	# get the substitute variable parameters
	param_temp = params
	for param, ptags in func['params'].items():
		if 'in' in ptags['tags']:
			try:
				sub[param] = float(input())
			except ValueError:
				sub[param] = param_temp.pop(-1)
		else:
			sub[param] = param_temp.pop(-1)
	
	val = evalExpr(func['expr'][0], functions, sub)
	if 'out' in tags:
		print(val, end='')
	
	return val

# takes a nested list of parameters
# returning the recursively evaluated value equivalent
def flattenParams(params, functions, sub):
	flattened = []
	
	# for every parameter
	for param in params:
		# if it's a dictionary ( a method call), call it
		if isinstance(param, dict):
			flattened.append(float(executeCall(param, functions)))
		# otherwise, if it's a normal param
		elif isinstance(param, str):
			# assert it's a value
			if not isNum(param):
				# search for inner methods
				inner = getInnerBlocks("(" + param + ")", '(', ')')
				# check for if it's an expression
				if re.search(r"\[.*\]", param):
					param = evalExpr(param, functions, sub)
				# check if it's a call
				elif isinstance(param, dict):
					param = executeCall(param, functions, sub)
				elif inner and len(inner) != 0:
					nparams = flattenParams(inner, functions, sub)
					return nparams
				elif param in sub.keys():
					param = sub.get(param)
				else:
					error("Raw parameter " + param + " not numerical or a valid expression!")
			# append its value
			flattened.append(float(param))
		else:
			error("Invalid parameter " + param)
			
	return flattened

# evaluates a single []-enclosed expression
def evalExpr(expression, functions, sub = {}):
	if isinstance(expression, str):
		expression = stripExpr(expression, functions, sub)[0][0]
	# if it's got one value inside...
	if len(expression) == 1:
		# return it
		return assertVal(expression[0], functions, sub)
	# check if it's a simple 3-value'd operation
	elif len(expression) == 3:
		lambda_oper = isGetOper(expression[0])
		# if it is...
		if lambda_oper:
			# get the other two values
			lvalue = expression[1]
			rvalue = expression[2]
			# assert neither value is an expression
			lvalue = assertVal(lvalue, functions, sub)
			rvalue = assertVal(rvalue, functions, sub)
			
			# return the value of the lambda
			return lambda_oper(float(lvalue), float(rvalue))
		# is it a conditional..?
		lambda_oper = isGetCond(expression[0])
		
		if lambda_oper:
			# get the two other values
			lvalue = expression[1]
			rvalue = expression[2]
			
			# assert neither value is an expression
			lvalue = assertVal(lvalue, functions, sub)
			rvalue = assertVal(rvalue, functions, sub)
				
			# return the lambda value
			return lambda_oper(float(lvalue), float(rvalue))
			
		# is it an if-statement..?
		if isIf(expression[0]):
			# get the two other values
			lvalue = expression[1]
			rvalue = expression[2]
			
			# assert the lvalue isn't an expression
			lvalue = assertVal(lvalue, functions, sub)
			
			# get the two rvalues
			try:
				rvalue_t, rvalue_f = tuple(rvalue)
			except ValueError:
				error("Conditional result has too many operands!")
			
			# assert the t/f values aren't expressions
			if lvalue:
				rvalue = assertVal(rvalue_t, functions, sub)
			else:
				rvalue = assertVal(rvalue_f, functions, sub)
			
			# return the correct value
			return rvalue
	else:
		error("Invalid expr \"" + str(expression) + '".')

##############################################################
def stripExpr(method, functions = [], sub = {}):
	def cleanStrList(l):
		return list(filter(lambda x : x, l))
	
	# should only execute once, just to remove initial curly braces
	for i in ['{','}']:
		method = method.replace(i,'')
	
	def getInner(method):
		if not re.search(r"\[.*\]", method):
			return method
		
		# get contents of the top-most layer of elements
		inner = []
		depth = 0
		callDepth = 0
		currentstring = ""
		for char in method:
			
			if char == '^':
				callDepth += 1
			
			if callDepth != 0:
				currentstring += str(char)
				if char == '$':
					callDepth -= 1
				continue
			
			if char == ']':
				depth -= 1
				
			if depth != 0:
				currentstring += str(char)
				
			if char == '[':
				depth += 1
			
			if depth == 0:
				inner.append(currentstring)
				currentstring = ""
				continue
		
		return cleanStrList(inner)
	
	def splitExpr(inner):
		# split items up at whitespace at depth 0
		expr = []
		for item in inner:
			depth = 0
			currentstring = ""
			currentlist = []
			callDepth = 0
			for char in item:
				if char == '^':
					callDepth += 1
				if callDepth != 0:
					currentstring += str(char)
					if char == '$':
						callDepth -= 1
					continue
				
				# if at depth 0, read characters, splitting at whitespace
					# when depth increased, begin reading all characters until depth is 0
				if char == ']':
					depth -= 1
				
				if depth > 0:
					currentstring += str(char)
				else:
					if re.match(r"\s", str(char)):
						currentlist.append(currentstring)
						currentstring = ""
					else:
						currentstring += str(char)
				
				if char == '[':
					depth += 1
			currentlist.append(currentstring)
			currentlist = cleanStrList(currentlist)
			
			expr.append(currentlist)
		return expr
	
	expr = splitExpr(getInner(method))
	# look, ok, i spent like,
	# four hours on these next two methods??
	# trying random things till it worked??
	# and it works, so please
	# never touch these ever again
	# thank you and goodnight
	def iterate(item):
		nitem = []
		for char in item:
			nchar = ""
			if isinstance(char, str):
				if re.search(r"\[.*\]", char) and not re.search(r"^\^.*\$$", char):
					nchar = splitExpr(getInner(char))
					nitem.extend(nchar)
				else:
					nchar = char
					nitem.append(nchar)
		return nitem
	
	def unflatten(exp):
		first_pass = []
		for item in exp:
			if isinstance(item, str) or isinstance(item, dict):
				first_pass.append(item)
			else:
				first_pass.append(unflatten(iterate(item)))
		
		return first_pass
		
	# turns regex-enclosed method calls into call dictionary objects
	def getCalls(arr):
		narr = []
		for i in arr:
			if isinstance(i, str):
				search_method = re.search(r"^\s*\^\s*(\w+?)\s*\((.*)\)\s*\$$", i)
				search_expr = re.search(r"(.*)(\[.*\])(.*)", i)
				if search_expr:
					params = evalExpr(search_expr.group(2), functions, sub)
					elem = search_expr.group(1) + str(params) + search_expr.group(3)
					narr.append(getCalls([elem]))
				elif search_method:
					params = search_method.group(2)
					paramstr = getInnerBlocks("("+params+")", '(', ')')[0]['params']
					elem = {
						'name': search_method.group(1),
						'params': paramstr
					}
					narr.append(elem)
				else:
					narr.append(i)
			elif isinstance(i, list):
				narr.append(getCalls(i))
		return narr
				
	return getCalls(unflatten(expr)), ""
	
# returns a list of calls, in order
def getCalls(code):
	calls = []
	
	# iterate over every char
	depth = 0
	cstr = ""
	
	# this loop logs parenthesis depth, and slices at every
	# return to 0 depth
	for char in code:
		# append the character
		cstr += str(char)
		if char == ')':
			depth -= 1
			if depth == 0 and cstr:
				calls.append(cstr)
				cstr = ""
		
		if char == '(':
			depth += 1
	
	def factorCalls(calls):
		factored = []
		
		if isinstance(calls, str):
			search = re.search(r"^.*\(.*\)$", calls)
			if search:
				return factorCalls([calls])[0]
			return calls
		
		# for every call
		for call in calls:
			factored_call = {}
			#                    name      params
			name = re.search(r"\s*(.*?)\s*\((.*)\)", call)
			if name:
				factored_call['name'] = name.group(1)
				factored_call['params'] = [factorCalls(i) for i in stripParams(name.group(2).strip())]
				factored.append(factored_call)
			else:
				error("Invalid call: " + call)
		
		return factored
	
	def stripParams(params):
		stripped = []
		
		# split at ',', but only at top-most paren depth
		# ...boilerplate much?
		depth = 0
		cstr = ""
		get = []
		for char in params:
			if char == '(':
				depth += 1
			if char == ')':
				depth -= 1
			if char == ',' and depth == 0:
				get.append(cstr)
				cstr = ""
			else:
				cstr += str(char)
		get.append(cstr)
		
		get = [i.strip() for i in get]
		
		if all(get):
			stripped.extend(get)
		
		return stripped
		
	return factorCalls(calls)