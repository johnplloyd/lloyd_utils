import os,sys

def print_help():
	print'''
Input file, -i

Functions, -f:
	rm_dup		Remove duplicate lines
	rm_char		Remove all instances of a character from the file, 
			include an -n flag to only remove character in that
			column
				req: -str; opt: -n,-sep,-com
				UNIX: sed s unless looking in a specific column
	upper		Produce file with all uppercase characters, include
			an -n flag to only make uppercase characters in that 
			column
				opt: -n,-sep,-com
	lower		Produce file with all lowercase characters, include
			an -n flag to only make lowercase characters in that 
			column
				opt: -n,-sep,-com
	split_line	Split every line on a character string, include
			an -n flag to only keep that column in the output
				req: -str; opt: -n,-sep,-com
				UNIX: cut with -d option unless string is >1
				character
	random		Produce a file of n randomly selected lines
				req: -n
	col_elements	Print a non-redundant list of elements in a column
				req: -n; opt: -sep, -com
	count_elements	Print non-redundant elements and the number of times 
			they appear in a column
				req: -n; opt: -sep,-com
	prefix		Add a prefix to every line in a file. Include an -n 
			flag to only suffix that column
				req: -str; opt: -n,-sep,-com
	suffix		Add a suffix to every line in a file. Include an -n 
			flag to only suffix that column
				req: -str; opt: -n,-sep,-com
	reverse		Reverse the order of lines in a file
	clear_spaces	Clean out inconsistent space delimitation. Returns
			tab-delimited.
	max_val		Print lines with a value less than a threshold (-flt).
			Script will assume column 1 (0-index). Include an -n 
			flag to adjust this.
				req: -flt; opt: -n,-sep,-com
	min_val		Print lines with a value greater than a threshold 
			(-flt). Script will assume column 1 (0-index). Include
			an -n flag to adjust this.
				req: -flt; opt: -n,-sep,-com
	keep_line	Keep lines based on a character string or list, include
			an -n flag to only look in that column (0 index)
				req: -str or -list; opt: -n,-sep,-com
				UNIX: grep if not looking in a specific column
	rm_line		Remove lines based on a character string or list 
			input, include an -n flag to only look in that 
			column (0 index)
				req: -str or -list; opt: -n,-sep,-com
				UNIX: grep with -v option if not looking in a 
				specific column
	find_replace	Find character string (-str) and replace (-rpl),
			include an -n flag to only look in that column (0 index)
				req: -str,-rpl; opt: -n,-sep
				UNIX: sed s if not looking in a specific column
	rm_column	Remove a column of data
				req: -n; opt: -sep
				UNIX: cut with --complement
	get_column	Retrieve data from column n (0 base), inclusion
			of -rid flag will return a two-column file with
			identifiers from column 0
				req: -n; opt: -desc,-sep,-rid
				UNIX: cut

Other flags:
	-n	Integer
	-flt	Float value
	-str	Character string
	-rpl	Replace string
	-desc	Description
	-com	Comment character (default = #)
	-rid	Rows have an identifier in the first column
	-sep	Column separator character (default = tab, \"space\" is valid)
	-list	Input to turn into a list
'''

def convert_sep(separator):
	if separator == "space":
		separator = " "
	elif separator == "tab":
		separator = "\t"
	return separator

def float_list(list):
	float_list = []
	express_error = True
	for item in list:
		float_item = None
		try:
			float_item = float(item)
		except:
			if express_error == True:
				print "List contains values that will not float! Ignoring..."
				express_error = False
		if float_item != None:
			float_list.append(float_item)
	return float_list

def string_list(list,col_sep):
	str_list = []
	for item in list:
		str_list.append(str(item))
	list_str = col_sep.join(str_list)
	return list_str

def clean_spaces(string):
	while "  " in string:
		string = string.replace("  "," ")
	return string

def inp2list(input_file):
	list = []
	try:
		inp = open(input_file)
	except:
		print "Cannot open -list input!"
		sys.exit()
	for line in inp:
		item = line.strip()
		if item != "":
			list.append(item)
	inp.close()
	return list

def set_string_status(item):
	if isinstance(item,set):
		set_or_string = "set"
	elif isinstance(item,str):
		set_or_string = "str"
	else:
		print "Remove/keep item is neither a list nor a string!"
		sys.exit()
	return set_or_string

# def process_rm_item(rm_item,item_to_check,outfile,out_line):
def process_rm_item(rm_item,item_to_check,out_line):
	set_or_string = set_string_status(rm_item)
	if set_or_string == "str":
		if rm_item not in item_to_check:
			print out_line.strip()
			# outfile.write(out_line)
	elif set_or_string == "set":
		proceed = True
		for rm in rm_item:
			if rm in item_to_check:
				proceed = False
				break
		if proceed == True:
			print out_line.strip()
			# outfile.write(out_line)

