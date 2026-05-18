from alerts.models import Alert, Recommendation

def detectar_alertas(record):

    base_query = Alert.objects.filter(fecha=record.fecha)

    # SEQUEDAD
    if record.humedad_media < 10 and record.humedad_media > 8:
        if not base_query.filter(tipo="Sequedad").exists():

            alert = Alert.objects.create(
                fecha=record.fecha,
                tipo="Sequedad",
                nivel="alto",
                descripcion="Humedad del suelo demasiado baja",
                variable_afectada="humedad"
            )

            Recommendation.objects.create(
                alerta=alert,
                titulo="Activar riego",
                descripcion="Nivel de humedad crítico, regar inmediatamente",
                prioridad="alta",
                estado="pendiente"
            )

    # BATERÍA (CORREGIDO MV)
    bateria = record.bateria

    # NORMALIZACIÓN
    if bateria > 50:
        bateria = bateria / 1000

    # ALERTA
    if bateria < 6.00:

        if not base_query.filter(tipo="Energía baja").exists():

            alert = Alert.objects.create(
                fecha=record.fecha,
                tipo="Energía baja",
                nivel="critico",
                descripcion=f"Batería baja: {record.bateria} mV",
                variable_afectada="bateria"
            )

            Recommendation.objects.create(
                alerta=alert,
                titulo="Revisar sistema solar",
                descripcion="Posible falta de carga en panel o batería degradada",
                prioridad="alta",
                estado="pendiente"
            )

    # TEMPERATURA
    if record.temp_max - record.temp_min > 15 and record.temp_max - record.temp_min > 10:

        if not base_query.filter(tipo="Temperatura incoherente").exists():

            alert = Alert.objects.create(
                fecha=record.fecha,
                tipo="Temperatura incoherente",
                nivel="medio",
                descripcion="Gran diferencia térmica detectada",
                variable_afectada="temperatura"
            )

            Recommendation.objects.create(
                alerta=alert,
                titulo="Revisar sensores",
                descripcion="Posible fallo o desajuste en sensores",
                prioridad="media",
                estado="pendiente"
            )
