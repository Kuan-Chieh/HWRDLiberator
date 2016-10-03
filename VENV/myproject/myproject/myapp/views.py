# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse
import datetime

import os

#from myproject.functions.ADesign_KC import *
#from myproject.myapp.ADesign_KC import *
#from myproject.myapp.functions.ADesign_KC import *
from myproject.myapp.functions.SBSYNC_KC import *
#from myproject.myapp.functions import *

from myproject.myapp.models import *
from myproject.myapp.forms import DocumentForm
import subprocess

#form_list = ['docfile', 'BOM_59t', 'BOM_59b', 'BOM_70', 'EXP', 'CMP']
designs = {}
f = functions()

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

    def decode(attrs, values):
        i = 0
        res = {}
        while i < len(attrs) and attrs[i] != '':
            res[attrs[i]] = values[i]
            i+=1
        return res
    
    # Handle file upload
    if request.method == 'POST':
        
        if "method" in request.POST:
            ID = request.POST["ID"]
            f.var_init(designs[int(ID)])
            method = request.POST["method"]
    
            kwarg = decode(request.POST["var_name"].split('|'),
                         request.POST["var"].split('|'))
            if request.POST["input_name"] != '':
                kwarg[request.POST["input_name"]] = request.POST["input"]
            #design = designs[int(ID)]
            output = getattr(f, method)(**kwarg).split('\n')
            
##            if method == 'opcheck':
##                
##                #design = designs[int(ID)]
##
##                #output = op_check(page)
##                output = f.op_check('').split('\n')
##                
##            elif method == 'check_PN':
##                
##                #design.check_difference('', 'pn')
##                #output = design._output
##                pass
##            elif method == 'Check type':
##                #design.check_incor()
##                #output = design._output
##                pass
##            else:
##                output = 'YA'
            
            
            
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

        #functions_name = ['opcheck', 'check_PN', 'Check type']
        
##        class f_dir():
##            def __init__(self, Name, func, var = [], input_f = None):
##                self.name = Name
##                self.func = func
##                self.var = var
##                self.input_f = input_f
##            def get(self, attr):
##                return getattr(self, attr)
        
        def f_dir(Name, func, var_name = [], var = [], input_name = '', input_des = ''):
            var_name_s = '|'.join(var_name)
            var_s = '|'.join(var)                
            return {'name': Name, 'func': func, 'var_name': var_name_s, 'var': var_s, 'input_name': input_name, 'input_des': input_des}
        
        functions = [f_dir('Optional_Check', 'op_check', input_name = 'page', input_des = 'Page'),
                     f_dir('list_by_op', 'lst_by_op', input_name = 'opt', input_des = 'Option'),
                     
                     f_dir('OP_show.', 'optional_show'),
                     f_dir('OP_write back.', 'op_write'),
                     
                     f_dir('Check_type', 'check_type'),
                     f_dir('Check_ALL_Part_Number_except_R&C', 'check_diff',
                           ['check_type', 'flag', 'except_R_C'], ['', 'pn', 'True']),
                     f_dir('Modify_All_SCH_CAP_by_BOM_PN', 'modify',
                           ['cor_type'], ['']),
                     
                     f_dir('check_CAP_size!', 'check_diff',
                           ['check_type', 'flag'], ['mlcc', 'size']),
                     f_dir('check_CAP_value!', 'check_diff',
                           ['check_type', 'flag'], ['mlcc', 'value']),
                     f_dir('check_CAP_PN!', 'check_diff',
                           ['check_type', 'flag'], ['mlcc', 'pn']),
                     f_dir('Check_Y5V_mlcc', 'check_y5v'),
                     f_dir('Modify_All_SCH_CAP_by_BOM_PN',
                           'modify',['cor_type'], ['mlcc']),

                     f_dir('check_RES_size!', 'check_diff',
                           ['check_type', 'flag'], ['res', 'size']),
                     f_dir('check_RES_value!', 'check_diff',
                           ['check_type', 'flag'], ['res', 'value']),
                     f_dir('check_RES_PN!', 'check_diff',
                           ['check_type', 'flag'], ['res', 'pn']),
                     f_dir('Modify_All_SCH_RES_by_BOM_PN', 'modify',
                           ['cor_type'], ['res']),

                     f_dir('List_by_PN', 'lst_by_PN', input_name = 'PN', input_des = 'PN level')

                     ]

                          

        return render_to_response(
            'SBSYNC.html',
            {'method': method, 'output': output, 'functions': functions,
             'test': [{'name': 'qwe'}], 'ID': ID},
            context_instance=RequestContext(request)
            )
    else:
        return HttpResponseRedirect(reverse('myproject.myapp.views.upload'))
    