# def process_keep_item(keep_item,item_to_check,outfile,out_line):
def process_keep_item(keep_item,item_to_check,out_line):
	set_or_string = set_string_status(keep_item)
	if set_or_string == "str":
		if keep_item in item_to_check:
			print out_line
	elif set_or_string == "set":
		for keep in keep_item:
			if keep in item_to_check:
				print out_line
				# outfile.write(out_line)
				break

def function_random(input_file,comment_char,n):
	import random
	inp = open(input_file)
	out = open(input_file + ".random_" + str(n),"w")
	
	list = []
	for line in inp:
		if line.startswith(comment_char):
			out.write(line)
		else:
			list.append(line)
	
	if len(list) < n:
		print "  WARNING: File length shorter than n, keeping all lines"
		random_list = list[:]
	else:
		random_list = random.sample(list,n)
	
	for line in random_list:
		out.write(line)
	
	inp.close()
	out.close()

def function_reverse(input_file,comment_char):
	inp = open(input_file)
	out = open(input_file + ".reverse","w")
	
	list = []
	i = 0
	for line in inp:
		if line.startswith(comment_char):
			out.write(line)
		else:
			list.append([line,i])
			i += 1
	
	list.sort(key=lambda k: (k[-1]),reverse=True)
	
	for line in list:
		out.write(line[0])
	
	inp.close()
	out.close()

# def function_keep_line(input_file,comment_char,char_str,n,col_sep):
def function_keep_line(input_file,comment_char,keep_item,n,col_sep):
	inp = open(input_file)
	# out = open(input_file + ".keep","w")
	#process_keep_item(keep_item,item_to_check,outfile,out_line)
	for line in inp:
		line = line.strip()
		if line.startswith(comment_char):
			print line
			# out.write(line)
		# elif char_str in line:
		else:	
			if n == None:
				# process_keep_item(keep_item,line,out,line)
				process_keep_item(keep_item,line,line)
				# out.write(line)
			else:
				lineLst = line.strip().split(col_sep)
				# process_keep_item(keep_item,lineLst[n],out,line)
				process_keep_item(keep_item,lineLst[n],line)
				# if char_str in lineLst[n]:
					# out.write(line)
	
	inp.close()
	# out.close()

def function_rm_line(input_file,comment_char,rm_item,n,col_sep):
	inp = open(input_file)
	# out = open(input_file + ".rem","w")
	
	for line in inp:
		if line.startswith(comment_char):
			print line.strip()
			# out.write(line)
		else:
			if n == None:
				# process_rm_item(rm_item,line,out,line)			
				process_rm_item(rm_item,line,line)			
			else:
				lineLst = line.strip().split(col_sep)
				# process_rm_item(rm_item,lineLst[n],out,line)
				process_rm_item(rm_item,lineLst[n],line)
	
	inp.close()
	# out.close()

def function_find_replace(input_file,col_sep,char_str,replace_str):
	inp = open(input_file)
	out = open(input_file + ".fr","w")
	
	for line in inp:
		if n == None:
			if char_str in line:
				line = line.replace(char_str,replace_str)
			out.write(line)
		else:
			lineLst = line.strip().split(col_sep)
			if char_str in lineLst[n]:
				lineLst[n] = lineLst[n].replace(char_str,replace_str)
				line = col_sep.join(lineLst) + "\n"
			out.write(line)
	
	inp.close()
	out.close()

def function_clear_spaces(input_file):
	inp = open(input_file)
	out = open(input_file + ".clean","w")
	
	for line in inp:
		clean_line = clean_spaces(line).replace(" ","\t")
		out.write(clean_line)
	
	inp.close()
	out.close()

def function_get_col(input_file,comment_char,index,description,col_sep,row_ids):
	inp = open(input_file)
	out = open(input_file + ".col" + str(n),"w")
	if description != None:
		out.write("#"+description+"\n")
	
	for line in inp:
		if not line.startswith(comment_char):
			lineLst = line.strip().split(col_sep)
			data = lineLst[index]
			if row_ids == True:
				id = lineLst[0]
				out.write("%s\t%s\n" % (id,data))
			else:
				out.write(data + "\n")
	
	inp.close()
	out.close()

def function_rm_col(input_file,index,col_sep):
	inp = open(input_file)
	out = open(input_file + ".rm_col" + str(n),"w")
	
	for line in inp:
		lineLst = line.strip().split(col_sep)
		lineLst.pop(index)
		out_str = col_sep.join(lineLst)
		out.write(out_str + "\n")
	
	inp.close()
	out.close()

def function_rm_dup(input_file,comment_char):
	inp = open(input_file)
	st = set()
	for line in inp:
		if line.startswith(comment_char):
			print line.strip()
		else:
			st.add(line)
	inp.close()
	
	if st != set():
		for line in st:
			print line.strip()
	else:
		print "No duplicates present!"

