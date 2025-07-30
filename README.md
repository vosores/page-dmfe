# Proyecto Django con WeasyPrint

Este proyecto utiliza Django junto con [WeasyPrint](https://weasyprint.org/) para generar documentos PDF directamente desde plantillas HTML.

---

## ⚙️ Requisitos del sistema

Antes de instalar los paquetes de Python, asegúrate de tener estas dependencias del sistema (Linux Debian/Ubuntu):

```bash
sudo apt update && sudo apt install -y     libpango1.0-0     libpangocairo-1.0-0     libcairo2     libgdk-pixbuf2.0-0     libffi-dev     libjpeg-dev     libxml2     libxml2-dev     libxslt1-dev     zlib1g-dev
```

---

## 📦 Instalación de entorno Python

1. Crear y activar un entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependencias Python:

```bash
pip install -r requirements.txt
```

Contenido de `requirements.txt`:

```
Django
WeasyPrint
jinja2
cairocffi
tinycss2
cssselect2
Pyphen
fonttools
requests
```

---

## 🧪 Cómo generar un PDF

Dentro de tu vista de Django puedes usar:

```python
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse

def generar_pdf(request):
    html_string = render_to_string("mi_template.html", {"contexto": "aquí"})
    pdf_file = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="documento.pdf"'
    return response
```

---

## 📝 Notas

- Asegúrate de que tus rutas relativas en CSS (por ejemplo fuentes o imágenes) sean absolutas o usen `base_url` al generar el HTML.
- WeasyPrint renderiza mejor con estilos CSS bien estructurados y sin JavaScript dinámico.

---

¡Listo! Puedes personalizar el template HTML para generar diplomas, informes, CVs u otros documentos en PDF directamente desde Django.