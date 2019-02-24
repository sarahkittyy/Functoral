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
			inner = getInnerBlocks(i.strip(), begin, end, sep)
			if inner and len(inner) != 0:
				params.extend(inner)
			else:
				params.append(i.strip())
		ret.append({
			'name': name,
			'params': params
		})
	return ret
print(getInnerBlocks('2,3', '(', ')'))