
#import modules
import sys
import fn
import numpy
import random
import math

def print_help():
	print('''
inp1 = scores files
inp2 = index with classes (0-base)
inp3 = index with scores (0-base)
inp4 = positive class name
inp5 = negative class name
inp6 = [optional] # of random samples to draw for balancing

NUMPY MODULE REQUIRED
''')

def pull_class_ids(fl,cls_i,pos_nm,neg_nm):
	pos_s = set()
	neg_s = set()
	inp = open(fl)
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			
			if typ == nm:
				s.add(id)
	inp.close()
	return s

# def pull_class_vals(fl,ids_s):
def pull_class_vals(fl,cls_i,val_i,pos_nm,neg_nm):
	ignore_list = ["NA","?",""]
	pos_l = []
	neg_l = []
	inp = open(fl)
	for line in inp:
		if not line.startswith("#"):
			lineLst = line.strip().split("\t")
			cls = lineLst[cls_i]
			val = lineLst[val_i]
			if val not in ignore_list:
				if cls == pos_nm:
					pos_l.append(float(val))
				elif cls == neg_nm:
					neg_l.append(float(val))
	inp.close()
	return pos_l,neg_l

def compare_median(pos_l,neg_l):
	med_pos = fn.median(pos_l)
	med_neg = fn.median(neg_l)
	print(med_pos,med_neg)
	if med_pos > med_neg:
		return "pos_high"
	elif med_pos < med_neg:
		return "pos_low"
	else:
		return "pos_equal"

def compare_average(pos_l,neg_l):
	ave_pos = sum(pos_l)/float(len(pos_l))
	ave_neg = sum(neg_l)/float(len(neg_l))
	print(ave_pos,ave_neg)
	if ave_pos > ave_neg:
		return "pos_high"
	elif ave_pos < ave_neg:
		return "pos_low"
	else:
		return "pos_equal"

def compare_percentile(pos_l,neg_l,prcntl):
	per_pos = numpy.percentile(pos_l,prcntl)
	per_neg = numpy.percentile(neg_l,prcntl)
	# ave_pos = sum(pos_l)/float(len(pos_l))
	# ave_neg = sum(neg_l)/float(len(neg_l))
	print(prcntl,per_pos,per_neg)
	if per_pos > per_neg:
		return "pos_high"
	elif per_pos < per_neg:
		return "pos_low"
	else:
		return "pos_equal"

def percent_nonzero(l):
	all = 0
	non0 = 0
	for item in l:
		all += 1
		if item != 0:
			non0 += 1
	per_non0 = float(non0)/all*100
	return per_non0

def compare_nonzero(pos_l,neg_l):
	# print neg_l
	pos_non0_per = percent_nonzero(pos_l)
	neg_non0_per = percent_nonzero(neg_l)
	print(pos_non0_per,neg_non0_per)
	if pos_non0_per > neg_non0_per:
		return "pos_high"
	elif pos_non0_per < neg_non0_per:
		return "pos_low"
	else:
		return "pos_equal"

def get_min_class_size(fl,cls_i):
	count_d = {}
	inp = open(fl)
	for line in inp:
		lineLst = line.strip().split("\t")
		class_nm = lineLst[cls_i]
		if class_nm not in count_d:
			count_d[class_nm] = 1
		else:
			count_d[class_nm] += 1
	inp.close()
	
	min_size = 1000000000
	for class_nm in count_d:
		class_cnt = count_d[class_nm]
		if class_cnt < min_size:
			min_size = class_cnt
	
	return min_size

def subsample_and_calc_error_rates(pos_l,neg_l,sub_cnt,cmp):
	thresh_s = set()
	for val in pos_l:
		thresh_s.add(val)
	for val in neg_l:
		thresh_s.add(val)
	
	out_l_fms = []
	out_l_kpa = []
	iter_cnt = 101
	for i in range(0,iter_cnt):
		# if i%10 == 0:
		print("  balanced set %s of %s"%(i+1,iter_cnt))
		ran_pos = random.sample(pos_l,sub_cnt)
		ran_neg = random.sample(neg_l,sub_cnt)
		
		max_fmeas = 0
		max_fmeas_fnr = ""
		max_fmeas_fpr = ""
		max_fmeas_thresh = ""
		
		max_kappa = 0
		max_kappa_fnr = ""
		max_kappa_fpr = ""
		max_kappa_thresh = ""
		
		for thresh in thresh_s:
			tp = 0
			fng = 0
			fp = 0
			tn = 0
			for val in ran_pos:
				if cmp == "pos_high":
					if val >= thresh:
						tp += 1
					else:
						fng += 1
				elif cmp == "pos_low":
					if val <= thresh:
						tp += 1
					else:
						fng += 1
			for val in ran_neg:
				if cmp == "pos_high":
					if val >= thresh:
						fp += 1
					else:
						tn += 1
				elif cmp == "pos_low":
					if val <= thresh:
						fp += 1
					else:
						tn += 1
			
			prc,rcl,fms = fn.calc_prec_rec_fm(tp,fng,fp,tn)
			if fms != "NC":
				if fms > max_fmeas:
					max_fmeas = fms
					max_fmeas_fnr = fn.calc_FNR(fng,tp)
					max_fmeas_fpr = fn.calc_FPR(fp,tn)
					max_fmeas_thresh = thresh
			
			kppa = fn.calc_kappa(tp,fng,fp,tn)
			abs_kppa = math.fabs(kppa)
			if abs_kppa > max_kappa:
				max_kappa = abs_kppa
				max_kappa_fnr = fn.calc_FNR(fng,tp)
				max_kappa_fpr = fn.calc_FPR(fp,tn)
				max_kappa_thresh = thresh
			
		out_l_fms.append([max_fmeas_thresh,max_fmeas,max_fmeas_fnr,max_fmeas_fpr])
		out_l_kpa.append([max_kappa_thresh,max_kappa,max_kappa_fnr,max_kappa_fpr])
	return out_l_fms,out_l_fms

