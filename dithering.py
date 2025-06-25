from abc import ABC, abstractmethod
import numpy as np
from PIL import Image

class DitheringStrategy(ABC):
    @abstractmethod
    def apply(self, img: Image.Image) -> Image.Image:
        pass

class GrayscaleDithering(DitheringStrategy):
    def apply(self, img):
        img = img.convert('L')
        arr = np.array(img, dtype=np.float32)
        h, w = arr.shape

        for y in range(h):
            for x in range(w):
                old = arr[y, x]
                new = 0 if old < 128 else 255
                err = old - new
                arr[y, x] = new
                if x + 1 < w: arr[y, x + 1] += err * 7/16
                if x > 0 and y + 1 < h: arr[y + 1, x - 1] += err * 3/16
                if y + 1 < h: arr[y + 1, x] += err * 5/16
                if x + 1 < w and y + 1 < h: arr[y + 1, x + 1] += err * 1/16

        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

class ColorDithering(DitheringStrategy):
    def apply(self, img):
        img = img.convert('RGB')
        arr = np.array(img, dtype=np.float32)
        h, w, _ = arr.shape

        def quantize(v): return round(v / 255 * 15) * (255 // 15)

        for y in range(h):
            for x in range(w):
                old = arr[y, x].copy()
                new = [quantize(v) for v in old]
                err = old - new
                arr[y, x] = new
                for dx, dy, f in [(1,0,7/16),(-1,1,3/16),(0,1,5/16),(1,1,1/16)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < w and 0 <= ny < h:
                        arr[ny, nx] += err * f

        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
