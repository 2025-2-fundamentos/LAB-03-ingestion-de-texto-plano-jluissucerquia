"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben estar en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    import pandas as pd

    filas = []

    with open("files/input/clusters_report.txt", encoding="utf-8") as f:
        lineas = f.readlines()

    # Saltar encabezado (primeras 4 líneas)
    lineas = lineas[4:]

    actual = None

    for linea in lineas:
        stripped = linea.strip()

        # Línea en blanco → cerramos cluster actual (si existe)
        if not stripped:
            if actual is not None:
                texto = " ".join(actual["keys"])
                # Normalizar espacios internos a un solo espacio
                texto = " ".join(texto.split())
                # Quitar punto final si lo hay
                if texto.endswith("."):
                    texto = texto[:-1]
                actual["principales_palabras_clave"] = texto
                del actual["keys"]
                filas.append(actual)
                actual = None
            continue

        # Línea de guiones → ignorar
        if stripped.startswith("-"):
            continue

        partes = stripped.split()

        # Si la primera "palabra" es un número → nueva fila
        if partes[0].isdigit():
            # Cerrar el cluster anterior si estaba abierto
            if actual is not None:
                texto = " ".join(actual["keys"])
                texto = " ".join(texto.split())
                if texto.endswith("."):
                    texto = texto[:-1]
                actual["principales_palabras_clave"] = texto
                del actual["keys"]
                filas.append(actual)

            actual = {
                "cluster": int(partes[0]),
                "cantidad_de_palabras_clave": int(partes[1]),
                "porcentaje_de_palabras_clave": float(partes[2].replace(",", ".")),
                "keys": [" ".join(partes[4:])],
            }
        else:
            # Línea de continuación: solo palabras clave
            actual["keys"].append(stripped)

    # Por si el último cluster no terminó en línea en blanco
    if actual is not None:
        texto = " ".join(actual["keys"])
        texto = " ".join(texto.split())
        if texto.endswith("."):
            texto = texto[:-1]
        actual["principales_palabras_clave"] = texto
        del actual["keys"]
        filas.append(actual)

    return pd.DataFrame(filas)