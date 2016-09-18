try:
        import db
        from SCH_NET import *
except:
        import myproject.myapp.functions.db as db
        from myproject.myapp.functions.SCH_NET import *

import re
import datetime

class ASRR:
	def __init__(self, BF="wBOM.txt", SF=""):
		self.BOM = db.BOM_db(BF);
		self.SCH = db.SCH_db(SF);
		self.SCHnet = SCH_NET();
		#self.BOM.BOM_parse();
		#self.SCH.EXP_parse();
		self.op_comp = False;
		self.parsed = False;
		self.set_op = [[],[]];#0:corresponding, 1: incorresponding
		self.unset_op = [[],[]];#0:corresponding, 1: incorresponding
		self._output=''
		
		self.part_both = set()
		self.part_SCH = set()
		self.part_BOM = set()
	
	def set_sch_file(self, ff, comp):
		self.SCH.set_filename(ff);
		self.SCH.set_comp_file(comp);
	
		

	def clear(self):
		self.BOM.clear();
		self.SCH.clear();
		self.op_comp = False;
		self.parsed = False;
		self.op_clear()
		self._output=''
		self.part_both.clear()
		self.part_SCH.clear()
		self.part_BOM.clear()
		
	def op_clear(self):
		self.set_op = [[], []];
		self.unset_op = [[], []];		
	def output_append(self,*arg):
		temp = ''
		for i in arg:
			temp += str(i)+'\t'
		self._output += temp[:-1]+'\n'
		return
	
	def output_clear(self):
		self._output = ''
		return
		
	def output_print(self):
		print()
		print()
		print('%s >>>>>'%datetime.datetime.now().strftime('%y-%m-%d  %H:%M:%S'))
		print(self._output)
		self.output_clear()
		return
		
	
	def show_BOM(self, type_flag = '',attrs = [], values = [], col_name = ['Part Number'], method = 1, keys = None, dic =None):

		self.BOM.print_BOM(type_flag, attrs, values, col_name, method, keys, dic)
		return 
		
		
	def show_sch(self, col_name = [], attrs = [], values= [], method = 1, keys = None, dic =None):
		self.SCH.print_SCH(col_name, attrs, values, method, keys, dic)
	
	def find_location_SCH(self, value):
		col_name = ['PCB Footprint', 'Value', 'Part Number', 'Component_Name', 'Package_Type', 'Optional', 'OPTIONAL', 'optional']
		keys = self.SCH.fetch([self.SCH.getkey()], [value])
		self.SCH.show(keys, None, col_name)
		#keys = None ->all elements
		#self.show_sch(col_name, lst = self.SCH.get_from_key(value))
		return
		'''			
				print('     Footprint:  ', part[self.footprint])
				print('     Part Value: ', part[self.part_value])
				print('     PN:         ', part[self.part_number])
				print('     Part Name:  ', part[self.part_name])
				print('     Part Type:  ', part[self.part_type])
				if self.op1 is not 0:
					print('     op1:        ', part[self.op1])
				if self.op2 is not 0:
					print('     op2:        ', part[self.op2])
				if self.op3 is not 0:
					print('     op3:        ', part[self.op3])'''
		
		
	def find_location_BOM(self, value):
		if value in self.BOM.get_locations():
			print('%s in BOM' % value)
		else:
			print('Not found %s in BOM' % value)
		return
	def EXP_out(self):
		self.SCH.export();
	
	def parser_init(self, sku = ''):
		self.BOM.parser();
		self.SCH.parser(sku);
		self.parsed = True;
		
		sch_id = set(self.SCH.get_elements().keys())
		bom_location = set(self.BOM.get_locations().keys())
		
		#part_both: both in SCH and BOM
		#part_SCH: only found in SCH
		#part_BOM: only found in BOM		
		self.part_both = sch_id.intersection(bom_location)
		self.part_SCH = sch_id - bom_location
		self.part_BOM = bom_location - sch_id

	def check_optional(self, page="", flag = False):
		#self.BOM.BOM_parse();
		#self.SCH.EXP_parse();
		if(not self.parsed):
			return;
		
		self.op_clear()
