"""socialMedia additional_templates.py

This script defines extensions to django template language
Author: Desmond, Akshita and Sok Ee 
"""

from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    """ This function allows for obtaining value in a dictionary through its keys.
    """
    return dictionary.get(key)