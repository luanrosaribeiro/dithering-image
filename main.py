# ditherizacao_luan_cache_upload.py
# Luan Rosa Ribeiro - 20242BG.ADS0011
# Instruções de Build:
#   - Ative o ambiente virtual: source venv/bin/activate
#   - Crie um arquivo `.env` com as credenciais do Redis
#   - Rode o comando: python ditherizacao_luan_cache_upload.py
#   - Após preencher o caminho da imagem, o programa salva as ditherizações
#     e também armazena os dados originais no Redis.

import os
import redis
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Conecta ao Redis
try:
    r = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        username=REDIS_USER,
        password=REDIS_PASSWORD,
        decode_responses=False
    )
    r.ping()
    print("Conexão com o Redis estabelecida com sucesso!")

except redis.exceptions.ConnectionError as e:
    print(f"Erro ao conectar com o Redis: {e}")
    exit()

def dithering_escala_cinza(img):
    img = img.convert('L')
    arr = np.array(img, dtype=np.float32)
    height, width = arr.shape

    for y in range(height):
        for x in range(width):
            old_pixel = arr[y, x]
            new_pixel = 0 if old_pixel < 128 else 255
            arr[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            if x + 1 < width:
                arr[y, x + 1] += quant_error * 7 / 16
            if x - 1 >= 0 and y + 1 < height:
                arr[y + 1, x - 1] += quant_error * 3 / 16
            if y + 1 < height:
                arr[y + 1, x] += quant_error * 5 / 16
            if x + 1 < width and y + 1 < height:
                arr[y + 1, x + 1] += quant_error * 1 / 16

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def dithering_escala_colorida(img):
    img = img.convert('RGB')
    arr = np.array(img, dtype=np.float32)
    height, width, _ = arr.shape

    def quantize(value):
        return round(value / 255 * 15) * (255 // 15)

    for y in range(height):
        for x in range(width):
            old_pixel = arr[y, x].copy()
            new_pixel = [quantize(v) for v in old_pixel]
            arr[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            for dx, dy, factor in [(1, 0, 7/16), (-1, 1, 3/16), (0, 1, 5/16), (1, 1, 1/16)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    arr[ny, nx] += quant_error * factor

    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

image_path = input("Digite o caminho da imagem: ")

try:
    original = Image.open(image_path)
    original_array = np.array(original)

    # Armazenar dados no Redis com expiração de 10s
    expire_time = 10
    r.setex('caminho_imagem_original', expire_time, image_path.encode('utf-8'))
    r.setex('matriz_imagem_original', expire_time, original_array.tobytes())
    r.setex('forma_matriz_original', expire_time, json.dumps(original_array.shape).encode('utf-8'))
    r.setex('dtype_matriz_original', expire_time, str(original_array.dtype).encode('utf-8'))
    print("Imagem original e matriz armazenadas no Redis com sucesso (expiram em 10s).")

    # Gerar imagens
    img_escala_cinza = dithering_escala_cinza(original)
    img_colorida = dithering_escala_colorida(original)

    # Mostrar e salvar
    fig, axs = plt.subplots(1, 3, figsize=(15, 10))
    axs[0].imshow(original)
    axs[0].set_title("Original")
    axs[1].imshow(img_escala_cinza, cmap='gray')
    axs[1].set_title("Ditherização em Tons de Cinza")
    axs[2].imshow(img_colorida)
    axs[2].set_title("Ditherização com Cores")

    for ax in axs:
        ax.axis('off')

    plt.tight_layout()
    plt.savefig("resultado.png")
    print("Imagem salva como resultado.png")

except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