def function_split_line(input_file,index,col_sep,char_str,comment_char):
	inp = open(input_file)
	out = open(input_file+".split","w")
	for line in inp:
		if line.startswith(comment_char):
			out.write(line)
		else:
			line_split = line.split(char_str)
			if index == None:
				out.write(col_sep.join(line_split))
			else:
				out.write(line_split[index].strip()+"\n")
	inp.close()
	out.close()

def function_upper(input_file,index,col_sep,comment_char):
	inp = open(input_file)
	out = open(input_file+".upper","w")
	for line in inp:
		if line.startswith(comment_char):
			out.write(line)
		else:
			if index == None:
				out.write(line.upper())
			else:
				lineLst = line.strip().split(col_sep)
				lineLst[index] = lineLst[index].upper()
				out.write(col_sep.join(lineLst)+"\n")
	inp.close()
	out.close()

def function_lower(input_file,index,col_sep,comment_char):
	inp = open(input_file)
	out = open(input_file+".lower","w")
	for line in inp:
		if line.startswith(comment_char):
			out.write(line)
		else:
			if index == None:
				out.write(line.lower())
			else:
				lineLst = line.strip().split(col_sep)
				lineLst[index] = lineLst[index].lower()
				out.write(col_sep.join(lineLst)+"\n")
	inp.close()
	out.close()

def function_rmChar(input_file,rmChar,index,col_sep,comment_char):
	inp = open(input_file)
	# out = open(input_file+".rmChar","w")
	for line in inp:
		if line.startswith(comment_char):
			# out.write(line)
			print(line.strip())
		else:
			if index == None:
				# out.write(line.lower())
				print line.strip().replace(rmChar,"")
			else:
				lineLst = line.strip().split(col_sep)
				lineLst[index] = lineLst[index].replace(rmChar,"")
				# out.write(col_sep.join(lineLst)+"\n")
				print col_sep.join(lineLst)
	inp.close()
	# out.close()

def function_colEle(input_file,index,col_sep,comment_char):
	inp = open(input_file)
	col_set = set()
	for line in inp:
		if line.startswith(comment_char):
			pass
		else:
			lineLst = line.strip().split(col_sep)
			col_set.add(lineLst[index])
	inp.close()
	for item in col_set:
		print item

def function_cntEle(input_file,n,col_sep,comment_char):
	inp = open(input_file)
	ele_dict = {}
	for line in inp:
		if line.startswith(comment_char):
			pass
		else:
			lineLst = line.strip().split(col_sep)
			element = lineLst[n]
			if element not in ele_dict:
				ele_dict[element] = 1
			else:
				ele_dict[element] += 1
	inp.close()
	for ele in ele_dict:
		cnt = str(ele_dict[ele])
		print "%s\t%s"%(ele,cnt)

def function_prefix(input_file,n,char_str,col_sep,comment_char):
	inp = open(input_file)
	for line in inp:
		if line.startswith(comment_char):
			print line.strip()
		else:
			if n == None:
				print char_str+line.strip()
			else:
				lineLst = line.strip().split(col_sep)
				out_item = char_str+lineLst[n].strip()
				lineLst[n] = out_item
				print col_sep.join(lineLst)
	inp.close()

def function_suffix(input_file,n,char_str,col_sep,comment_char):
	inp = open(input_file)
	for line in inp:
		if line.startswith(comment_char):
			print line.strip()
		else:
			if n == None:
				print line.strip()+char_str
			else:
				lineLst = line.strip().split(col_sep)
				out_item = lineLst[n].strip()+char_str
				lineLst[n] = out_item
				print col_sep.join(lineLst)
	inp.close()

def function_maxVal(input_file,flt_val,n,col_sep,comment_char):
	if n == None:
		ind = 1
	else:
		ind = n
	inp = open(input_file)
	for line in inp:
		if line.startswith(comment_char):
			print line.strip()
		else:
			lineLst = line.strip().split(col_sep)
			line_val = float(lineLst[ind])
			if line_val <= flt_val:
				print line.strip()
	inp.close()

def function_minVal(input_file,flt_val,n,col_sep,comment_char):
	if n == None:
		ind = 1
	else:
		ind = n
	inp = open(input_file)
	for line in inp:
		if line.startswith(comment_char):
			print line.strip()
		else:
			lineLst = line.strip().split(col_sep)
			line_val = float(lineLst[ind])
			if line_val >= flt_val:
				print line.strip()
	inp.close()

### SET DEFAULTS
function = input_file = n = char_str = float_val = None
input_list = description = replace_str = None
comment_char = "#"
col_sep = "\t"
row_ids = False


