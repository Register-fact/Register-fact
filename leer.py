import pytesseract
from PIL import Image

# Cargar la imagen
imagen = Image.open('image.jpg')

# Utilizar pytesseract para leer el texto de la imagen
texto = pytesseract.image_to_string(imagen)

# Imprimir el texto extraído
print(texto)
