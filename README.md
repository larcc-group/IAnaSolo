# IAnaSolo

Interpretação de Análises de Solo com uso de Deep Learning 

## Autores:
**Alisson Allebrandt** (Creator) <br>
**Diego H Schmidt** (Creator) <br>
**Dalvan Griebler** (Mentoring)

![ezgif com-video-to-gif (2)](https://user-images.githubusercontent.com/16272139/89842948-8810f980-db4d-11ea-9370-f1478d0bd2e5.gif)

Este repositório contém 4 projetos distintos, sendo eles:

1 - Interpretador de laudos de análise de solo [PYTHON] -> /ProcessamentoDeImagens\
2 - Aplicativo mobile para captura da foto do laudo de análise de solo e envio para interpretação e gravação dos resultados no banco de dados [REACT-NATIVE] -> /appMobile\
3 - Api para comunicação do app que se comunca com o interpretador de laudos de análise citado acima, e armazena os resultados em um banco de dados MongoDB [NODE JS] -> /api-node\
4 - Auditor feito em Node JS para validar os resultados processados pelo interpretador, e definir o grau de acertos e erros\

# Forma de execução do projeto

## 1 - Interpretador de laudos

Após ter o Python versão 2.7 instalado, será necessário instalar as dependências do projeto por meio do comando pip.

pip install numpy\
pip install pytesseract\
pip install opencv-python\
pip install google-cloud-vision\
pip install Pillow

Também será preciso instalar a biblioteca image magic na máquina https://imagemagick.org/script/download.php

 -- Qualquer outra dependência que possa vir a faltar pode ser buscada no site https://pypi.org/
 
 Após instalar o python e todas as dependências pode-se rodar o arquivo main.py para realização do processamento de laudos.
 Para este script são esperados os seguintes parâmetros de entrada:
 
  **parm_input_folder_images** = Pasta com as imagens de laudos de análise de solo para leitura e interpretação\
  **parm_layout_file** = Layout em formato .json do formato do laudo a ser analisado. Exemplo pode ser encontrado no repositório /ProcessamentoDeImagens/layouts/lab_setrem.json\
  **parm_extract_method** = full ou default. Full irá tentar extrair informações do cabebalho da análise também. Default, somente os nutrientes químicos.\
  **parm_output_results** = Pasta de saída para os resultados em .csv e imagens tratadas e convertidas.\
  **parm_convert_number** = True ou False, se estiver como True irá converter o valor do nutriente quimico para decimal.\
  
  
## 2 - Aplicativo mobile em react-native
 
 Instalar o React-Native na máquina: https://reactnative.dev/docs/getting-started </br>
 Abrir a pasta do projeto e executar npm install </br>
 Depois executar npx react-native run-android </br>
 
## 3 - API em Node Js e Auditor
 
 Ter o Node JS instalado na máquina: https://nodejs.org/en/download/ </br>
 Acessar a pasta do projeto e executar npm install </br>
 Executar npm run dev para iniciar o servidor </br>
 
 
 