### PARSE ARGUMENTS
i = 0
for arg in sys.argv:
	if arg == "-f":
		try:
			function = sys.argv[i+1]
		except:
			pass
	elif arg == "-i":
		try:
			input_file = sys.argv[i+1]
		except:
			pass
	elif arg == "-n":
		n = int(sys.argv[i+1])
	elif arg == "-com":
		comment_char = sys.argv[i+1]
	elif arg == "-rid":
		row_ids = True
	elif arg == "-sep":
		col_sep = convert_sep(sys.argv[i+1])
	elif arg == "-str":
		char_str = sys.argv[i+1]
	elif arg == "-desc":
		description = sys.argv[i+1]
	elif arg == "-rpl":
		replace_str = sys.argv[i+1]
	elif arg == "-list":
		input_list = inp2list(sys.argv[i+1])
	elif arg == "-flt":
		float_val = float(sys.argv[i+1])
	i+=1

if function == None or input_file == None:
	print_help()
	print "Function (-f) and input file (-i) required!"
	sys.exit()
elif function == "random":
	if n == None:
		print_help()
		print "Integer (-n) required!"
		sys.exit()
	else:
		function_random(input_file,comment_char,n)
		sys.exit()
elif function == "reverse":
	function_reverse(input_file,comment_char)
	sys.exit()
elif function == "keep_line":
	if char_str == None and input_list == None:
		print_help()
		print "Character string (-str) required!"
		sys.exit()
	else:
		# function_keep_line(input_file,comment_char,char_str,n,col_sep)
		if char_str != None:
			function_keep_line(input_file,comment_char,char_str,n,col_sep)
		elif input_list != None:
			input_set = set(input_list)
			function_keep_line(input_file,comment_char,input_set,n,col_sep)
		sys.exit()
elif function == "rm_line":
	if char_str == None and input_list == None:
		print_help()
		print "Character string (-str) or input list (-list) required!"
		sys.exit()
	else:
		if char_str != None and input_list != None:
			print "Input either string (-str) or list (-list), not both!"
			sys.exit()
		elif char_str != None:
			function_rm_line(input_file,comment_char,char_str,n,col_sep)
		elif input_list != None:
			input_set = set(input_list)
			function_rm_line(input_file,comment_char,input_set,n,col_sep)
		sys.exit()
elif function == "clear_spaces":
	function_clear_spaces(input_file)
	sys.exit()
elif function == "get_column":
	if n == None:
		print_help()
		print "Integer (-n) required!"
		sys.exit()
	else:
		function_get_col(input_file,comment_char,n,description,col_sep,row_ids)
		sys.exit()
elif function == "rm_column":
	if n == None:
		print_help()
		print "Integer (-n) required!"
		sys.exit()
	else:
		function_rm_col(input_file,n,col_sep)
		sys.exit()
elif function == "find_replace":
	if char_str == None or replace_str == None:
		print_help()
		print "Find string (-str) and replace string (-rpl) required!"
		sys.exit()
	else:
		function_find_replace(input_file,col_sep,char_str,replace_str)
		sys.exit()
elif function == "rm_dup":
	function_rm_dup(input_file,comment_char)
	sys.exit()
elif function == "split_line":
	if char_str == None:
		print_help()
		print "Spliting string (-str) required!"
		sys.exit()
	function_split_line(input_file,n,col_sep,char_str,comment_char)
	sys.exit()
elif function == "upper":
	function_upper(input_file,n,col_sep,comment_char)
	sys.exit()
elif function == "lower":
	function_lower(input_file,n,col_sep,comment_char)
	sys.exit()
elif function == "rm_char":
	function_rmChar(input_file,char_str,n,col_sep,comment_char)
	sys.exit()
elif function == "col_elements":
	if n == None:
		print_help()
		print "Column index (-n) required!"
	else:
		function_colEle(input_file,n,col_sep,comment_char)
	sys.exit()
elif function == "count_elements":
	if n == None:
		print_help()
		print "Column index (-n) required!"
	else:
		function_cntEle(input_file,n,col_sep,comment_char)
	sys.exit()
elif function == "prefix":
	if char_str == None:
		print_help()
		print "Character string (-str) required!"
	else:
		function_prefix(input_file,n,char_str,col_sep,comment_char)
elif function == "suffix":
	if char_str == None:
		print_help()
		print "Character string (-str) required!"
	else:
		function_suffix(input_file,n,char_str,col_sep,comment_char)
elif function == "max_val":
	if float_val == None:
		print_help()
		print "Float value (-flt) required!"
	else:
		function_maxVal(input_file,float_val,n,col_sep,comment_char)
elif function == "min_val":
	if float_val == None:
		print_help()
		print "Float value (-flt) required!"
	else:
		function_minVal(input_file,float_val,n,col_sep,comment_char)
else:
	print_help()
	print "Function not recognized!"
	sys.exit()
