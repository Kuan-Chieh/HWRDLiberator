import os
import sys
import subprocess
from ADesign_KC import *
from tkinter import *
from tkinter.filedialog import *

design = ASRR("wBOM.txt")
init_dir = ""
key_name = ''
page_key = ''
op_name = ''

class output_f:
    _output = ''
    def append(self,*arg):
        for i in arg:
            temp = ''
            for j in i:
                temp += str(j)+'\t'
            self._output += '%s\n'%temp
        return
	
    def init(self, function = ''):
        self._output = ''
        self.append([''],[''],[''],['%s >>>>>>%s'%(datetime.datetime.now().strftime('%y-%m-%d  %H:%M:%S'), function)], [''])
        return

    def print(self):
        self.append([''], ['%s >>>>>>Done'%datetime.datetime.now().strftime('%y-%m-%d  %H:%M:%S')],[''])
        print(self._output)        
        return


output = output_f()

def SEL_Input(ent):
    global init_dir
    ent.delete(0, len(ent.get()))
    ftmp = askopenfilename(initialdir=init_dir)
    init_dir = os.path.split(ftmp)[0]
    ent.insert(0, ftmp)

def makeform(root, fields):
    rows = []
    entries = [];
    for ff in fields:
        row = Frame(root)
        lab = Label(row, width=8, text=ff)
        ent = Entry(row, width=80)
        row.pack(side=TOP, fill=X)
        lab.pack(side=LEFT)
        ent.pack(side=LEFT, fill=X)
        entries.append(ent)
        rows.append(row)

    Button(rows[0], text='SEL', command=lambda:SEL_Input(entries[0])).pack(side=RIGHT)
    Button(rows[1], text='SEL', command=lambda:SEL_Input(entries[1])).pack(side=RIGHT)
    Button(rows[2], text='SEL', command=lambda:SEL_Input(entries[2])).pack(side=RIGHT)
    Button(rows[3], text='SEL', command=lambda:SEL_Input(entries[3])).pack(side=RIGHT)
    Button(rows[4], text='SEL', command=lambda:SEL_Input(entries[4])).pack(side=RIGHT)
    
    return entries

def call_wBOM_parser(bom_list):
    boms = []
    for bb in bom_list:
        boms.append(bb.get())
    if(boms[0] == '' and boms[1] == '' and boms[2] == ''):
        print("Need BOM file!")
        return;
    arg = '" "'.join([x for x in boms[:3] if x != ''])
    arg = 'WASRBOM.exe "' + arg + '" wBOM.txt' + ' 2'
    #arg = 'WASRBOM.exe "' + arg + '" wasdqwe.txt' + ' 2'
    print(arg)
    #os.popen(arg)
    subprocess.call(arg)
    comp_init(boms[-3], boms[-2], boms[-1])

def comp_init(exp, comp, sku):
    if exp:
        print(exp)
        design.set_sch_file(exp, comp)
        #design.check_optional()
        design.parser_init(sku)

        global page_key, op_name, key_name
        page_key = design.SCH.get_page_key()
        op_name = design.SCH.get_op_name()
        key_name = design.SCH.getkey()
        
    else:
        print("Need SCH EXP file!")

def get_BOM_from_loc(part):
    BOM_part_name = design.BOM.get_from_key(part, design.BOM.get_locations())
    BOM_element = design.BOM.get_from_key(BOM_part_name)
    return BOM_part_name, BOM_element

def op2mes(element):
    global op_name
    op_temp = []
    for op in op_name:
        op_temp.append(element[op])
    return '|'.join(op_temp)
        
