from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import fitz  # PyMuPDF
import os


def ocr_image(image):
    # Verificar se a imagem já está em tons de cinza ou preto e branco
    if image.mode not in ["L", "1"]:
        # Converter para tons de cinza se a imagem não estiver em "L" ou "1"
        image = image.convert("L")

    # Aumentar contraste e nitidez para melhorar OCR
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)  # Ajuste o valor conforme necessário
    image = image.filter(ImageFilter.SHARPEN)
    # image.show()
    # Aplicar OCR
    text = pytesseract.image_to_string(image, lang="por")
    return text


class ImageToText:
    def __init__(self, lang="por"):
        """Inicializa a classe com o idioma do OCR (padrão: português)."""
        self.lang = lang  # Defina 'por' para português ou o idioma de sua preferência

    def image_to_text(self, file_path):
        """Converte uma imagem ou PDF em texto usando OCR."""
        try:
            # Verificar se o arquivo é uma imagem ou um PDF
            if file_path.lower().endswith(
                (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
            ):
                # Carregar a imagem diretamente
                image = Image.open(file_path)
                # Executar OCR na imagem
                text = ocr_image(image)
                return text
            elif file_path.lower().endswith(".pdf"):
                # Carregar o PDF
                pdf_document = fitz.open(file_path)
                text = ""
                # Criar diretório para salvar as imagens convertidas
                output_dir = "converted_images"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                # Iterar sobre cada página do PDF
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    # Converter a página para uma imagem com a maior qualidade possível
                    pix = page.get_pixmap(
                        matrix=fitz.Matrix(600 / 72, 600 / 72)
                    )  # 600 DPI
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    # Salvar a imagem convertida como JPG
                    img_path = os.path.join(output_dir, f"page_{page_num + 1}.jpg")
                    img.save(img_path, "JPEG", quality=95)  # Alta qualidade JPEG
                    # Executar OCR na imagem
                    page_text = ocr_image(img)
                    text += page_text
                return text
            else:
                raise ValueError("Formato de arquivo não suportado.")
        except ValueError as ve:
            print("Erro ao processar o arquivo:", ve)
            return None
        except Exception as e:
            print("Erro inesperado ao processar o arquivo:", e)
            return None


# Exemplo de uso
if __name__ == "__main__":
    image_processor = ImageToText(lang="por")
    file_path = "evidência2.pdf"  # Substitua pelo caminho da sua imagem ou PDF

    texto_extraido = image_processor.image_to_text(file_path)
    if texto_extraido:
        print("Texto extraído do arquivo:")
        print(texto_extraido)  # Imprime o texto extraído sem truncamento
        # Salvar o texto extraído em um arquivo txt
        with open("extracted_text.txt", "w", encoding="utf-8") as text_file:
            text_file.write(texto_extraido)
        print("Texto extraído salvo em 'extracted_text.txt'.")
    else:
        print("Nenhum texto encontrado ou erro na leitura do arquivo.")