##		self.output_clear()
		if page:
			if self.SCH.SCH_type != 'PARTINST' and not self.SCH.comp_parsed:
				print('check_optional_by_page only functions at instance-EXP or occurrence-EXP with comp-file')
				return
		#self.output_append('Page'.center(35), '-----', 'SCH Optional'.center(17), '<<<', 'Location/description'.center(19), '>>>   BOM    -----')
		
		#self.output_append('*'*122)
		
		self.op_comp = True
		#print(self.SCH.fetch(self.SCH.get_page_key(), page)
		part_both_page = self.SCH.fetch([self.SCH.get_page_key()], [page], 2, self.part_both)
		
		
		for part in part_both_page:
			
			sch_element = self.SCH.get_from_key(part)
			
			if sch_element[self.SCH.get_op_key()]:
				self.unset_op[0].append(part.upper())
			else:
				self.unset_op[1].append(part.upper())
			
			#page_info = sch_element[self.SCH.get_page_key()]
			#if page and not(page in page_info):
			#	continue;
			
			#optional message
			#op_temp = []
			#for op in self.SCH.get_op_name():
			#	op_temp.append(sch_element[op])
			#mes = '|'.join(op_temp)
			
			#	Page								------	optionals		===		"ID"											>>>		Y	-----
			#self.output_append(page_info.center(35), '-----', mes.center(17), '===', ('"'+ part + '"').center(19),">>>    Y     -----")
			
		
		#self.output_append('Incorresponding elements/ Total elements: %d/ %d'%(len(self.unset_op[1]), len(self.unset_op[1])+len(self.unset_op[0])))
		#self.output_append('='*122)
		
		part_SCH_page = self.SCH.fetch([self.SCH.get_page_key()], [page], 2, self.part_SCH)
		for part in part_SCH_page:
			#why Capital?
			
			#self.set_op.append(part)
						
			sch_element = self.SCH.get_from_key(part)
			
			if not sch_element[self.SCH.get_op_key()]:
				#corresponding case
				self.set_op[0].append(part.upper())
			else:
				self.set_op[1].append(part.upper())
			
			
			#page_info = sch_element[self.SCH.get_page_key()]
			#if page and not(page in page_info):
			#	continue;

			#optional message
			#op_temp = []
			#for op in self.SCH.get_op_name():
			#	op_temp.append(sch_element[op])
			#mes = '|'.join(op_temp)
		
			#self.output_append(page_info.center(35), '-----', mes.center(17),'<<<', ('"' + part + '"').center(19),"===    N     -----")
			
		#self.output_append('Incorresponding elements/ Total elements: %d/ %d'%(len(self.set_op[1]), len(self.set_op[1])+len(self.set_op[0])))
		#self.output_append('='*122)
		
		
		#self.output_append('###########################')
		#self.output_append("Locations cannot find in SCH:")	
##		count = 0	
##		for part in self.part_BOM:
##			#location --> part number --> elements
##			BOM_part_name = self.BOM.get_from_key(part, self.BOM.get_locations())
##			BOM_element = self.BOM.get_from_key(BOM_part_name)
##			
##			self.output_append(BOM_part_name + "\t" + part + "\t" + BOM_element['Component_Name'])
##			count += 1
##	
##		self.output_append('Elements on BOM but not SCH: %d'%(count))
##		self.output_append('='*50)
##		
##		self.output_append('-'*22+'Result'+'-'*22)
##		self.output_append('Elements on SCH and BOM:')
##		self.output_append('Incorresponding elements/ Total elements: %d/ %d'%(len(self.unset_op[1]), len(self.unset_op[1])+len(self.unset_op[0])))
##		self.output_append('Elements on SCH but not in BOM:')
##		self.output_append('Incorresponding elements/ Total elements: %d/ %d'%(len(self.set_op[1]), len(self.set_op[1])+len(self.set_op[0])))
##		self.output_append('Subtotal: %d'% (len(self.unset_op[1])+len(self.unset_op[0])+len(self.set_op[1])+len(self.set_op[0])))
##		self.output_append('')
##		self.output_append('Elements on BOM but not SCH:')
##		self.output_append('%d'%(count))
##		self.output_append('-'*122)
##		
##		self.output_append('Total elements counted from SCH: %d' % len(self.SCH.get_elements()))
##		self.output_append('='*22+'END...'+'='*22)
##		self.output_print()
		#print(len(part_both),len(part_SCH), len(part_BOM))
		
		part_BOM_lst = list(self.part_BOM)
		return (self.unset_op,
                        self.set_op,
                        part_BOM_lst
                        )

	def list_by_optional(self, opt=""):
		#self.BOM.BOM_parse();
		#self.SCH.EXP_parse();
		#print(opt)
		if(not self.parsed):
			return;
