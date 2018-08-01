
# import modules
import sys
import os

def print_help():
	print('''
Required args:
 -c	commands file
 -m	memory (in Gb)
 -w	walltime (in hours)

Optional args:
 -J	job name, default = 'job'
 -p	# of processors
 -nc    # of commands to submit in a single PBS file, default = 1
	  Input 'all' to include all commands in a single PBS
 -e	load environment line
 -s	submit PBS files? y/n, default = y
''')

def parse_args(argv_l):
	PRC = 1
	NC = 1
	JOB_NM = 'job'
	ENV = ''
	SUB = True
	for i in range(0,len(argv_l)):
		if argv_l[i] == "-c":
			CMD = argv_l[i+1]
		elif argv_l[i] == "-J":
			JOB_NM = argv_l[i+1]
		elif argv_l[i] == "-m":
			MEM = argv_l[i+1]
		elif argv_l[i] == "-w":
			HR = argv_l[i+1]
		elif argv_l[i] == "-p":
			PRC = argv_l[i+1]
		elif argv_l[i] == "-e":
			ENV = argv_l[i+1]
		elif argv_l[i] == "-nc":
			NC = argv_l[i+1]
		elif argv_l[i] == "-s":
			arg = argv_l[i+1].lower()
			if arg == "n" or arg == "no":
				SUB = False
			elif arg == "y" or arg == "yes":
				SUB = True
			else:
				print("WARNING! Submit PBS argument not recognized.\n         PBS files will be submitted.")
		elif argv_l[i].startswith("-"):
			print("WARNING! Unrecognized flag ignored:",argv_l[i])
	return CMD, JOB_NM, MEM, HR, PRC, ENV, NC, SUB

def header_template():
	header ='''
#PBS -A junzli_flux
#PBS -N %s_%s
#PBS -q flux
#PBS -j oe
#PBS -V
#PBS -l nodes=1:ppn=%s,pmem=%sgb
#PBS -l walltime=%s:00:00
#PBS -l qos=flux
'''
	return(header)

def write_pbs(CMD, NC, JOB_NM, MEM, HR, PRC, ENV, SUB):
	blank_header = header_template()
	
	cmd_l = []
	inp = open(CMD)
	for line in inp:
		if not line.strip() == '':
			cmd_l.append(line)
	inp.close()
	
	if str(NC).lower() == 'all' or str(NC).lower() == "a":
		break_ind = [0]
	else:
		break_ind = range(0, len(cmd_l), int(NC))
	
	job_i = 1
	cmd_i = 0
	pbs_nms = []
	for cmd in cmd_l:
		if cmd_i in break_ind:
			if job_i > 1:
				out.close()
			
			pbs_nm = "%s_%s.pbs"%(JOB_NM, job_i)
			pbs_nms.append(pbs_nm)
			
			out = open(pbs_nm, "w")
			PBS_hdr = blank_header%(JOB_NM, job_i, PRC, MEM, HR)
			out.write(PBS_hdr)
		
			if ENV != '':
				out.write(ENV+"\n")
			
			job_i += 1

		out.write(cmd)
		
		cmd_i += 1			
	
	out.close()

	if SUB == True:
		for pbs_nm in pbs_nms:
			os.system("qsub %s"%pbs_nm)

def main():
	
	if len(sys.argv) == 1:
		print_help()
		sys.exit()
	
	CMD, JOB_NM, MEM, HR, PRC, ENV, NC, SUB = parse_args(sys.argv)
	write_pbs(CMD, NC, JOB_NM, MEM, HR, PRC, ENV, SUB)

	

if __name__ == "__main__":
	main()

