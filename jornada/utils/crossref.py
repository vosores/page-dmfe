import requests

def formatear_autores_apa7(autores_raw):
    autores_formateados = []

    for autor in autores_raw:
        apellido = autor.get("family", "").strip()
        nombres = autor.get("given", "").strip().split()
        iniciales = " ".join(f"{n[0]}." for n in nombres if n)
        if apellido:
            autores_formateados.append(f"{apellido}, {iniciales}")

    if len(autores_formateados) > 1:
        return ", ".join(autores_formateados[:-1]) + " & " + autores_formateados[-1]
    elif autores_formateados:
        return autores_formateados[0]
    else:
        return ""

def obtener_datos_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        metadata = data.get("message", {})

        autores_raw = metadata.get("author", [])
        autores = formatear_autores_apa7(autores_raw)

        return {
            "titulo": metadata.get("title", [""])[0],
            "autores": autores,
            "revista": metadata.get("container-title", [""])[0],
            "anio": metadata.get("issued", {}).get("date-parts", [[None]])[0][0],
            "doi": metadata.get("DOI", ""),
        }
    except requests.RequestException as e:
        print(f"Error al consultar Crossref: {e}")
        return None