##		self.output_clear()		
##		self.output_append('Page'.center(35), '-----', 'SCH Optional'.center(35), '<<<', 'Location/description'.center(73), '>>>', 'BOM'.center(11), "-----")
##		self.output_append('*'*165)
		

		
##		self.output_append("Both")
		part_Both_op = self.SCH.op_check(op_value = opt, keys = self.part_both)
		part_SCH_op = self.SCH.op_check(op_value = opt, keys = self.part_SCH)
		return (part_Both_op, part_SCH_op)
##		count = 0
##		for part in self.part_both:
##			
##			
##			sch_element = self.SCH.get_from_key(part)
##			page_info = sch_element[self.SCH.get_page_key()]
##
##			
##			#optional message
##			op_temp = []
##			flag = False
##			
####			for op in self.SCH.get_op_name():
####				op_temp.append(sch_element[op])
####				if re.match(opt, sch_element[op]):
####					flag =True
##			if not flag:
##				continue
##			mes = '|'.join(op_temp)
##			
##			count += 1
##			BOM_part_name = self.BOM.get_from_key(part, self.BOM.get_locations())
##			BOM_element = self.BOM.get_from_key(BOM_part_name)
##			self.output_append(page_info.center(35), '-----', mes.center(40), '===', ('"'+ part+ '"').center(20), ">>>", 'Y'.center(11),"-----   ", BOM_part_name, BOM_element['Component_Name'])
##		self.output_append('-'*50)
##		self.output_append('Subtotal: %d'%count)
##		self.output_append('='*50)
##		
##		self.output_append("Only in SCH")
##		count =0
##		for part in self.part_SCH:
##						
##
##			sch_element = self.SCH.get_from_key(part)
##			page_info = sch_element[self.SCH.get_page_key()]
##
##			#optional message
##			op_temp = []
##			flag = False
##			for op in self.SCH.get_op_name():
##				op_temp.append(sch_element[op])
##				if re.match(opt, sch_element[op]):
##					flag =True
##			if not flag:
##				continue
##			count += 1
##			mes = '|'.join(op_temp)
##			
##						
##			self.output_append(page_info.center(35), '-----', mes.center(40), '===', ('"' + part + '"').center(20), ">>>", 'N'.center(11),"-----")
##		self.output_append('-'*50)
##		self.output_append('Subtotal: %d'%count)
##		self.output_append('='*50)
##		
##		
##		
##		#check if BOM have location but SCH don't
##		if(opt == ""):
##			self.output_append("Only in BOM")
##			self.output_append('###########################')
##			self.output_append("Locations cannot find in SCH:")		
##			for part in self.part_BOM:
##				#location --> part number --> elements
##				BOM_part_name = self.BOM.get_from_key(part, self.BOM.get_locations())
##				BOM_element = self.BOM.get_from_key(BOM_part_name)
##			
##				self.output_append(BOM_part_name + "\t" + part + "\t" + BOM_element['Component_Name'])
##		
##			self.output_append('-'*50)
##			self.output_append('Subtotal: %d'%len(self.part_BOM))
##			self.output_append('='*50)
##		
##		self.output_print()
		

		
	def optional_write(self):
