# Conteo de Plántulas en Video con Segmentación y Seguimiento

### Autores:
- Sneyder Buitrago González  
- Daniel Ramírez Cárdenas

---

## 📌 Descripción

Este proyecto realiza el **conteo automático de plántulas** en un video, utilizando técnicas de **procesamiento digital de imágenes**, **segmentación avanzada** y **seguimiento de objetos**. 

El algoritmo está diseñado para trabajar con videos donde:
- La **cámara se mueve de derecha a izquierda**.
- Las **plántulas se mueven de izquierda a derecha** (relativo a la cámara).

Las plántulas son segmentadas, identificadas y rastreadas a través de los cuadros del video. El conteo ocurre cuando las plántulas cruzan una **línea de conteo vertical** ubicada cerca del borde izquierdo del video.

---

## 📷 Resultado del procesamiento de imagen
(img/img.png)

## 🧠 Características técnicas

- Conversión de color a espacio **LAB** para segmentación robusta.
- Aplicación de **umbral adaptativo con Otsu** para obtener la máscara binaria.
- Uso de la **transformada de distancia** para mejorar la separación de objetos.
- Aplicación del algoritmo **Watershed** para separar plántulas cercanas.
- **Seguimiento de centroides** a través de frames.
- **Conteo confiable** cuando los objetos cruzan una línea de detección.

---

## ⚙️ Requisitos

Este proyecto está implementado en Python 3 e incluye las siguientes dependencias:

- [`opencv-python`](https://pypi.org/project/opencv-python/)
- [`numpy`](https://pypi.org/project/numpy/)

Puedes instalarlas ejecutando:

```bash
pip install opencv-python numpy
```
## 🚀 Uso

Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/plants-counter.git
```
cd plants-counter
Asegúrate de tener el archivo de video que deseas procesar.

Ejecuta el programa con el siguiente comando:

```bash
python count.py <ruta_al_video>
```
Ejemplo:

```bash
python count.py videos/plantulas.mp4
```
Durante la ejecución se abrirán varias ventanas:

- video: muestra el video con los objetos rastreados y el contador.
- proc: muestra la segmentación de objetos con watershed.
- other: muestra la transformada de distancia.

Presiona la tecla espacio para pausar/reanudar el procesamiento. Presiona q para salir.

## 📦 Estructura del Proyecto
````bash
plants-counter/
├── count.py             # Código principal de conteo
├── tracker.py           # Lógica de rastreo de objetos
├── README.md            # Documentación del proyecto
└── videos/              # Carpeta opcional para guardar videos de entrada
````

## 📷 Recomendaciones para los Videos

- Las plántulas deben tener coloración verde visible.
- El fondo debe tener suficiente contraste con las plantas.
- Movimiento preferido: cámara de derecha a izquierda, plántulas de izquierda a derecha.

## 🧩 Posibles Mejoras Futuras

- Entrenamiento con redes neuronales para mejorar la detección.
- Exportación de estadísticas a CSV.
- Interfaz gráfica (GUI).
- Soporte para múltiples líneas de conteo.


## 📬 Contacto

Si tienes preguntas, sugerencias o deseas colaborar, no dudes en contactar a:

- Daniel Ramírez Cárdenas
- 📧 daniel.ramirez7@udea.edu.co
- Sneyder Buitrago González
- 📧 sneyder.buitrago@udea.edu.co
- 📍 Medellín, Colombia



