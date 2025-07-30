from django import template

register = template.Library()

@register.filter
def ulify(text):
    """
    Convierte un bloque de texto con saltos de línea en una lista HTML <ul>.
    Cada línea no vacía se convierte en un elemento <li>.
    """
    if not text:
        return ''
    # Separa el texto en líneas, quitando espacios en blanco
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ''
    # Envuelve cada línea en una etiqueta <li>
    list_items = ''.join(['<li>{}</li>'.format(line) for line in lines])
    # Envuelve la lista de elementos en <ul>
    return '<ul>{}</ul>'.format(list_items)

@register.filter
def olify_reversed(text):
    """
    Convierte un bloque de texto con saltos de línea en una lista HTML <ol> enumerada inversamente.
    Cada línea no vacía se convierte en un elemento <li>.
    """
    if not text:
        return ''
    # Separa el texto en líneas y elimina espacios en blanco
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ''
    # Envuelve cada línea en una etiqueta <li>
    list_items = ''.join(f'<li>{line}</li>' for line in lines)
    # Devuelve la lista completa dentro de una etiqueta <ol> con el atributo reversed
    return f'<ol reversed>{list_items}</ol>'

@register.filter
def split(value, sep=","):
    return value.split(sep)

@register.filter
def strip(value):
    """Elimina espacios en blanco al inicio y al final de la cadena."""
    return value.strip()


@register.filter
def is_directivo(label):
    return any(keyword in label for keyword in ["Director", "Decano", "Jefe"])

@register.filter
def is_apoyo(label):
    return any(keyword in label for keyword in ["Secretario", "Tutor"])

@register.filter
def is_otro(label):
    return not is_directivo(label) and not is_apoyo(label)

@register.filter
def tiene_cargo(academico, nombre):
    return academico.tiene_cargo(nombre)
