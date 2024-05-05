from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def getFirstChar(value): 
    return value[0]

@register.filter
def checkLen(value, l):
    if(len(value) == l): 
        return True
    
    return False 

@register.filter
def is_empty(x): 
    if x is None: 
        return True

    return False