def op_check(page):    
    output.init('Optional Check')
    global page_key
    
    unset_op, set_op, BOM = design.check_optional(page, True)
    Both = design.SCH.get_from_keys(unset_op[1])
    SCH = design.SCH.get_from_keys(set_op[1])
    output.append(['Page'.center(35), '-----', 'SCH Optional'.center(17), '<<<', 'Location/description'.center(19), '>>>   BOM    -----'],
                  ['*'*122])
    
    for element in Both:
        page_info = element[page_key]
        mes = op2mes(element)
            
            
        output.append([page_info.center(35),
                       '-----',
                       mes.center(17),
                       '===',
                       ('"'+ element[key_name] + '"').center(19),
                       ">>>    Y     -----"
                       ],)
    output.append(['='*122])
    
    for element in SCH:
        page_info = element[page_key]
        mes = op2mes(element)
            
            
        output.append([page_info.center(35),
                       '-----',
                       mes.center(17),
                       '<<<',
                       ('"'+ element[key_name] + '"').center(19),
                       "===    N     -----"
                       ])
    output.append(['#'*122], ['Locations cannot find in SCH:'])
    
    
    for element in BOM:
        BOM_part_name = design.BOM.get_from_key(part, self.BOM.get_locations())
        BOM_element = self.BOM.get_from_key(BOM_part_name)
        output.append([BOM_part_name, element, BOM_element['Component_Name']])
        
    output.append([''])
    output.append(['-'*22+'Result'+'-'*22],
                  ['Elements on SCH and BOM:'],
                  ['Incorresponding elements/ Total elements: %d/ %d'%(len(unset_op[1]),
                                                                       len(unset_op[1])+len(unset_op[0]))],
                  [''],
                  ['Elements on SCH but not in BOM:'],
                  ['Incorresponding elements/ Total elements: %d/ %d'%(len(set_op[1]),
                                                                       len(set_op[1])+len(set_op[0]))],
                  [''],
                  ['Subtotal elements: %d'% (len(unset_op[1])+len(unset_op[0])+len(set_op[1])+len(set_op[0]))],
                  [''],
                  ['Elements on BOM but not SCH:'],
                  [len(BOM)],
                  ['-'*122],
                  )
    
    
        
    
    output.print()

def lst_by_op(opt = ''):
    global page_key
    output.init('List by optional')
    part_Both_op, part_SCH_op = design.list_by_optional(opt)
    output.append(['Page'.center(35),
                   '-----', 'SCH Optional'.center(35),
                   '<<<', 'Location/description'.center(73),
                   '>>>', 'BOM'.center(11), "-----"
                   ],

                  ['*'*165],

                  ["Both"]
                  )
    for part in part_Both_op:
        element = design.SCH.get_from_key(part)
        page_info = element[page_key]
        mes = op2mes(element)
        BOM_part_name, BOM_element = get_BOM_from_loc(part)
        output.append([page_info.center(35),
                       '-----',
                       mes.center(40),
                       '===',
                       ('"'+ part+ '"').center(20),
                       ">>>", 'Y'.center(11),
                       "-----   "
                       , BOM_part_name,
                       BOM_element['Component_Name']])
    output.append(['-'*50],
                  ['Subtotal: %d'%len(part_Both_op)],
                  ['='*50],
                  ["Only in SCH"],)
    for part in part_SCH_op:
        element = design.SCH.get_from_key(part)
        page_info = element[page_key]
        mes = op2mes(element)
        output.append([page_info.center(35),
                      '-----',
                      mes.center(40),
                      '===',
                      ('"' + part + '"').center(20),
                      ">>>", 'N'.center(11),
                      "-----"],)
    output.append(['-'*50],
                  ['Subtotal: %d'%len(part_SCH_op)],
                  ['='*50],
                  ["Only in SCH"],)
    output.print()
    
def optional_show():
    output.init('OP show')
    output.append(["1. set option to '/x' : "],
                  ["Corresponding part:"],
                  [design.set_op[0]],
                  ["Incorresponding part:"],
                  [design.set_op[1]],
                  ["2. set option to 'N/A' :"],
                  ["Corresponding part:"],
                  [design.unset_op[0]],
                  ["Incorresponding part:"],
                  [design.unset_op[1]],
                  )
    output.print()
                   
                   
         
def op_write():
    output.init('OP show')
    output.append(["write option back to sch"],
                  ["1. set option to '/x' : "],
                  ["2. set option to 'N/A' :"],
                  )
    design.optional_write()
    output.print()
        
