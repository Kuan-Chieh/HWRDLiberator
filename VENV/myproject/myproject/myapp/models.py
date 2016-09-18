# -*- coding: utf-8 -*-
from django.db import models
import os
#import datetime
#from test import test123

def user_directory_path(instance, filename):
    return os.path.join('Session', str(instance.session.id), str(filename))


class Document(models.Model):
    #@classmethod
    #def path(cls):
        #return 'Session\\%r' % cls.session.id
    session = models.ForeignKey('Session',
                                on_delete = models.CASCADE,
                                related_name = 'file',
                                )
    file_type = models.TextField()
    docfile = models.FileField(upload_to=user_directory_path)
    def filename(self):
        return os.path.basename(self.docfile.name)
    #def Change_path(self):
    #    self.docfile.upload_to = 'Session\\%r' % self.session.id


        
class Session(models.Model):
    DateTime = models.DateTimeField(
                                    #auto_now = True,
                                    auto_now_add = True,)
    
    #property of SCH
    head = models.TextField(null=True,)
    #attrs = models.TextField(null=True,)
    SCH_type = models.TextField(null=True,)
    
    #key = hash(datetime.datetime.now())
    #BOM_59t = models.TextField(null=True,).
    #BOM_59b = models.TextField(null=True,)
    #BOM_70 = models.TextField(null=True,)
    #EXP = models.TextField(null=True,)
    #CMP = models.TextField(null=True,)
    def __unicode__(self):
        return '%s' % self.id

class Element(models.Model):
    session = models.ForeignKey('Session',
                                on_delete = models.CASCADE,
                                related_name = 'elements',
                                )
    loca = models.TextField()

    # property of SCH
    op = models.BooleanField(default = False)

    #property of BOM
    #BOM_PN = models.TextField()
    #
    BOM = models.ForeignKey('BOM',
                            on_delete = models.CASCADE,
                            related_name = 'elements',
                            null = True
                            )
    BOM_type = models.TextField(null=True,)
    
    def __unicode__(self):
        return '%s element of Session %s'% (self.loca, self.session.id)

class BOM(models.Model):
    session = models.ForeignKey('Session',
                            on_delete = models.CASCADE,
                            related_name = 'BOMs',
                            )
    PN = models.TextField()
    CN = models.TextField()
    #Component Name is useless!!
    
    def __unicode__(self):
        return '%s\t%s'% (self.PN, self.CN)

class Substitute(models.Model):
    BOM = models.ForeignKey('BOM',
                            on_delete = models.CASCADE,
                            related_name = 'substitutes',
                            )
    PN = models.TextField()
    CN = models.TextField()
    def __unicode__(self):
        return '%s\t%s'% (self.PN, self.CN)


    
class Property(models.Model):
    element = models.ForeignKey('Element',
                                on_delete = models.CASCADE,
                                related_name = 'property',
                                )
    
    primary = models.BooleanField()
    #op = models.BooleamField()
    order = models.IntegerField(null = True)
    attr = models.TextField()
    value = models.TextField()
    
    def __unicode__(self):
        if self.primary:
            return ('%s[%d]: %s: %s' % (self.element.loca, self.order, self.attr, self.value))
        else:
            return ('%s[x]: %s: %s' % (self.element.loca, self.attr, self.value))

