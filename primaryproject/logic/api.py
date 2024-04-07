from flask import Flask, jsonify
# Asegúrate de añadir el directorio al PYTHONPATH como se mostró anteriormente si es necesario
from logicAlgorit import get_plant_info

app = Flask(__name__)

@app.route('/get_plant_info', methods=['GET'])
def get_plant_data():
    numero_de_plantas, exg_promedio = get_plant_info()
    return jsonify({'numero_de_plantas': numero_de_plantas, 'exg_promedio': exg_promedio})

if __name__ == '__main__':
    app.run(debug=True)




