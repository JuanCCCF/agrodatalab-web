from django.shortcuts import render, redirect
import pandas as pd
import io
from dateutil import parser
from enviropro.models import EnviroProRecord
from alerts.models import Alert, Recommendation
from enviropro.utils import detectar_alertas
from django.utils import timezone
from django.contrib import messages

"""
Vista de importación de archivos CSV.

Este módulo permite la carga y procesamiento de datos ambientales
procedentes de archivos CSV subidos por el usuario a través de la web.

Funcionalidades principales:
- Subida de archivos CSV desde la interfaz web.
- Detección automática del formato del CSV.
- Limpieza y normalización de datos.
- Creación de registros en la base de datos.
- Generación automática de alertas tras la importación.

El sistema es capaz de trabajar con dos tipos de CSV:
1. Datos de sensores (8 sondas individuales).
2. Datos diarios ya agregados (resúmenes).
"""

def import_view(request):

    has_data = EnviroProRecord.objects.exists()

    if request.method == "POST":

        # Obtener el archivo CSV
        file = request.FILES["csv_file"]

        if not file:
            messages.error(request, "No has seleccionado ningún archivo CSV")
            return redirect("import_data")

        # Lectura del CSV
        df = pd.read_csv(
            io.StringIO(file.read().decode("utf-8-sig")),
            sep=None,
            engine="python"
        )

        # Límite de filas --> Solo se cargarán las primeras 2000 filas, ya que la versión free de la web no soporta más RAM
        if len(df) > 2000:
            df = df.head(2000)

            messages.warning(
                request,
                f"Archivo subido correctamente. Se han procesado {len(df)} filas (limitado a 2000 por restricciones del sistema)."
            )

        # Limpiar nombres de las columnas
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace("\ufeff", "")

        columnas = set(df.columns)

        # Detectar automáticamente el tipo de CSV
        csv_sensores = "humedad_s1_media" in columnas
        csv_diario = "humedad_media_diaria" in columnas

        # Función auxiliar
        # Convierte valores a float de forma segura
        def safe_float(x):
            try:
                if x is None:
                    return 0.0
                x = str(x).strip()
                if x in ["", "nan", "None"]:
                    return 0.0
                return float(x.replace(",", "."))
            except:
                return 0.0

        # Importación de filas del CSV
        for _, row in df.iterrows():

            # Detectar fecha en ambos formatos
            fecha = pd.to_datetime(
                row.get("fecha"),
                errors="coerce"
            )

            # Si no existe, intentar con fecha_hora
            if pd.isna(fecha):
                fecha = pd.to_datetime(
                    row.get("fecha_hora"),
                    errors="coerce"
                )

            # Si no hay fecha válida --> ignorar fila
            if pd.isna(fecha):
                continue

            # Convertir a fecha con zona horaria Django
            fecha = fecha.to_pydatetime()
            fecha = timezone.make_aware(fecha, timezone.get_current_timezone())

            # CSV Tipo sensores (8 sondas individuales)
            if csv_sensores:

                hums = [
                    safe_float(row.get(f"humedad_s{i}_media"))
                    for i in range(1, 9)
                ]
                humedad_media = sum(hums) / 8

                temps = [
                    safe_float(row.get(f"temp_s{i}_media"))
                    for i in range(1, 9)
                ]

                temp_media = sum(temps) / 8
                temp_max = max(temps)
                temp_min = min(temps)

                bateria = safe_float(row.get("bateria_mv"))
                panel = safe_float(row.get("panel_solar_mv"))
            
            # CSV Tipo diario (datos ya agregados)
            elif csv_diario:

                humedad_media = safe_float(
                    row.get("humedad_media_diaria")
                )

                temp_media = safe_float(
                    row.get("temp_suelo_media_diaria")
                )

                temp_max = safe_float(
                    row.get("temp_suelo_max_diaria")
                )

                temp_min = safe_float(
                    row.get("temp_suelo_min_diaria")
                )

                bateria = safe_float(
                    row.get("bateria_media_v")
                )

                panel = safe_float(
                    row.get("panel_solar_medio_v")
                )

            else:
                # Formato CSV desconocido --> ignorar
                continue

            # Crear registro en la base de datos
            record = EnviroProRecord.objects.create(
                fecha=fecha,
                humedad_media=humedad_media,
                temp_suelo=temp_media,
                temp_max=temp_max,
                temp_min=temp_min,
                bateria=bateria,
                panel_solar=panel,
                observaciones=""
            )

            # Generar alertas automáticamente
            detectar_alertas(record)

        return redirect("registros")

    return render(request, "imports/import.html", {
        "has_data": has_data
    })

# Eliminar todos los datos del sistema
def reset_data(request):
    if request.method == "POST":
        EnviroProRecord.objects.all().delete()
        Alert.objects.all().delete()
        Recommendation.objects.all().delete()

        messages.success(request, "Datos eliminados correctamente")

        # Redirigir después de POST
        return redirect("import_data")

    # Si alguien entra por GET --> Se manda a confirmación
    return redirect("reset_import_confirm")


def reset_import_confirm(request):
    return render(request, "imports/reset_import_confirm.html")