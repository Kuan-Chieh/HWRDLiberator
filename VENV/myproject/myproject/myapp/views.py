# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

from django.core.urlresolvers import reverse
import datetime

import os


from myproject.myapp.ADesign_KC import *

from myproject.myapp.models import *
from myproject.myapp.forms import DocumentForm
import subprocess

#form_list = ['docfile', 'BOM_59t', 'BOM_59b', 'BOM_70', 'EXP', 'CMP']
designs = {}

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
            if method == 'opcheck':
                design.check_optional(page="", flag = True)
                output = design._output

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
            path = 'media\\Session\\%s'%session.id
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

                
                    
                if BOM_file:
                    #print(os.getcwd())
                    arg = '" "'.join([path + '\\' + x.filename() for x in BOM_file if x != ''])
                    arg = 'myproject\\myapp\\WASRBOM.exe "' + arg + '" ' + path + '\\wBOM.txt' + ' 2'
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
                design = ASRR(BF=path + "\\wBOM.txt", SF = SCH_file.docfile.path)
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
    
