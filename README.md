# AgroDataLab Web

- Web: https://agrodatalab-web.onrender.com/
- Enlace vídeo (Youtube): https://youtu.be/OabzghwdXr0

## Descripción

EnviroPro es una aplicación web desarrollada con Django para la gestión, análisis y visualización de datos ambientales procedentes de sensores IoT.

## Objetivos del proyecto

- Monitorizar variables ambientales en tiempo real o por lotes
- Detectar anomalías en humedad, temperatura y energía
- Generar alertas automáticas según umbrales definidos
- Proporcionar recomendaciones asociadas a cada alerta
- Visualizar datos mediante un dashboard interactivo

## Tecnologías utilizadas

- Python 3
- Django
- Pandas
- Bootstrap 5
- Chart.js
- SQLite (desarrollo)
- Gunicorn (deploy)
- Render (hosting)

## Estructura del proyecto
AgroDataLab_Web/
- dashboard/
- enviropro/
- alerts/
- imports/
- users/
- manage.py
- requirements.txt

## Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/JuanCCCF/agrodatalab-web.git

# 2. Entrar al proyecto
cd AgroDataLab_Web

# 3. Crear entorno virtual
python -m venv venv

# 4. Activar entorno
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Migraciones
python manage.py migrate

# 7. Ejecutar servidor
python manage.py runserver
```

## Notas
- Límite de 1000 filas por importación (restricción de memoria en hosting gratuito)
- Optimizado para Render Free Tier

## Autores
- Jesús Ruiz Borruecos
- Juan Ruiz Pérez

**Curso:** Curso de Especialización en Desarrollo de aplicaciones en lenguaje Python
**Centro:** IES Trassierra (Córdoba)

## Despliegue
Proyecto desplegado en Render:
https://agrodatalab-web.onrender.com/
