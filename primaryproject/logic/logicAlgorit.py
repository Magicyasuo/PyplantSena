from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

image_path = r'C:\Users\ingdi\Downloads\primaryproject\images\Captura.PNG'
img = Image.open(image_path)
img_np = np.array(img)

import matplotlib.pyplot as plt
import matplotlib.patches as patches

img = Image.open(image_path)
img_np = np.array(img)

# Define tus coordenadas de interés
coordenadas_interes = [(720, 120),(570,60), (62, 105), (310, 400)]

# Crear la figura y el eje con un plano cartesiano
fig, ax = plt.subplots(figsize=(10, 6))  # Puedes ajustar el tamaño de la figura aquí


# Añadir los puntos rojos para cada coordenada de interés
for x, y in coordenadas_interes:
    ax.scatter(x, y, s=100, c='red', marker='o')  # Ajusta el tamaño y color si es necesario

# Ajustar los límites de los ejes para igualar las dimensiones de la imagen
ax.set_xlim(0, img_np.shape[1])
ax.set_ylim(0, img_np.shape[0])

# Invertir el eje Y para que el origen (0,0) esté en la esquina superior izquierda
# ax.invert_yaxis()

# Función para extraer áreas alrededor de las coordenadas con un cierto radio
radio = 16  # Definir un radio para extraer áreas alrededor de las coordenadas
def extraer_areas(img_np, coordenadas, radio):
    areas = []
    for x, y in coordenadas:
        area = img_np[y-radio:y+radio, x-radio:x+radio]
        areas.append(area)
    return areas

# Extraer las áreas de interés
areas_interes = extraer_areas(img_np, coordenadas_interes, radio)

# Opcional: Visualizar las áreas extraídas
for area in areas_interes:
    plt.imshow(area)
    # # # plt.show()

from skimage.feature import match_template
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.patches as patches

# Asumiendo que img_np es tu imagen numpy cargada previamente
# Asumiendo que areas_interes son las plantillas extraídas previamente

def agrupar_detecciones(coincidencias, umbral_dist=10):
    agrupadas = []
    visitado = [False] * len(coincidencias)

    for i, (y, x) in enumerate(coincidencias):
        if not visitado[i]:
            grupo = [(y, x)]
            visitado[i] = True
            for j, (y2, x2) in enumerate(coincidencias):
                if not visitado[j]:
                    distancia = np.sqrt((y - y2)**2 + (x - x2)**2)
                    if distancia <= umbral_dist:
                        grupo.append((y2, x2))
                        visitado[j] = True
            prom_y = int(np.mean([pos[0] for pos in grupo]))
            prom_x = int(np.mean([pos[1] for pos in grupo]))
            agrupadas.append((prom_y, prom_x))
    return agrupadas

def extraer_subimagenes(img_np, coordenadas, radio):
    subimagenes = []
    altura, ancho = img_np.shape[:2]
    for y, x in coordenadas:
        if x-radio >= 0 and y-radio >= 0 and x+radio < ancho and y+radio < altura:
            subimagen = img_np[y-radio:y+radio, x-radio:x+radio]
            subimagenes.append(subimagen)
    return subimagenes

# Proceso de coincidencia de plantillas y agrupación
resultados_combinados = None
for template in areas_interes:
    resultado = match_template(img_np, template)
    if resultados_combinados is None:
        resultados_combinados = resultado
    else:
        resultados_combinados = np.maximum(resultados_combinados, resultado)

umbral = 0.9  # Ajustar basado en pruebas
coincidencias = np.where(resultados_combinados >= umbral)
coincidencias_agrupadas = agrupar_detecciones(list(zip(coincidencias[0], coincidencias[1])))

# Extracción de sub-imágenes usando detecciones agrupadas
radio_subimagen = 25  # Ajustar según el tamaño esperado de las plantas
subimagenes_plantas = extraer_subimagenes(img_np, coincidencias_agrupadas, radio_subimagen)

# Visualización de la imagen original con puntos de detección superpuestos
fig, ax = plt.subplots(figsize=(10, 6))

# Imprimir el número total de plantas contadas en la consola
numero_de_plantas_contadas = len(coincidencias_agrupadas)
print(f"Número total de plantas contadas: {numero_de_plantas_contadas}")
# # # plt.show()


def calcular_exg(subimagen):
    if subimagen.ndim == 3 and subimagen.shape[2] >= 3:
        R = subimagen[:,:,0].astype(float) / 255
        G = subimagen[:,:,1].astype(float) / 255
        B = subimagen[:,:,2].astype(float) / 255
        ExG = 2*G - R - B
        return np.mean(ExG)
    else:
        return None


# Asegúrate de que subimagenes_plantas esté definido y contenga las sub-imágenes extraídas anteriormente
# Si no has definido N, puedes hacerlo aquí. N será el número de valores ExG a imprimir
N = numero_de_plantas_contadas

# Calcular ExG para cada sub-imagen
exg_valores = [calcular_exg(subimagen) for subimagen in subimagenes_plantas if subimagen is not None]


# Asegurándonos de que 'exg_valores' no contenga ningún None

#N = numero_de_plantas_contadas
exg_valores_filtrados = [valor for valor in exg_valores if valor is not None]

# Calcular el promedio de los valores de ExG
if exg_valores_filtrados:
    exg_promedio = sum(exg_valores_filtrados) / len(exg_valores_filtrados)
    print(f"Promedio de ExG para todas las sub-imágenes y numero de plantas encontradas: {exg_promedio}")
    print(f"Numero de plantas encontradas: {N}")
else:
    print("No hay valores de ExG para calcular el promedio.")

# Al final de logicAlgorit.py
def get_plant_info():
    # Asume que aquí ya calculaste las variables numero_de_plantas_contadas y exg_promedio
    return numero_de_plantas_contadas, exg_promedio
