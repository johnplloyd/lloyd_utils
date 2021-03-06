
def get_file_length(fl):
	flen = 0
	inp = open(fl)
	for line in inp:
		flen +=1
	inp.close()
	return flen

def split_file(fl,lis):
	ln_cnt = 0
	sec_cnt = 1
	inp = open(fl)
	out = open("%s.%s_split"%(fl,sec_cnt),"w")
	for line in inp:
		ln_cnt += 1
		if ln_cnt <= lis:
			out.write(line)
		else:
			out.close()
			sec_cnt += 1
			out = open("%s.%s_split"%(fl,sec_cnt),"w")
			out.write(line)
			ln_cnt = 1
	out.close()
	inp.close()
	print(sec_cnt,"split files generated")

def main():
	import sys
	if len(sys.argv)==1:
		print('''
inp1 = file to split
inp2 = number of sections
''')
		sys.exit()
	file = sys.argv[1]
	sections = float(sys.argv[2])
	file_len = get_file_length(file)
	import math
	lines_in_split = math.ceil(file_len/sections)
	print(file_len,"lines in the original file")
	print(int(lines_in_split),"lines in the split files")
	print(sections,"split files should be generated")
	split_file(file,lines_in_split)

if __name__ == "__main__":
	main()

