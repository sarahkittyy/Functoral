import re
from interpreter.util import error
import itertools
from interpreter.execute import execute
from interpreter.expr import stripExpr

def interpret(code):
	# strip & initialize defined functions
	code, functions = stripFunctions(code)
	
	# execute
	execute(code, functions)

def stripFunctions(code):		
	##################################################33
	def stripName(method):
		# compile the name-matching pattern
		name_pattern = re.compile(r"(\w*)\s*\(")
		
		# get the name
		name = str(re.search(name_pattern, method).group(1))
		
		# strip the name
		stripped_method = re.sub(r"(\w*)", "", method, 1)
		
		# return the name & stripped method
		return name, stripped_method
		
	###############################################
	
	def stripParams(method):
		params = {}
		
		# get the inside of the param parenthesis
		param_list_str = re.search(r"\((.*?)\)", method).group(1)
		
		# remove spaces
		param_list_str = param_list_str.replace(' ', '')
		
		# get comma-delimited list of params
		param_list = []
		if param_list_str:
			param_list = param_list_str.split(',')
			
		# for every param..
		for param_str in param_list:
			# strip tags
			tags, param_str = stripTags(param_str)
			# append params
			params[param_str] = { "tags": tags }
		
		# strip the method
		stripped_method = re.sub(r"\(.*?\)", "", method, 1)
		
		return params, stripped_method
		
	##########################################################

	def stripTags(method):
		# compile the tag-matching pattern
		tag_pattern = re.compile(r"(<.*?>)+\s*")
		
		# get a string representing all tags.
		tag_match = re.match(tag_pattern, method)
		
		# get a list of all tags
		tag_list = []
		if tag_match:
			tag_list = re.findall(r"<(.*?)>", tag_match.group(0))
			
		# remove leading & trailing whitespace
		tag_list = list(map(lambda x : re.sub(r"\s*(.*?)\s*",r"\1",x), tag_list))
		
		# get the stripped method -- only stripping method tags, not param tags
		method_ret = re.sub(tag_pattern, "", method, len(tag_list)-1)
		
		# return the tag matches & the stripped method
		return tag_list, method_ret
	
	##################################################
	code_stripped = code.replace('\n', ' ')
	functions = {}
	
	# get all methods
	method_matcher = re.compile(r"(<.*?>\s*)*\w*?\s*\(.*?\)\s*\{.*?\}")
	matches = re.finditer(method_matcher, code_stripped)
		
	# get all matching strings.
	methods = [str(m.group(0)) for m in matches]
	
	# for every method...
	for method in methods:
		# create a function object
		function = {}
		
		# grab all tags before the function name decl
		tagstr = re.sub(r"\s*(<.*>\s*)*\w*\(.*",r"\1", method)
		
		# get the tags
		tags, _ = stripTags(tagstr)
		# get the method name
		name, method = stripName(method)
		# get the params
		params, method = stripParams(method)
		# get the expression
		expr, method = stripExpr(method)
		
		# method is now an empty string, it's completely stripped
		if method:
			error("Invalid syntax.")
		
		# add the name to the function
		function['tags'] = tags
		function['params'] = params
		function['expr'] = expr
		
		# append the function
		functions[name] = function
	
	return re.sub(method_matcher, "", code_stripped), functions