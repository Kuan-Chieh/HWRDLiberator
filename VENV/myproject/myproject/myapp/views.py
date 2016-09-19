# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse
import datetime

import os

#from myproject.functions.ADesign_KC import *
#from myproject.myapp.ADesign_KC import *
from myproject.myapp.functions.ADesign_KC import *
#from myproject.myapp.functions import *

from myproject.myapp.models import *
from myproject.myapp.forms import DocumentForm
import subprocess

#form_list = ['docfile', 'BOM_59t', 'BOM_59b', 'BOM_70', 'EXP', 'CMP']
designs = {}

def autospace(tuple_):
    string, l = tuple_
    if len(string) > l:
        return string
    d = l - len(string)
    return ' '*(d//2) + string + ' '*(d//2+d%2)

def line(*arg):
    res = ''
    for line in arg:
        if type(line) == str:
            res += line
        else:
            res += autospace(line)
    return res         
            
def op2mes(element, op_name):
    
    op_temp = []
    for op in op_name:
        op_temp.append(element[op])
    return '|'.join(op_temp)

def upload(request):
    
    form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def SBSYNC(request):
    # Handle file upload
    if request.method == 'POST':
        
        if "method" in request.POST:
            method = request.POST["method"]
            ID = request.POST["ID"]
            design = designs[int(ID)]
            output = []
            
            page_key = design.SCH.get_page_key()
            op_name = design.SCH.get_op_name()
            key_name = design.SCH.getkey()
            
            if method == 'opcheck':
                #unset_op, set_op, BOM = design.check_optional(page, True)
                unset_op, set_op, BOM = design.check_optional('', True)
                Both = design.SCH.get_from_keys(unset_op[1])
                SCH = design.SCH.get_from_keys(set_op[1])
                output += [line(('Page', 35),
                                '-----',
                                ('SCH Optional', 17),
                                '<<<',
                               ('Location/description', 19),
                                '>>>   BOM    -----'),
                           '*'*122]
                           
    
                for element in Both:
                    page_info = element[page_key]
                    mes = op2mes(element, op_name)

                    output += [line((page_info, 35),
                                    '-----',
                                    (mes, 17),
                                    '===',
                                    line('"'+ element[key_name] + '"', 19),
                                    ">>>    Y     -----")]
                output += ['='*122]
                
                for element in SCH:
                    page_info = element[page_key]
                    mes = op2mes(element, op_name)
                    output += [line((page_info, 35),
                                    '-----',
                                    (mes, 17),
                                    '<<<',
                                    ('"'+ element[key_name] + '"', 19),
                                    "===    N     -----")
                               ]
                output += ['#'*122, 'Locations cannot find in SCH:']
        
                
                for element in BOM:
                    BOM_part_name = design.BOM.get_from_key(part, self.BOM.get_locations())
                    BOM_element = self.BOM.get_from_key(BOM_part_name)
                    
                    output += ' '.join([BOM_part_name,
                                        element,
                                        BOM_element['Component_Name']])
                
                output += ['',
                           '-'*22+'Result'+'-'*22,
                           'Elements on SCH and BOM:',
                           'Incorresponding elements/ Total elements: %d/ %d'%(len(unset_op[1]),
                                                                           len(unset_op[1])+len(unset_op[0])),
                           '',
                           'Elements on SCH but not in BOM:',
                           'Incorresponding elements/ Total elements: %d/ %d'%(len(set_op[1]),
                                                                           len(set_op[1])+len(set_op[0])),
                           '',
                           'Subtotal elements: %d'% (len(unset_op[1])+len(unset_op[0])+len(set_op[1])+len(set_op[0])),
                           '',
                           'Elements on BOM but not SCH:',
                           len(BOM),
                           '-'*122,
                           ]
        
##
##
##                design.check_optional(page="", flag = True)
##                output = design._output




                

            elif method == 'check_PN':
                
                design.check_difference('', 'pn')
                output = design._output
            elif method == 'Check type':
                design.check_incor()
                output = design._output
            else:
                output = 'YA'
            
            
            
        else:
            method = ''
            #form = DocumentForm(request.POST, request.FILES)
            session = Session(DateTime = datetime.datetime.now())
            session.save()
            path = os.path.join('media', 'Session', str(session.id))
            files = request.FILES
            #path = 'Session\\%s' % session.id
            for file_type in files:
                
                newdoc = Document(session = session,
                                  #path = path,
                                  file_type = file_type,#EXP, BOM, CMP,
                                  docfile=request.FILES[file_type])
                #newdoc.docfile.path = path
                
                newdoc.save()
            #return  HttpResponse('sdytfuiho')
            BOM_file = session.file.filter(file_type__contains = 'BOM').order_by('file_type')
            SCH_file = session.file.filter(file_type = 'EXP')
            
            if BOM_file or SCH_file:

                
                wBOM_path = os.path.join(path, "wBOM.txt")
                if BOM_file:
                    #print(os.getcwd())
                    arg = '" "'.join([os.path.join(path, x.filename())
                                      for x in BOM_file if x != ''])
                    wBOM_parser_path = os.path.relpath(os.path.join(os.path.dirname(__file__), 'functions', 'WASRBOM.exe'), os.getcwd())
                    arg = wBOM_parser_path + ' "' + arg + '" ' + wBOM_path + ' 2'
                    print(arg)
                    subprocess.call(arg)
                    flag_b = 'bom OK'
                else:
                    flag_b = 'no bom'
                    
                
                
                if SCH_file:
                    flag_s = 'SCH OK'
                    SCH_file = SCH_file[0]
                else:
                    flag_s = 'no SCH'
                ID = session.id 
                design = ASRR(BF= wBOM_path, SF = SCH_file.docfile.path)
                designs[ID] = design
                    #SCH_file = SCH_file[0]
                    #return HttpResponse('QQ')

                design.parser_init()
                #output = 'SBSYNC: %d -- %d'%(len(design.SCH._elements), len(designs))
                output = '%s\n%s\n%s'%(str(ID), flag_b, flag_s)
            else:
                output = "QQ"

        functions = ['opcheck', 'check_PN', 'Check type']

        return render_to_response(
            'SBSYNC.html',
            {'method': method, 'output': output, 'functions': functions, 'ID': ID},
            context_instance=RequestContext(request)
            )
    else:
        return HttpResponseRedirect(reverse('myproject.myapp.views.upload'))
    