##		print("write option back to sch")
##		print("1. set option to '/x' : ")
##		#print(self.set_op);
##		print("2. set option to 'N/A' :")
##		#print(self.unset_op);
		
		for key in self.set_op[1]:
			element = self.SCH.get_from_key(key)

			for op in self.SCH.get_op_name():
				self.SCH.set(element, op, '/X')
			#print(type(element))
			#print(element)
			#print(self.SCH.get_op_key())
			self.SCH.set(element, self.SCH.get_op_key(), False)

		for key in self.unset_op[1]:
			element = self.SCH.get_from_key(key)
			
			for op in self.SCH.get_op_name():
				self.SCH.set(element, op, 'N/A')
			self.SCH.set(element, self.SCH.get_op_key(), True)



				
				
				
	def check_flag(self,flag):
		if flag.lower() == 'size':
			return 'PCB Footprint'
		if flag.lower() == 'pn':
			return 'Part Number'
		if flag.lower() == 'value':
			return 'Value'
		else:
			return 'Component_Name'
		
	def check_comp(self, check_type,fun_flag, SCH_attr, BOM_attr):
		if check_type == 'res' and fun_flag == 'Value':
			return self.res2value(BOM_attr) == self.res2value(SCH_attr)
		if fun_flag == 'PCB Footprint':
			return BOM_attr in SCH_attr
		else:
			return BOM_attr == SCH_attr
		
	def check_difference(self, check_type, flag='cn', except_R_C = False):	
		"""Compare  and show the difference between parts in SCH and BOM

		Args:
			check_type: type of part. res, mlcc/ cap, other
			flag: compare value. size, pn, value, cn(default)
			
		 Return:
			 None
		"""
			
		fun_flag = self.check_flag(flag)
		bom_flag = fun_flag
		if check_type.lower() == 'res':
			type_flag = '^10G'
			
		elif check_type.lower() == 'mlcc' or check_type.lower() == 'cap':
			type_flag = '^11G'
		#elif check_type.lower() == 'ind':
		#	type_flag = '^09G'
		#	if flag != 'pn':bom_flag = 'Component_Name'
		else:
			if not fun_flag in ['Component_Name','Part Number']:
				print('(%s, %s) is not acceptable' % (check_type, fun_flag)) 
				return
			type_flag = '.'
		
		SCH_keys = set(self.SCH.fetch(['Part Number'], [type_flag], method = 3, keys = self.part_both))
		if except_R_C:
			SCH_keys -= set(self.SCH.fetch(['Part Number'], ['^10G'], method = 3, keys = self.part_both))
			SCH_keys -= set(self.SCH.fetch(['Part Number'], ['^11G'], method = 3, keys = self.part_both))
		
		#self.output_clear()
		#self.output_append('####### Check %s %s! #######' % (check_type,fun_flag))
		#self.output_append('Page'.center(35), '----', 'Location'.center(20), ':', 'SCH'.center(30),   '<===>', 'BOM'.center(30))
		
		incor = self.check_incor()
		SCH_keys -= set(incor)
		#SCH_keys = list(SCH_keys)
		#count = 0
		return([x for x in SCH_keys
                        if not
                        self.check_comp(check_type,
                                        fun_flag,
                                        self.SCH.get_from_key(x)[fun_flag],
                                        self.BOM.get_from_key(self.BOM.get_from_location(x.upper()))[bom_flag]
                                        )
                        ],
                       
                       incor
                       )
		
		
##		for SCH_key in SCH_keys:
##
##			SCHpart = self.SCH.get_from_key(SCH_key)
####			if re.match('10G', SCHpart['Part Number']) or re.match('11G', SCHpart['Part Number']):
####				continue
##			BOM_key = self.BOM.get_from_location(SCH_key.upper())
##			BOMpart = self.BOM.get_from_key(BOM_key)
##			
##			#BOM is not corresponding to SCH
####			if not SCHpart['Part Number'][:3] == BOMpart['Part Number'][:3]:
####				incor.append([SCH_key, SCHpart['Part Number'], BOMpart['Part Number']])
####				continue
##				
##			
##			if not self.check_comp(check_type, fun_flag, SCHpart[fun_flag], BOMpart[bom_flag]) :
##			#(BOMpart[bom_flag] in SCHpart[fun_flag] or SCHpart[fun_flag] in BOMpart[bom_flag]):
##				page_info = SCHpart[self.SCH.get_page_key()]
##				self.output_append(page_info.center(35), "----", SCH_key.upper().center(20), ":", SCHpart[fun_flag].center(30), "<===>", BOMpart[bom_flag].center(30));
##				count += 1
				
