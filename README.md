DITHERING IMAGE - PROCESSAMENTO DE IMAGENS EM PYTHON
------------------------------------------------------

Descrição do Projeto
---------------------
Este repositório contém um projeto Python desenvolvido para aplicar o filtro de Dithering no processamento de imagens. O programa permite realizar dithering em tons de cinza e em cores, além de armazenar os dados da imagem original no Redis com tempo de expiração, ideal para testes e análise temporária.

O desenvolvimento foi feito utilizando a IDE Visual Studio Code, devido à praticidade do terminal integrado e à disponibilidade de extensões úteis.

Requisitos
-----------
- Python 3.8 ou superior
- Redis em execução local ou remoto
- Bibliotecas: numpy, pillow, matplotlib, python-dotenv, redis

Ambiente Virtual
------------------
Este projeto utiliza um ambiente virtual Python para isolar suas dependências. Siga os passos abaixo para configurá-lo:

1. Acesse o diretório do projeto:
   cd /caminho/para/o/projeto

2. Crie o ambiente virtual:
   python3 -m venv venv

3. Ative o ambiente virtual:
   source venv/bin/activate

4. Instale as dependências:
   pip install -r requirements.txt

Para desativar o ambiente virtual:
   deactivate

Execução do Programa
---------------------
1. Crie um arquivo `.env` com as variáveis do Redis:
   Exemplo:
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   REDIS_USER=seu_usuario
   REDIS_PASSWORD=sua_senha

2. Execute o script principal:
   python main.py

3. Informe o caminho da imagem quando solicitado.

A imagem processada será salva como `resultado.png` e os dados originais serão armazenados no Redis com expiração de 10 segundos.

Princípios SOLID Aplicados
---------------------------
Durante a refatoração do projeto foram aplicados dois princípios do SOLID: SRP e OCP, resultando em um código mais organizado, reutilizável e fácil de manter.

1. SRP – Single Responsibility Principle (Princípio da Responsabilidade Única):
   - O código foi dividido em múltiplas classes com responsabilidades bem definidas.
   - A lógica de processamento de imagem foi separada da lógica de armazenamento no Redis.
   - Funções com múltiplas utilidades foram substituídas por classes como:
     - DitheringStrategy (abstração)
     - GrayscaleDithering
     - ColorDithering
     - RedisStorage

2. OCP – Open/Closed Principle (Aberto para Extensão, Fechado para Modificação):
   - Agora é possível adicionar novos algoritmos de dithering criando novas classes que estendem DitheringStrategy.
   - Isso evita a modificação de código existente e facilita a evolução do projeto.

