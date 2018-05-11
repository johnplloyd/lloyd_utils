
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
 -nc    # of commands to submit in a single PBS file, default = 1
	  Input 'all' to include all commands in a single PBS
 -e	load environment line
''')

def parse_args(argv_l):
	NC = 1
	JOB_NM = 'job'
	ENV = ''
	for i in range(0,len(argv_l)):
		if argv_l[i] == "-c":
			CMD = argv_l[i+1]
		elif argv_l[i] == "-J":
			JOB_NM = argv_l[i+1]
		elif argv_l[i] == "-m":
			MEM = argv_l[i+1]
		elif argv_l[i] == "-w":
			HR = argv_l[i+1]
		elif argv_l[i] == "-e":
			ENV = argv_l[i+1]
		elif argv_l[i] == "-nc":
			NC = argv_l[i+1]
		elif argv_l[i].startswith("-"):
			print("WARNING! Unrecognized flag ignored:",argv_l[i])
	return CMD, JOB_NM, MEM, HR, ENV, NC

def header_template():
	header ='''
#PBS -A junzli_flux
#PBS -N %s_%s
#PBS -q flux
#PBS -j oe
#PBS -V
#PBS -l nodes=1:ppn=1,pmem=%sgb
#PBS -l walltime=%s:00:00
#PBS -l qos=flux
'''
	return(header)

def write_pbs(CMD, NC, JOB_NM, MEM, HR, ENV):
	blank_header = header_template()
	
	cmd_l = []
	inp = open(CMD)
	for line in inp:
		if not line.strip() == '':
			cmd_l.append(line)
	inp.close()
	
	if NC.lower() == 'all' or NC.lower() == "a":
		break_ind = [0]
	else:
		break_ind = range(0, len(cmd_l), int(NC))
	
	job_i = 1
	cmd_i = 0
	for cmd in cmd_l:
		if cmd_i in break_ind:
			if job_i > 1:
				out.close()
				os.system("qsub %s"%pbs_nm)
			
			pbs_nm = "%s_%s.pbs"%(JOB_NM, job_i)
			out = open(pbs_nm, "w")
			PBS_hdr = blank_header%(JOB_NM, job_i, MEM, HR)
			out.write(PBS_hdr)
		
			if ENV != '':
				out.write(ENV+"\n")
			
			job_i += 1

		out.write(cmd)
		
		cmd_i += 1			
	
	out.close()
	os.system("qsub %s"%pbs_nm)

def main():
	
	if len(sys.argv) == 1:
		print_help()
		sys.exit()
	
	CMD, JOB_NM, MEM, HR, ENV, NC = parse_args(sys.argv)
	
	write_pbs(CMD, NC, JOB_NM, MEM, HR, ENV)

	

if __name__ == "__main__":
	main()