def check_type():
    global page_key
    output.init('Check type')
    output.append(['Page'.center(35),
                  '----',
                  'Location'.center(20),
                  ':', 'SCH'.center(30),
                  '<===>',
                  'BOM'.center(30)],
                  )
    
    Both_incor = design.check_incor()
    for part in Both_incor:
        element = design.SCH.get_from_key(part)
        page_info = element[page_key]
        BOM_part_name, BOM_element = get_BOM_from_loc(part)
        output.append([page_info.center(35),
                       "----",
                       SCH_key.upper().center(20),
                       ":",
                       SCHpart['Part Number'].center(30),
                       "<===>",
                       BOMpart['Part Number'].center(30)])
    output.append(['-'*122],
                  ['Total: %d' % len(Both_incor)])
    output.print()

def check_diff(check_type, flag='cn', except_R_C = False):
    bom_flag = fun_flag = design.check_flag(flag)
    output.init('Check %s %s' %(check_type, fun_flag))
    global page_key
    
    output.append(['################################'],
                  ['Page'.center(35),
                  '----', 'Location'.center(20),
                  ':',
                  'SCH'.center(30),
                  '<===>',
                  'BOM'.center(30)])
    Both_check, incor = design.check_difference(check_type, flag, except_R_C)
    for part in Both_check:
        element = design.SCH.get_from_key(part)
        page_info = element[page_key]
        BOM_part_name, BOM_element = get_BOM_from_loc(part)
        output.append([page_info.center(35),
                       "----",
                       part.upper().center(20),
                       ":",
                       element[fun_flag].center(30),
                       "<===>",
                       BOM_element[bom_flag].center(30)])
    output.append(['################################'],
                  ['Number of part with different %s: %d'% (fun_flag, len(Both_check))],
                  ['################################'],
                  )
    if incor:
        output.append(['Incorresponding elements'],)
        for i in incor:
            output.append([i])
        output.append(['################################'],
                      ['Number of part with different type: %d'% (len(incor))],
                      )
    output.print()

def check_y5v():
    output.init('Check Y5V')
    global page_key
    Both_Y5V, incor = design.check_y5v()
    for part in Both_Y5V:
        element = design.SCH.get_from_key(part)
        page_info = element[page_key]
        BOM_part_name, BOM_element = get_BOM_from_loc(part) 
        output.append([page_info.center(35),
                      "----",
                      part.upper().center(20),
                      ":",
                      element['Component_Name'].center(30)])
    output.append(['################################'],
                  [('Total Y5V elements: %d'%len(Both_Y5V))],
                  ['################################'],
                  )
    if incor:
        output.append(['Incorresponding elements'],)
        for i in incor:
            output.append([i])
        output.append(['################################'],
                      ['Number of part with different type: %d'% (len(incor))],
                      )
        
    output.print()

def modify(cor_type):
    output.init(' Write property of %s to EXP' % cor_type)
    diff = design.correct(cor_type)
    output.append(['-'*122],
                  ['Total: %d %s elements modified in SCH' % (len(diff), cor_type)])
    output.print()
    
