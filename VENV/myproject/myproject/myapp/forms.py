# -*- coding: utf-8 -*-

from django import forms


class DocumentForm(forms.Form):
    #docfile = forms.FileField(
    #    label='select file',        
    #    widget=forms.ClearableFileInput(attrs={'multiple': True}))
    BOM_59t = forms.FileField(
        label='59T BOM',        
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    BOM_59b = forms.FileField(
        label='59B BOM',        
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    BOM_70 = forms.FileField(
        label='70 BOM',        
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    EXP = forms.FileField(
        label='EXP',        
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    CMP = forms.FileField(
        label='CMP',        
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
