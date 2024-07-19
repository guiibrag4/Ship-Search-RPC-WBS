# Detecção de Navios

Bem-vindo ao projeto de Detecção de Navios! Este projeto utiliza RPC (Remote Procedure Call), Threads e OpenCV para detectar navios na imagem. 

![FotoSiteNavio](https://github.com/kelvin-sous/Ship-Search-RPC-WBS/assets/145872728/1dba5745-1942-4c9f-b28a-d1be60f73a82)

![FotoSiteNavio2](https://github.com/kelvin-sous/Ship-Search-RPC-WBS/assets/145872728/318e268c-63b1-4bcc-bd6f-4cf7ee08e915)

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Como Funciona](#como-funciona)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Contribuindo](#contribuindo)
- [Problemas Comuns](#problemas-comuns)
- [Contato](#contato)

## Sobre o Projeto

Este projeto foi desenvolvido para demonstrar a capacidade de detecção de objetos usando o OpenCV. Ele permite que os usuários façam upload de imagens, que são então processadas para detectar navios.

## Como Funciona

1. O usuário faz o upload de uma imagem através da interface web.
2. A imagem é enviada para o servidor, onde é processada usando um classificador Haar.
3. O servidor divide a imagem em segmentos para processamento paralelo.
4. Os navios detectados são marcados na imagem e o resultado é retornado ao usuário.

## Pré-requisitos

- Python 3.8+
- Flask
- OpenCV
- Um navegador web moderno

## Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/seu-usuario/deteccao-de-navios.git
    cd deteccao-de-navios
    ```

2. Crie um ambiente virtual e ative-o:

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    ```

3. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

4. Certifique-se de que o diretório `uploads` existe:

    ```sh
    mkdir -p uploads
    ```

## Uso

1. Inicie o servidor Flask:

    ```sh
    python app.py
    ```

2. Abra o navegador e acesse `http://127.0.0.1:5000`.

3. Faça o upload de uma imagem e clique em "Detectar Navios".

## Contribuindo

Contribuições são bem-vindas! Por favor, siga os passos abaixo para contribuir:

1. Fork o repositório.
2. Crie uma nova branch:

    ```sh
    git checkout -b feature/sua-feature
    ```

3. Faça suas modificações.
4. Faça o commit das suas alterações:

    ```sh
    git commit -m 'Adiciona nova funcionalidade'
    ```

5. Envie para o branch:

    ```sh
    git push origin feature/sua-feature
    ```

6. Abra um Pull Request.

## Problemas Comuns

### Erro ao Carregar o Classificador Haar

Certifique-se de que o caminho para o classificador Haar (`haarcascades/first_cascade.xml`) está correto e o arquivo existe.

### Imagem Não Processada Corretamente

Verifique se a imagem está sendo enviada corretamente e se o formato é suportado pelo OpenCV.

### O Carregador Não Aparece

Certifique-se de que o CSS e JavaScript estão corretamente incluídos e não há erros no console do navegador.

## Contato

Se você tiver perguntas ou sugestões, sinta-se à vontade para abrir uma issue ou entrar em contato:

**Email**: prokelvin65@gmail.com  
**GitHub**: [@kelvin-sous](https://github.com/kelvin-sous)  
  <br>
**Email**: guilhermebragariosdacosta@gmail.com  
**GitHub**: [@guiibrag4](https://github.com/guiibrag4)

---

Obrigado por conferir nosso projeto! Esperamos que seja útil e interessante para você.