def lst_by_PN(PN):
    output.init(' Print all %s-elements' % PN)
    output.append([('Page'.center(35),
                    '----',
                    'Location'.center(15),
                    ": ",
                    'SCH'.center(20),
                    ' <---> ',
                    'BOM'.center(20))],
                  ['-'*120]
                  )
    Both_keys, SCH_keys, BOM_keys = design.check_part_by_PN(PN)
    global page_key
    locations = design.BOM.get_locations()
    for part in Both_keys:
        sch_element = design.SCH.get_from_key(part)
        page_info = sch_element[page_key]
        BOM_part_name = design.BOM.get_from_key(part, locations)
        output.append([page_info.center(35),
                      "----",
                      part.center(15),
                      ": ",
                      sch_element['Value'].center(20),
                      ' <---> ',
                      BOM_part_name.center(20)])

    output.append(['-'*120])
    for part in SCH_keys:
        sch_element = design.SCH.get_from_key(part)
        page_info = sch_element[page_key]
        output.append([page_info.center(35),
                       "----",
                       part.center(15),
                       ": ",
                       sch_element['Value'].center(20),
                       ' <---> ',
                       'XXXXXX'.center(20)
                       ])
    output.append(['-'*120])
    for part in BOM_keys:
        BOM_part_name = design.BOM.get_from_key(part, locations)
        output.append(['------'.center(35),
                       "----",
                       part.center(15),
                       ": ",
                       'XXXXXX'.center(20),
                       ' <---> ',
                       BOM_part_name.center(20)])
    output.append(['-'*120],
                  ['%d "%s"-element in both SCH and BOM'%(len(Both_keys), PN)],
                  ['%d "%s"-element in SCH only'%(len(SCH_keys), PN)],
                  ['%d "%s"-element in BOM only'%(len(BOM_keys), PN)],
                  ['-'*120])
    output.print()
    
    
def main():
    top = Tk("BOM2SCH")
    spl1 = "*"*120;
    spl2 = "#"*60;
    input_BOM = 'BOM_59T', 'BOM_59B', 'BOM_70', 'SCH_EXP', 'Comp_file', 'sku'
    BOMs = makeform(top, input_BOM)

    #init_design_frame = Frame(top);
    btn_wBOM = Button(top, text = 'Design Init', fg='#000079', bg='#66B3FF',command = lambda:call_wBOM_parser(BOMs))
    btn_wBOM.pack()
    #pp = Button(top, text='SCH Init', bg='#00DB00', fg='#000079', command = lambda:comp_init(BOMs[3].get()))
    #pp.pack(fill=X)
    #init_design_frame.pack(fill=X)
    empty1 = Frame(top);
    Label(empty1, text=spl1).pack(fill=X);
    empty1.pack();
    
    
    op_label_frame = Frame(top)
    btn_label = Label(op_label_frame, text='SCH Optional check!')
    btn_label.pack(side=LEFT)
    op_label_frame.pack(fill=X)
    
    op_frame = Frame(top)
    opage = Label(op_frame, text='page:(empty for all SCH)')
    opage.pack(side=LEFT);
    opent = Entry(op_frame, width=30)
    opent.pack(side=LEFT)
    

    
##    op_check_btn = Button(op_frame, text='Show All', command = lambda:design.check_optional(opent.get()))
##    op_check_btn.pack(side=LEFT)
    op_check_btn_op = Button(op_frame, text='Optional Check', command = lambda:op_check(opent.get()))
    op_check_btn_op.pack(side=LEFT)
    
    #cvalue = Button(top, text='Check PN', command = lambda:design.check_value());
    #printBOM = Button(op_frame, text='Print BOM.', command = lambda:design.list_optional_by_page(opent.get()))
    #printBOM.pack()
    op_frame.pack(fill=X)



    empty2 = Frame(top);
    Label(empty2, text=spl1).pack(fill=X);
    empty2.pack();

    op_list_frame = Frame(top)
    opt_lab = Label(op_list_frame, text='Option: (empty for all SCH)')
    opt_lab.pack(side=LEFT);
    opt = Entry(op_list_frame, width=30)
    opt.pack(side=LEFT)
    op_list = Button(op_list_frame, text='list by op', command = lambda:lst_by_op(opt.get()))
    op_list.pack(side=LEFT)
    op_list_frame.pack(fill=X)


    op_show_frame = Frame(top);
    show_op = Button(op_show_frame, text="OP show.", command = lambda:optional_show());
    show_op.pack(side=LEFT)
    write_op = Button(op_show_frame, text="OP write back.", command = lambda:op_write());
    write_op.pack(side=LEFT);
    op_show_frame.pack(fill=X);

    empty3 = Frame(top);
    Label(empty3, text=spl1).pack(fill=X);
    empty3.pack();
    
    modify_frame = Frame(top)
    check_incorr_btn = Button(modify_frame, text = 'Check type', command = lambda: check_type());
    check_incorr_btn.pack(side=LEFT) 
