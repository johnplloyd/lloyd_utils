
#import modules
import sys
import fn

def print_help():
	print('''

arguments:
  -i  input file
  -l  index with labels (0-base)
  -s  index with scores (0-base)
  -p  positive class name, DEFAULT = yes
  -n  negative class name, DEFAULT = no
''')

def parse_args(argv_l):
	#set defaults
	pn = "yes"
	nn = "no"
	for i in range(0,len(argv_l)):
		if argv_l[i] == "-i":
			inf = argv_l[i+1]
		elif argv_l[i] == "-l":
			l = argv_l[i+1]
		elif argv_l[i] == "-s":
			s = argv_l[i+1]
		elif argv_l[i] == "-p":
			pn = argv_l[i+1]
		elif argv_l[i] == "-n":
			nn = argv_l[i+1]
		# elif argv_l[i].startswith("-"):
			# print "WARNING: Flag not recognized:",argv_l[i]
			# print "Quitting"
			# sys.exit()
	return inf,l,s,pn,nn

def make_label_and_score_lists(fl,li,si,pos,neg):
	ignore_list = ["NA","?",""]
	ll = []
	sl = []
	inp = open(fl)
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			lab_raw = lineLst[int(li)]
			scr = lineLst[int(si)]
			if scr not in ignore_list:
				if lab_raw == pos:
					# lab = 1
					ll.append(1)
					sl.append(float(scr))
				elif lab_raw == neg:
					ll.append(0)
					sl.append(float(scr))
				# elif lab_raw == "?":
					# pass
				else:
					# print "  LABEL NOT RECOGNIZED!:",lab_raw
					pass
	inp.close()
	return ll,sl

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		infile,lab_ind,scr_ind,pos_nm,neg_nm = parse_args(sys.argv)
	except:
		print_help()
		print("Error reading arguments, quitting!")
		sys.exit()
	
	label_lst,score_lst = make_label_and_score_lists(infile,lab_ind,scr_ind,pos_nm,neg_nm)
	aucroc = fn.calc_aucroc(label_lst,score_lst)
	dir = "+"
	if aucroc < 0.5:
		aucroc = 1-aucroc
		dir = "-"
	print("%s\t%s\t%s"%(infile,aucroc,dir))
	

if __name__ == "__main__":
	main()
