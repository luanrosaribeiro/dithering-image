# main.py
# Luan Rosa Ribeiro - 20242BG.ADS0011
# Instruções de Build:
#   - Ative o ambiente virtual: source venv/bin/activate
#   - Crie um arquivo `.env` com as credenciais do Redis
#   - Rode o comando: python main.py
#   - Após preencher o caminho da imagem, o programa salva as ditherizações
#     e também armazena os dados originais no Redis (expira em 10s).

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from storage import RedisStorage
from dithering import GrayscaleDithering, ColorDithering

# Solicita o caminho da imagem ao usuário
image_path = input("Digite o caminho da imagem: ")

try:
    original = Image.open(image_path)
    original_array = np.array(original)

    # Armazena a imagem original no Redis com tempo de expiração
    storage = RedisStorage()
    storage.store_image(image_path, original_array)

    print("Imagem armazenada no Redis com sucesso.")

    # Aplica as estratégias de ditherização (aberto para extensão)
    strategies = [
        ("Original", original),
        ("Cinza", GrayscaleDithering().apply(original)),
        ("Colorida", ColorDithering().apply(original))
    ]

    # Exibe e salva a imagem com matplotlib
    fig, axs = plt.subplots(1, len(strategies), figsize=(15, 10))
    for ax, (title, img) in zip(axs, strategies):
        ax.imshow(img, cmap='gray' if title == "Cinza" else None)
        ax.set_title(title)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig("resultado.png")
    print("Imagem salva como resultado.png")

except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
