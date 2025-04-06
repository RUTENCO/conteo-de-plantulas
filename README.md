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
