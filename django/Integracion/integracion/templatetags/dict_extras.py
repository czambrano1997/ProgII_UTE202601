from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        val = dictionary.get(key, '')
        # Si un campo relacional de Odoo devuelve [id, "nombre"], mostramos solo el nombre
        if isinstance(val, (list, tuple)) and len(val) == 2:
            return val[1]
        return val
    return ''