##		self.output_append('####### Check %s %s done #######' % (check_type,fun_flag))
##		
##		self.output_append('Number of part with different %s: %d/ %d'% (fun_flag,count, len(SCH_keys)))
##		self.output_append('################################')
##		for x in incor:
##			self.output_append('Type of %s is not corresponding(SCH: %s; BOM: %s)'% (x[0], x[1], x[2]))
##		if incor:
##			self.output_append('################################')
#			self.output_append('Number of part with different type: %d/ %d'% (len(incor), len(SCH_keys)))
			
##		self.output_print()
		
	def check_y5v(self):
##		self.output_clear()
##		self.output_append("####### List all Y5V mlcc #######");
		type_flag = '^11G';

		SCH_keys = set(self.SCH.fetch(['Part Number'], [type_flag], method = 3, keys = self.part_both))
		incor = self.check_incor()
		SCH_keys -= set(incor)
		
		#count = 0
		return ([x for x in SCH_keys
                         if self.BOM.get_from_key(self.BOM.get_from_location(x.upper()))['CChar'].upper() == 'Y5V'],
                        incor)
##		for SCH_key in self.SCH.fetch(['Part Number'], [type_flag], method = 3):
##			SCHpart = self.SCH.get_from_key(SCH_key)
##			try:
##				BOM_key = self.BOM.get_from_location(SCH_key.upper())
##			except KeyError:
##				#SCHpart not in BOM
##				continue
##			BOMpart = self.BOM.get_from_key(BOM_key) 
##			#BOM is not corresponding to SCH
##			if not SCHpart['Part Number'][:3] == BOMpart['Part Number'][:3]:
##				incor.append([SCH_key, SCHpart['Part Number'], BOMpart['Part Number']])
##				continue
##			if BOMpart['CChar'].upper() == 'Y5V':
##				page_info = SCHpart[self.SCH.get_page_key()]
##				self.output_append(page_info.center(35), "----", SCH_key.upper().center(20), ":", SCHpart['Component_Name'].center(30))
##				count += 1
##		self.output_append("####### List all Y5V mlcc #######");
##		self.output_append('Total Y5V elements: %d'%count)
##		self.output_append('################################')
##		for x in incor:
##			self.output_append('Type of %s is not corresponding(SCH: %s; BOM: %s)'% (x[0], x[1], x[2]))
##		if incor:
##			self.output_append('################################')
##			self.output_append('Number of part with different type: %d'% (len(incor)))
##		self.output_print()
##		
	def check_incor(self):
		
		#self.output_clear()
		#self.output_append('Page'.center(35), '----', 'Location'.center(20), ':', 'SCH'.center(30),   '<===>', 'BOM'.center(30))
		#count = 0
		return [x for x in self.part_both
			if self.SCH.get_from_key(x)['Part Number'][:3]!=
			self.BOM.get_from_location(x.upper())[:3]]
##		for SCH_key in self.part_both:
##			SCHpart = self.SCH.get_from_key(SCH_key)
##			BOM_key = self.BOM.get_from_location(SCH_key.upper())
##			BOMpart = self.BOM.get_from_key(BOM_key)
##			if SCHpart['Part Number'][:3] != BOMpart['Part Number'][:3]:
##				page_info = SCHpart[self.SCH.get_page_key()]
##				self.output_append(page_info.center(35), "----", SCH_key.upper().center(20), ":", SCHpart['Part Number'].center(30), "<===>", BOMpart['Part Number'].center(30));
##				count += 1
##		self.output_append('Total: %d' % count)
##		self.output_print()
				
	
	def correct(self, cor_type):
