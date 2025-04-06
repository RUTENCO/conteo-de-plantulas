# Parámetros del rastreo
# Diccionario para almacenar los objetos rastreados. Cada objeto tiene un ID único.
object_tracker = {}
object_id = 0  # ID inicial para los objetos nuevos.
# Número máximo de frames que un objeto puede no ser detectado antes de considerarlo desaparecido.
max_disappear_frames = 30
plant_count = 0  # Contador de plantas que han cruzado la línea de conteo.


def track(centroids, line_x, line_thickness):
    """
    Función para rastrear los objetos detectados a través de diferentes frames.

    Args:
    - centroids: Lista de tuplas (cx, cy) con las coordenadas del centroide de cada objeto detectado en el frame actual.
    - line_x: Posición horizontal de la línea de conteo en píxeles.
    - line_thickness: El grosor de la línea de conteo en píxeles.

    Returns:
    - plant_count: Número total de plantas que han cruzado la línea de conteo.
    - object_tracker: Diccionario actualizado con los objetos rastreados.
    """

    global plant_count, object_tracker, object_id

    # Crear un nuevo diccionario para almacenar el rastreo actualizado de objetos.
    new_tracker = {}

    # Para cada centroide detectado, intentamos encontrar el objeto que podría estar asociado a este.
    for i, (cx, cy) in enumerate(centroids):
        # Variable para almacenar el ID de un objeto rastreado coincidente.
        matched_id = None

        # Buscar en los objetos rastreados existentes para encontrar un objeto cercano al nuevo centroide.
        for oid, data in object_tracker.items():
            tracked_cx, tracked_cy = data["centroid"]
            # Comprobar si la distancia entre el centroide rastreado y el nuevo es pequeña (en un radio de 25 píxeles).
            if ((tracked_cx - cx)**2 + (tracked_cy - cy)**2) < 25**2:
                # Si hay coincidencia, guardamos el ID del objeto.
                matched_id = oid
                break

        # Si encontramos un objeto cercano, lo actualizamos en el nuevo rastreo.
        if matched_id is not None:
            new_tracker[matched_id] = {
                "id": matched_id,
                "idx": i,
                "centroid": (cx, cy),
                # Mantener si ya cruzó la línea.
                "crossed": object_tracker[matched_id]["crossed"],
                # Resetear el contador de frames sin ver.
                "frames_since_seen": 0,
            }
        else:
            # Si no encontramos coincidencia, asignamos un nuevo ID al objeto y lo añadimos al rastreo.
            new_tracker[object_id] = {
                "id": object_id,
                "idx": i,
                "centroid": (cx, cy),
                "crossed": False,  # Inicialmente no ha cruzado la línea.
                # El objeto ha sido visto en este frame.
                "frames_since_seen": 0}
            object_id += 1  # Incrementar el ID para el siguiente objeto nuevo.

    # Comprobar objetos que no fueron encontrados en el nuevo rastreo, indicándonos que han desaparecido.
    for oid, data in object_tracker.items():
        if oid not in new_tracker:
            # Aumentar el contador de frames sin ver.
            data["frames_since_seen"] += 1
            # Si el objeto ha desaparecido durante más de `max_disappear_frames`, no lo actualizamos en el nuevo rastreo.
            if data["frames_since_seen"] < max_disappear_frames:
                # Mantener el objeto en el rastreo pero con el contador incrementado.
                new_tracker[oid] = data

    # Verificar si los objetos han cruzado la línea de conteo. Si no lo han hecho, y cruzan la línea, actualizar.
    for oid, data in new_tracker.items():
        cx, cy = data["centroid"]
        # Si el objeto no ha cruzado la línea y está lo suficientemente cerca de ella, lo marcamos como cruzado.
        if not data["crossed"] and abs(cx - line_x) <= line_thickness:
            # El objeto ha cruzado la línea.
            new_tracker[oid]["crossed"] = True
            plant_count += 1  # Incrementamos el contador de plantas.

    # Actualizar el rastreo global con los nuevos datos.
    object_tracker = new_tracker

    # Devolver el contador de plantas y el rastreo actualizado.
    return plant_count, object_tracker