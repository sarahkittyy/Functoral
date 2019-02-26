import re
import os
from ast import literal_eval

def error(msg, code=-1):
	print("Error: " + str(msg))
	exit(-1)
	
def callpredef(name, params):
	if name == 'print':
		for param in params:
			# substitue in special chars
			param = literal_eval('"' + param + '"')
			# check for ending spaces
			param = re.sub(r"\\s", r" ", param)
			#print
			print(param, end='', flush=True)
			return True, 0
	return False, -1

def cleancode(code):
	clean_code = code
	
	# strip comments
	clean_code = list(map(lambda line : re.sub(r"(.*)!!.*", r"\1", line), clean_code))
	
	# remove beginning & ending whitespace
	clean_code = list(map(lambda line : re.sub(r"^\s*(.*?)\s*$", r"\1", line), clean_code))
		
	# strip empty lines.
	clean_code = list(filter(lambda line : len(line)!=0, clean_code))
	
	return '\n'.join(clean_code)

def isNum(num):
	try:
		float(num)
	except ValueError:
		return False
	return True

# returns a lambda if string parameter is a valid oper (+, -, *, /)
# returns none otherwise
def isGetOper(oper):
	if oper == '+':
		return lambda x, y: x + y
	elif oper == '-':
		return lambda x, y: x - y
	elif oper == '*':
		return lambda x, y: x * y
	elif oper == '/':
		return lambda x, y: x / y
	elif oper == '&':
		return lambda x, y: x
	return None
	
# returns a lambda if string parameter is a valid conditional operator
def isGetCond(oper):
	if oper == '==':
		return lambda x, y: x == y
	elif oper == '<':
		return lambda x, y: x < y
	elif oper == '>':
		return lambda x, y: x > y
	elif oper == '>=':
		return lambda x, y: x >= y
	elif oper == '<=':
		return lambda x, y: x <= y
	elif oper == '!=':
		return lambda x, y: x != y
	else:
		return None

# returns true if the operator is conditioanl
def isIf(oper):
	if oper is '?':
		return True
	return False

# if an expression looks like this:
# ....(stuff ( more stuff (etc. ) ) etc....)
# this method returns a list of contained outermost enclosures
def getInnerBlocks(string, begin, end, sep = [","]):
	ret_list = []
	if not isinstance(string, str):
		return None
	
	# read a name until depth 1. Store until depth 0, and append it along with
	# the contents.
	# at depth 0, ignore separators
	
	cname = ""
	depth = 0
	last_name = ""
	cstr = ""
	clist = []
	for char in string:
		if char == end:
			depth -= 1
			if depth == 0:
				clist.append(cstr)
				ret_list.append({
					'name': last_name,
					'params': clist
				})
				clist = []
				cstr = ""
				
		if depth == 0:
			if char not in sep and char not in [begin, end]:
				cname += str(char)
		elif depth == 1:
			if char in sep:
				clist.append(cstr)
				cstr = ""
			else:
				cstr += str(char)
		elif depth == 2:
			cstr += str(char)
			
		if char == begin:
			depth += 1
			if depth == 1:
				last_name = cname
				cname = ""
	ret = [] 
	for item in ret_list:
		name = item['name'].strip()
		params = []
		for i in item['params']:
			cstr = i.strip()
			inner = getInnerBlocks(cstr, begin, end, sep)
			if inner and len(inner) != 0:
				params.extend(inner)
			else:
				params.append(i.strip())
		ret.append({
			'name': name,
			'params': params
		})
	return ret