##		if cor_type.lower() == 'res':
##			type_flag = '^10G'
##			#attrs = ['Part Number', 'Value', 'PCB Footprint', 'Tolerance']
##			
##		elif cor_type.lower() == 'mlcc' or cor_type.lower() == 'cap':
##			type_flag = '^11G'
##			#attrs = ['Part Number', 'Value', 'PCB Footprint', 'CType', 'CChar', 'Tolerance']
##			
##		else:
##			#print('%s is not acceptable ' % cor_type)
##			#return
##			#print('correct all element')
##			#type_flag = '.'
##			#attrs = ['Part Number', 'Component_Name']
##			type_flag = '^.'
##		
		attrs = ['Part Number', 'Value', 'PCB Footprint', 'Tolerance', 'Component_Name']
		
		#count = 0
		#print('####### write %s property to EXP #######' % cor_type)
		diff = self.check_difference(cor_type, 'pn', False)[0]
		for SCH_key in diff:
			SCHpart = self.SCH.get_from_key(SCH_key)
			BOM_key = self.BOM.get_from_location(SCH_key.upper())
			BOMpart = self.BOM.get_from_key(BOM_key) 
			#type of part in SCH and BOM should be corresponding
			for attr in attrs:
				if attr in BOMpart:
					self.SCH.set(SCHpart, attr, BOMpart[attr])
		return(diff)			
##
##		print('-'*100)
##		print('Total: %d/ %d %s elements modified in SCH' % (count, len(both_key), cor_type))
		#print(attrs)
		#print('='*100)
		
		
		#print('Only in SCH:')
		#SCH_keys = self.SCH.fetch(['Part Number'], [type_flag], method = 3, keys = self.part_SCH)
		#for SCH_key in SCH_keys:
		#	print('%s'%SCH_key)
		#print('-'*100)
		#print('Total: %d elements only in SCH' % len(SCH_keys))
		#print('='*100)
		
		
		#print('Only in BOM:')
		#count = 0
		#for BOM_key in self.part_BOM:
		#	if  re.match(type_flag, self.BOM.get_from_key(BOM_key, self.BOM.get_locations())):
		#		print(BOM_key)
		#		count += 1
		#print('-'*100)
		#print('Total: %d elements only in BOM' % count)
			
		
#		print('####### write %s property to EXP done #######' % cor_type)
		
	
		
		
		
	def list_inductor(self):
		self.output_clear()
		self.output_append('####### List 09G Inductor #######')
		type_flag = '^09G';
		for SCH_key in self.SCH.fetch(['Part Number'], [type_flag], method = 3):
			SCHpart =self.SCH.get_from_key(SCH_key)
			try:
				BOM_key = self.BOM.get_from_location(SCH_key.upper())
			except KeyError:
				#SCHpart not in BOM
				continue
			BOMpart = self.BOM.get_from_key(BOM_key) 
			page_info = SCHpart[self.SCH.get_page_key()]
			self.output_append(page_info.center(35), "----", SCHpart['ID'].upper().center(20), ":", SCHpart['Value'].center(30), "<===>", BOMpart['Component_Name'].center(30));

		self.output_append('####### List 09G Inductor #######')
		self.output_print()
		
	
		
		
	def check_part_by_PN(self, level):
		if level == "":
			return;
##		self.output_clear()
##		self.output_append('^' + level + "wendi");
##		self.output_append('####### List #######')
##		self.output_append('Page'.center(35),'----','Location'.center(15), ": ", 'SCH'.center(20), ' <---> ', 'BOM'.center(20))
##		self.output_append('-'*120)
		#res = '^'+ level;
		#tmp = [];
		
		locations = self.BOM.get_locations()

		Both_keys = self.SCH.fetch(['Part Number'], [level], 3, self.part_both)
		#l = self.SCH.get(attrs = ['Part Number'], values = [level], method = 2, lst = self.SCH.get_from_key(part_both))
		#for part in lst:
##		for part in both_keys:
##			#print(part['ID'])
##			sch_element = self.SCH.get_from_key(part)
##			page_info = sch_element[self.SCH.get_page_key()]
##			
##			BOM_part_name = self.BOM.get_from_key(part, locations)
##			
##			self.output_append(page_info.center(35), "----", part.center(15), ": ", sch_element['Value'].center(20), ' <---> ', BOM_part_name.center(20));
##			#self.output_append(' '.center(35), "----", part['ID'].center(15))
##			#self.output_append( ": ", part['Value'].center(20))
##			#self.output_append( ' <---> ', BOM_part_name.center(20));
##		#for part in tmp:
##		#	print(part[0].split(':')[2].center(35), " ... ", part[self.SCH.location].center(15), ": ", part[self.SCH.part_value].center(15), " <$$$> ", self.BOM.wBOM[count][1].center(15));
##		self.output_append('-'*120)
		
		SCH_keys = self.SCH.fetch(['Part Number'], [level], 3, self.part_SCH)
