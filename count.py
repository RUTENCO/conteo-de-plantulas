"""
Autores:
    Sneyder Buitrago González
    Daniel Ramírez Cárdenas
Descripción:
    Este código realiza el conteo de plántulas en un video grabado con la cámara moviéndose de derecha a izquierda,
    mientras que las plántulas se mueven de izquierda a derecha.
    El algoritmo rastrea las plántulas y las cuenta cuando cruzan una línea de conteo
Uso:
    Instalar tanto opencv como numpy y Ejecutar:

    python count.py <video>
"""

import cv2 as cv
import numpy as np
import sys
from tracker import track  # Función externa para realizar el seguimiento de objetos


# Función para calcular la máscara de la imagen usando el espacio de color LAB
def compute_mask(frame):
    # Convertir la imagen de BGR a LAB (espacio de color que separa la luminancia de los canales cromáticos)
    lab = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
    # Aplicar un umbral de Otsu sobre el canal 'a' para segmentar la imagen
    _, mask = cv.threshold(lab[:, :, 1], 0, 255,
                           cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    return mask


# Función para realizar la transformada de distancia y segmentar el fondo
def segment_foreground(blurred):
    # Aplicar la transformada de distancia (para medir la proximidad a los bordes)
    distance_transform = cv.distanceTransform(blurred, cv.DIST_L2, 5)
    # Encontrar los componentes conectados en la imagen binarizada
    n_obj, obj_labels, stats, centroids = cv.connectedComponentsWithStats(
        blurred)
    # Normalizar la transformada de distancia para cada componente detectado
    for i in range(1, n_obj):
        distance_transform[obj_labels ==
                           i] /= distance_transform[obj_labels == i].max()

    # Umbralizar la transformada de distancia para obtener la región de fondo seguro
    _, sure_fg = cv.threshold(
        distance_transform, 0.5 * distance_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Crear el fondo seguro dilatando la imagen binarizada
    kernel = np.ones((5, 5), np.uint8)
    sure_bg = cv.dilate(blurred, kernel, iterations=3)
    # Determinar la región desconocida (donde no se sabe si es fondo o primer plano)
    unknown = cv.subtract(sure_bg, sure_fg)

    return sure_fg, unknown, distance_transform


# Función para aplicar la segmentación de objetos usando Watershed
def apply_watershed(frame, sure_fg, unknown):
    # Etiquetar los componentes conectados en la imagen de primer plano
    nlabels, markers = cv.connectedComponents(sure_fg)
    markers += 1  # Asignar un marcador único a los objetos
    markers[unknown == 255] = 0  # Marcar las regiones desconocidas como fondo
    # Aplicar el algoritmo Watershed para segmentar los objetos
    markers = cv.watershed(frame, markers)
    markers[markers == -1] = 1  # Marcar los bordes con el valor 1
    markers = np.uint8(markers)

    # Convertir la imagen de marcadores a binaria
    binary = markers.copy()
    binary[binary > 1] = 255
    binary[binary <= 1] = 0
    return binary, markers


# Función para dibujar los objetos detectados en el frame
def draw_objects(frame, object_tracker, plant_count):
    # Iterar sobre los objetos rastreados y dibujar los resultados
    for id, data in object_tracker.items():
        if data["frames_since_seen"] == 0:  # Solo si el objeto está visible en el frame
            label = data["id"]
            x, y = data["centroid"]
            x, y = int(x), int(y)
            label_pos = x + 32, y - 32
            b, g, r = (255, 255, 255)
            # Dibujar un marcador para el objeto (rojo si cruzó la línea, morado si no)
            cv.drawMarker(frame, (x, y), (0, 0, 255) if data["crossed"] else
                          (255, 0, 255), cv.MARKER_TRIANGLE_UP, 16, 4)

    # Dibujar la línea de conteo en el frame (como una línea vertical en la posición especificada)
    line_x = int(frame.shape[1] * line_position)
    cv.line(frame, (line_x, 0),
            (line_x, frame.shape[0]), (255, 0, 0), line_thickness)

    # Mostrar el número de plantas contadas en el frame
    cv.putText(frame, f"""Plantas contadas: {
               plant_count}""", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 8)
    cv.putText(frame, f"""Plantas contadas: {
               plant_count}""", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

    return frame


# Función principal para procesar cada frame del video
def process_frame(frame):
    frame = frame.copy()  # Hacer una copia del frame para no modificar el original

    # Calcular la posición de la línea de conteo en píxeles
    line_x = int(frame.shape[1] * line_position)

    # Paso 1: Calcular la máscara de la imagen para segmentar el objeto
    mask = compute_mask(frame)

    # Paso 2: Preprocesar la máscara con desenfoque y dilatación
    blurred = cv.GaussianBlur(mask, (11, 11), 0)
    merged = cv.dilate(
        blurred, cv.getStructuringElement(cv.MORPH_RECT, (5, 1)))

    # Paso 3: Segmentación de objetos mediante la transformada de distancia
    sure_fg, unknown, dt = segment_foreground(merged)

    # Paso 4: Aplicar el algoritmo Watershed para mejorar la segmentación
    binary, markers = apply_watershed(frame, sure_fg, unknown)

    # Paso 5: Encontrar los componentes conectados en la imagen segmentada
    nlabels, markers, stats, centroids = cv.connectedComponentsWithStats(
        binary)
    centroids = centroids[1:]  # Excluir el fondo

    # Paso 6: Rastrear los objetos detectados
    global plant_count, object_tracker
    plant_count, object_tracker = track(centroids, line_x, line_thickness)

    # Paso 7: Dibujar los objetos y resultados sobre el frame
    img = draw_objects(frame, object_tracker, plant_count)

    return img, markers, dt


# Parámetros globales
object_tracker = {}  # Diccionario para rastrear los objetos
object_id = 0  # ID inicial de objetos
# Máximo de frames que un objeto puede desaparecer antes de ser descartado
max_disappear_frames = 30
plant_count = 0  # Contador de plantas detectadas
# Posición relativa de la línea de conteo (90% del ancho de la imagen)
line_position = 0.9
line_thickness = 12  # Grosor de la línea de conteo
paused = False  # Estado de pausa del procesamiento de video


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Video path required")
        exit(1)

    # Inicializar captura de video desde el archivo especificado
    video_path = sys.argv[1]
    cap = cv.VideoCapture(video_path)

    # Obtener las dimensiones del video
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    # Ventana para mostrar video original
    cv.namedWindow("video", cv.WINDOW_NORMAL)
    # Ventana para mostrar resultados procesados
    cv.namedWindow("proc", cv.WINDOW_NORMAL)
    # Ventana para mostrar otros resultados (como la transformada de distancia)
    cv.namedWindow("other", cv.WINDOW_NORMAL)

    # Bucle principal para procesar cada frame del video
    frame = None
    ret = True
    while True:
        if not paused or frame is None:
            ret, frame = cap.read()  # Leer el siguiente frame
            if not ret:
                break  # Salir si no hay más frames

        # Procesar el frame y obtener la imagen resultante, marcadores y la transformada de distancia
        img, markers, dt = process_frame(frame[:, frame_width // 2:, :])

        # Mostrar los resultados en las ventanas correspondientes
        cv.imshow("video", img)
        cv.imshow("proc", cv.applyColorMap(
            np.uint8(markers / markers.max() * 255), cv.COLORMAP_TURBO))
        cv.imshow("other", cv.applyColorMap(
            np.uint8(dt / dt.max() * 255), cv.COLORMAP_TURBO))

        key = cv.waitKey(1)
        if key == ord("q"):
            break  # Salir si se presiona 'q'
        elif key == ord(" "):
            paused = not paused  # Alternar entre pausa y reanudación

    cap.release()  # Liberar la captura de video
    cv.destroyAllWindows()  # Cerrar todas las ventanas
