import joblib
import sys
import os
import warnings
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Suprimir advertencias
warnings.filterwarnings('ignore')
#Direcciones de archivos
script_dir = os.path.dirname(os.path.abspath(__file__))
kmeans_model_path = os.path.join(script_dir, 'kmeans_model.pkl')
Scaler_path= os.path.join(script_dir, 'scaler.pkl')
label_encoders_path = os.path.join(script_dir, 'label_encoders.pkl')
# Cargar el modelo KMeans y los LabelEncoders
kmeans_loaded = joblib.load(kmeans_model_path)
label_encoders = joblib.load(label_encoders_path)
scaler = joblib.load(Scaler_path)

# Obtener los parámetros de la línea de comandos
if len(sys.argv) != 6:
    print("Uso: python modelo.py <Hora> <Circuito> <Tipo> <Día de la Semana> <month>")
    sys.exit(1)

hora = int(sys.argv[1])
circuito = sys.argv[2]
tipo = sys.argv[3]
dia_de_la_semana = sys.argv[4]
month = int(sys.argv[5])
#Diccionario para permitir entrada en español
dia_semana_dict = {
    'lunes': 'Monday',
    'martes': 'Tuesday',
    'miércoles': 'Wednesday',
    'jueves': 'Thursday',
    'viernes': 'Friday',
    'sábado': 'Saturday',
    'domingo': 'Sunday'
}
#Todo a minúsculas
dia_de_la_semana = dia_de_la_semana.lower()
#Usamos el diccionario
dia_de_la_semana = dia_semana_dict.get(dia_de_la_semana, 'Desconocido')
entrada = [hora, circuito, tipo, dia_de_la_semana, month]

# Supongamos que 'nuevos_datos' es un DataFrame con los datos que quieres predecir
columnas = ['Hora', 'Circuito', 'Tipo', 'Día de la Semana', 'month']
nuevos_datos = pd.DataFrame([entrada], columns=columnas)

# Aplicar la transformación a las nuevas columnas usando los LabelEncoders
for column in nuevos_datos.columns:
    le = label_encoders[column]
    # Aplicar la transformación a la nueva columna
    nuevos_datos[column] = le.transform(nuevos_datos[column])

nuevos_datos = scaler.transform(nuevos_datos)
# Predecir usando el modelo cargado
predicciones = kmeans_loaded.predict(nuevos_datos)
prediccion = predicciones[0]

# Clasificar la predicción
if prediccion == 0:
    clasificacion = "Llamada de importancia grave"
elif prediccion == 1:
    clasificacion = "Llamada de importancia moderada"
elif prediccion == 2:
    clasificacion = "Ruidos e incidentes de menor importancia"

print(f"La llamada fue clasificada en: {clasificacion}")