##		for part in SCH_keys:
##			sch_element = self.SCH.get_from_key(part)
##			page_info = sch_element[self.SCH.get_page_key()]
##			self.output_append(page_info.center(35), "----", part.center(15), ": ", sch_element['Value'].center(20), ' <---> ', 'XXXXXX'.center(20));
##		self.output_append('-'*120)
		
		BOM_keys = list(filter(lambda x:re.match(level, self.BOM.get_from_key(x, locations)), self.part_BOM))
		return (Both_keys, SCH_keys, BOM_keys)
##		for part in BOM_keys:
##			BOM_part_name = self.BOM.get_from_key(part, locations)
##			self.output_append('------'.center(35), "----", part.center(15), ": ", 'XXXXXX'.center(20), ' <---> ', BOM_part_name.center(20));
##			
##		
##		self.output_append('####### List done #######')
##		self.output_print()

	def res2value(self, rr):
		for i, cc in enumerate(rr):
			if not cc.isdigit():
				num = float(rr[:i])
				if rr[i].lower() == 'k':
					return num*1000;
				elif rr[i].lower() == 'm':
					return num*1000000;
				else:
					return num;
		return float(rr)

	

		
		
		
		
	#20160531
	
	

	def check_BOM_location(self):
		print('Check location in BOM but cannot find in SCH!')







	def snet_parser(self, fn):
		self.SCHnet.open_net_file(fn);
		self.SCHnet.parse();

	#def check_ME(self):
	#           self.SCH.

	def check_cap_derating(self):
		print("#############  CAP deRating  #############");
		cap = '^11G';
		for index, item in enumerate(self.BOM.wBOM):
			if re.match(cap, item[0]):
				print(index, ": ", item[0], "(", item[1], ")");
				for part in self.BOM.location[index]:
					net_name = self.SCHnet.find_part(part) #will return the net name the part connected
					if len(net_name) != 0:
						for nn in net_name:
							if nn == 'GND':
								continue;
							print(" - ", part, ' ===> ', nn);
					else:
						print(part, "do not show in SCH, plese check!");

		print("#############  CAP deRating  #############");









		
		
'''		
d = ASRR('bom.txt', 'exp.txt')
d.paser_init()
print(len(d.BOM._elements))
print(len(d.SCH._elements))
print('='*300)
#d.show_BOM()

print('='*300)
#d.show_sch()
print('='*300)
#d.check_optional()
print()
'''


'''
Clearing database...
Done...
EXP parsing done...
Clearing database...
Done...
EXP parsing done...
filtering:  match Component type
    ==>  ['RP1545', 'RP170']

    ==>  ['PQST3', 'PQST100']

    ==>  ['RPST11']

================================================================================
Total: 3
  ID: RPST110

  ID: RPST11

  ID: PQST1

  ID: PQST3

  ID: PQST100

================================================================================
Total: 5
-----        SCH        <<<=====================>>>     BOM  -----
******************************************************************
   87.+V3.3M_LAN & +5VSB/+3VSB SW   -----      N/A|N/A      ===       "RPST11"      >>>      Y   -----
   87.+V3.3M_LAN & +5VSB/+3VSB SW   -----   <null>|<null>   ===       "PQST3"       >>>      Y   -----
   87.+V3.3M_LAN & +5VSB/+3VSB SW   -----     /x|<null>     ===      "PQST100"      >>>      Y   -----
   87.+V3.3M_LAN & +5VSB/+3VSB SW   -----        N/A        <<<      "RPST110"      ===      N   -----
   87.+V3.3M_LAN & +5VSB/+3VSB SW   -----        N/A        <<<       "PQST1"       ===      N   -----
###########################
Locations cannot find in SCH:
10G212806214010	RP1545	RES 80.6K OHM 1/16W (0402) 1%
10G212806214010	RP170	RES 80.6K OHM 1/16W (0402) 1%
###########################
******************************************************************
'''