def calc_error_rates(fl_nm,pos_l,neg_l,cmp):
	thresh_s = set()
	for val in pos_l:
		thresh_s.add(val)
	for val in neg_l:
		thresh_s.add(val)
	
	out_l_fms = []
	out_l_kpa = []
	# for i in range(0,500):
		# if i%50 == 0:
			# print "  balanced set %s"%(i)
	tp = 0
	fng = 0
	fp = 0
	tn = 0
	# ran_pos = random.sample(pos_l,sub_cnt)
	# ran_neg = random.sample(neg_l,sub_cnt)
	
	# max_fmeas = 0
	# max_fmeas_fnr = ""
	# max_fmeas_fpr = ""
	# max_fmeas_thresh = ""
	
	# max_kappa = 0
	# max_kappa_fnr = ""
	# max_kappa_fpr = ""
	# max_kappa_thresh = ""
	
	out = open(fl_nm+".error_rates","w")
	out.write("#thresh\tprc\trcl\tfmeas\tkappa\tFNR\tFPR\ttp\tfn\tfp\ttn\n")
	for thresh in thresh_s:
		tp = 0
		fng = 0
		fp = 0
		tn = 0
		for val in pos_l:
			if cmp == "pos_high":
				if val >= thresh:
					tp += 1
				else:
					fng += 1
			elif cmp == "pos_low":
				if val <= thresh:
					tp += 1
				else:
					fng += 1
		for val in neg_l:
			if cmp == "pos_high":
				if val >= thresh:
					fp += 1
				else:
					tn += 1
			elif cmp == "pos_low":
				if val <= thresh:
					fp += 1
				else:
					tn += 1
		
		prc,rcl,fms = fn.calc_prec_rec_fm(tp,fng,fp,tn)
		fnr = fn.calc_FNR(fng,tp)
		fpr = fn.calc_FPR(fp,tn)
		kppa = fn.calc_kappa(tp,fng,fp,tn)
		out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(thresh,prc,rcl,fms,kppa,fnr,fpr,tp,fng,fp,tn))
	out.close()
		# if fms != "NC":
			# if fms > max_fmeas:
				# max_fmeas = fms
				# max_fmeas_fnr = fn.calc_FNR(fng,tp)
				# max_fmeas_fpr = fn.calc_FPR(fp,tn)
				# max_fmeas_thresh = thresh
		
		# kppa = fn.calc_kappa(tp,fng,fp,tn)
		# abs_kppa = math.fabs(kppa)
		# if abs_kppa > max_kappa:
			# max_kappa = abs_kppa
			# max_kappa_fnr = fn.calc_FNR(fng,tp)
			# max_kappa_fpr = fn.calc_FPR(fp,tn)
			# max_kappa_thresh = thresh
		
	# out_l_fms.append([max_fmeas_thresh,max_fmeas,max_fmeas_fnr,max_fmeas_fpr])
	# out_l_kpa.append([max_kappa_thresh,max_kappa,max_kappa_fnr,max_kappa_fpr])
	# return out_l_fms,out_l_fms

def print_output(out_l,fl_nm,perf_meas,sffx):
	out_l.sort(key=lambda k: (k[0]))
	out = open(fl_nm+"."+sffx,"w")
	out.write("#thresh\t%s\tFNR\tFPR\n"%perf_meas)
	for subl in out_l:
		out_subl = []
		for item in subl:
			out_subl.append(str(item))
		out_str = "\t".join(out_subl)+"\n"
		out.write(out_str)
	out.close()

def main():
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		scores_file = sys.argv[1]
		class_index = int(sys.argv[2])
		score_index = int(sys.argv[3])
		positive_class = sys.argv[4]
		negative_class = sys.argv[5]
		if len(sys.argv) == 7:
			subsample_cnt = int(sys.argv[6])
		else:
			subsample_cnt = ""
	except:
		print_help()
		print("Error reading arguments, quitting!")
		sys.exit()
	
	pos_val_list,neg_val_list = pull_class_vals(scores_file,class_index,score_index,positive_class,negative_class)
	comparison = compare_median(pos_val_list,neg_val_list)
	if comparison == "pos_equal":
		comparison = compare_percentile(pos_val_list,neg_val_list,90)
		if comparison == "pos_equal":
			comparison = compare_nonzero(pos_val_list,neg_val_list)	
	print("positive=%s"%(positive_class),comparison)
	# subsample_cnt = 1000
	if subsample_cnt == "":
		subsample_cnt = get_min_class_size(scores_file,class_index)
	print(subsample_cnt)
	fmeas_out_list_balanced,kappa_out_list_balanced = subsample_and_calc_error_rates(pos_val_list,neg_val_list,subsample_cnt,comparison)
	# fmeas_out_list,kappa_out_list = calc_error_rates(pos_val_list,neg_val_list,comparison)
	# calc_error_rates(scores_file,pos_val_list,neg_val_list,comparison)
	print_output(fmeas_out_list_balanced,scores_file,"fmeas","balFm_error_rate")
	print_output(kappa_out_list_balanced,scores_file,"kappa","balKap_error_rate")
	# print_output(fmeas_out_list,mld_file,"fmeas_error_rate")
	# print_output(kappa_out_list,mld_file,"kappa_error_rate")

if __name__ == "__main__":
	main()