##    ck_all_com = Button(modify_frame, text='check ALL Component Name except R& C', command=lambda:design.check_difference('', 'cn', True));
##    ck_all_com.pack(side=LEFT);
    ck_all_pn = Button(modify_frame, text = 'Check ALL Part Number except R& C', command = lambda: check_diff('', 'pn', True));
    ck_all_pn.pack(side=LEFT)   
    modify_btn = Button(modify_frame, text="PN, Desp write back.", command=lambda:modify(''))
    modify_btn.pack(side=RIGHT);
    modify_frame.pack(fill=X)
    
    mlcc_frame = Frame(top);
    #ck_mlcc_pn = Button(mlcc_frame, text='Check CAP PN!', command=lambda:design.check_mlcc_by_PN());
    #ck_mlcc_pn.pack(side=LEFT);
    ck_mlcc_size = Button(mlcc_frame, text='check CAP size!', command=lambda:check_diff('mlcc', 'size'));
    ck_mlcc_size.pack(side=LEFT);
    ck_mlcc_value = Button(mlcc_frame, text='check CAP value!', command=lambda:check_diff('mlcc', 'value'));
    ck_mlcc_value.pack(side=LEFT);
    ck_mlcc_pn = Button(mlcc_frame, text='check CAP PN!', command=lambda:check_diff('mlcc', 'pn'));
    ck_mlcc_pn.pack(side=LEFT);
    mlcc_y5v = Button(mlcc_frame, text='Check Y5V mlcc', command = lambda:check_y5v());
    mlcc_y5v.pack(side=LEFT);
    modify_mlcc = Button(mlcc_frame, text='Modify All SCH CAP by BOM PN', command = lambda:modify('mlcc'));
    modify_mlcc.pack(side=RIGHT);
    mlcc_frame.pack(fill=X)

    res_frame = Frame(top);
    #ck_res_pn = Button(res_frame, text='Check RES PN!', command=lambda:design.check_res_by_PN());
    #ck_res_pn.pack(side=LEFT);
    ck_res_size = Button(res_frame, text='check RES size!', command=lambda:check_diff('res', 'size'));
    ck_res_size.pack(side=LEFT);
    ck_res_value = Button(res_frame, text='check RES value!', command=lambda:check_diff('res', 'value'));
    ck_res_value.pack(side=LEFT);
    ck_res_pn = Button(res_frame, text='check RES PN!', command=lambda:check_diff('res', 'pn'));
    ck_res_pn.pack(side=LEFT);
    res = Button(res_frame, text='Modify All SCH RES by BOM PN', command = lambda:modify('res'));
    res.pack(side=RIGHT);
    res_frame.pack(fill=X)

    induc_frame = Frame(top)
    lpn = Label(induc_frame, text='PN level:(ex: 02G, 06G)')
    lpn.pack(side=LEFT);
    lent = Entry(induc_frame, width=20)
    lent.pack(side=LEFT)
    list_inductor_btn = Button(induc_frame, text='List by PN', command=lambda:lst_by_PN(lent.get()));
    list_inductor_btn.pack(side=LEFT)
    induc_frame.pack(fill=X)

    empty4 = Frame(top);
    Label(empty4, text=spl1).pack(fill=X);
    empty4.pack();


    ####################################################################################
    export_frame = Frame(top);
    exp_out = Button(export_frame, text="Export EXP.", command = lambda:design.EXP_out());
    exp_out.pack(side=RIGHT);

    wendi = Label(export_frame, text="     Wendi Cheng ... ... #38725  ");
    

    clear_design = Button(export_frame, text="Clear!", command = lambda:design.clear());
    clear_design.pack(side=LEFT)
    wendi.pack(side=LEFT);
    
    export_frame.pack(fill=X)


    empty5 = Frame(top);
    Label(empty5, text=spl2).pack(fill=X);
    empty5.pack();
    
    top.mainloop()

if __name__ == "__main__":
    main();


    
