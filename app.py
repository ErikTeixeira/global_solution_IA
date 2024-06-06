# pip install streamlit roboflow pillow opencv-python
# pip install pillow

# Execute o aplicativo Streamlit:
# streamlit run app.py

import io
from PIL import Image
import streamlit as st
import cv2
from roboflow import Roboflow

# Substitua pela sua chave de API do Roboflow
API_KEY = "p8ToOtSdu8VxVhNv6hYF"

# Dicionário para mapear classes a cores
cores_por_classe = {
    "Fishing net": (0, 0, 128),  # Azul escuro
    "aluminum can": (135, 206, 250),  # Azul claro
    "bottle": (128, 0, 128),  # Roxo
    "plastic bag": (255, 165, 0),  # Laranja
    "plastic waste": (255, 0, 0),  # Vermelho
    "tire": (0, 128, 0)  # Verde
}

def identificar_objetos(imagem):
    rf = Roboflow(api_key=API_KEY)
    project = rf.workspace("reconhecimentoimgs").project("global-solution")
    model = project.version(4).model

    # Converte a imagem do Streamlit para o formato do OpenCV
    imagem = Image.open(imagem)
    imagem = np.array(imagem)
    imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)

    # Realiza a inferência
    prediction = model.predict(imagem, confidence=40, overlap=30)

    # Desenha as bounding boxes e informações na imagem
    for predicao in prediction:
        confianca = predicao['confidence']

        # Verifica se a confiança é maior que 0.6 (60%)
        if confianca > 0.6:
            x1 = int(predicao['x'] - predicao['width'] / 2)
            y1 = int(predicao['y'] - predicao['height'] / 2)
            x2 = int(x1 + predicao['width'])
            y2 = int(y1 + predicao['height'])
            classe = predicao['class']

            # Obtém a cor para a classe
            cor = cores_por_classe.get(classe, (0, 0, 0)) # Cor padrão: preto

            # Desenha o retângulo com a cor da classe
            imagem = cv2.rectangle(imagem, (x1, y1), (x2, y2), cor, 2)

            # Adiciona o texto com a classe e confiança
            texto = f"{classe}: {confianca:.2f}"
            cv2.putText(imagem, texto, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor, 2)

    return imagem

# Configura a página do Streamlit
st.title("Identificação de Objetos")
st.write("Faça o upload de uma imagem para detectar objetos.")

# Cria um widget de upload de arquivo
imagem_carregada = st.file_uploader("Escolha uma imagem...", type=["jpg", "png", "jpeg"])

if imagem_carregada is not None:
    # Exibe a imagem carregada
    st.image(imagem_carregada, caption='Imagem Carregada', use_column_width=True)

    # Realiza a identificação dos objetos na imagem
    if st.button("Identificar Objetos"):
        imagem_com_deteccoes = identificar_objetos(imagem_carregada)

        # Exibe a imagem com as detecções
        st.image(imagem_com_deteccoes, caption='Imagem com Detecções', use_column_width=True)