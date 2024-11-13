from ollama_chat import Chat
from ocr import ImageToText
from datetime import datetime


def risk_grade(value):
    # Verificar e imprimir o nível de risco com base no valor
    if 1 <= value <= 2.25:
        print("Insignificante")
    elif 2.26 <= value <= 4.51:
        print("Baixo Risco")
    elif 4.52 <= value <= 6.77:
        print("Médio Risco")
    elif 6.78 <= value <= 10:
        print("Alto Risco")
    else:
        print("Valor fora do intervalo esperado")


def calculate_exceedance(value, limit):
    # Check if the value is within the limit or exceeds it
    if value <= limit:
        return 0  # Does not exceed the limit

    # Calculate the percentage of exceedance
    exceedance_percentage = ((value - limit) / limit) * 100

    # Return the appropriate value based on the exceedance range
    if 1 <= exceedance_percentage <= 5:
        return 0.5
    elif 6 <= exceedance_percentage <= 10:
        return 1
    elif 11 <= exceedance_percentage <= 50:
        return 1.5
    elif exceedance_percentage > 51:
        return 2


def answer_to_bool(res):
    """Converte uma resposta de 'sim' ou 'não' em um valor booleano."""
    res = res.strip().lower()
    if res.startswith(("sim", "s", "yes", "y", "1")):
        return True
    elif res.startswith(("não", "nao", "n", "no", "0")):
        return False
    else:
        print("Resposta inválida. Por favor, responda com 'sim' ou 'não'.")
        return None


def get_answers():
    # Pergunta sobre o número de pessoas atendidas
    while True:
        try:
            number_persons = int(input("Qual o número de pessoas atendidas?\n"))
            break
        except ValueError:
            print("Por favor, insira um número válido.")

    # Pergunta se os atendidos são parte do governo
    while True:
        res = input("Os atendidos são parte do governo? (sim/não)\n")
        part_of_government = answer_to_bool(res)
        if part_of_government is not None:
            print(part_of_government)
            break

    # Pergunta sobre o tipo de hospitalidade
    hospitality_type = input("Qual o tipo de hospitalidade?\n").strip()

    # Pergunta se há parentes do atendente entre os atendidos
    while True:
        res = input("Entre os atendidos existem parentes do atendente? (sim/não)\n")
        relatives = answer_to_bool(res)
        if relatives is not None:
            break

    # Pergunta se as aprovações necessárias já foram obtidas
    while True:
        res = input("Você já obteve as aprovações necessárias? (sim/não)\n")
        approvals = answer_to_bool(res)
        if approvals is not None:
            break

    # Pergunta sobre o caminho do arquivo do recibo
    receipt_path = input("Qual o caminho do arquivo do recibo?\n").strip()

    # Retorna um dicionário com todas as respostas
    return {
        "number_persons": number_persons,
        "part_of_government": part_of_government,
        "hospitality_type": hospitality_type,
        "relatives": relatives,
        "approvals": approvals,
        "receipt_path": receipt_path,
    }


res = get_answers()
limit_per_person = 400.00
# Exemplo de uso
print("Realizado conversão da imagem em texto...")
image_processor = ImageToText(lang="por")  # Substitua pelo caminho da sua imagem
extracted_text = image_processor.image_to_text(res["receipt_path"])
print("Conversão de imagem para texto finalizada.")
print("Iniciando análise do recibo...")

chat = Chat()
chat.set_context(extracted_text)
value = chat.get_value()
date = chat.get_date()
is_in_category = chat.get_category(res["hospitality_type"])
is_receipt = chat.is_receipt()

attendees_weight = (2 if res["part_of_government"] is True else 1) * 3
print("Attendees Weight:", attendees_weight)

relatives_weight = 2 if res["relatives"] is True else 0
print("Relatives Weight:", relatives_weight)

form_weight = (2 if date <= datetime.now() else 0) * 3
print("Form Weight:", form_weight)

misclassification_weight = 2 if is_in_category is False else 0
print("Misclassification Weight:", misclassification_weight)

receipt_weight = (2 if is_receipt is False else 0) * 3
print("Receipt Weight:", receipt_weight)

approvals_weight = 2 if res["approvals"] is False else 0
print("Approvals Weight:", approvals_weight)

limits_weight = (
    calculate_exceedance(value, (limit_per_person * res["number_persons"])) * 2
)
print("Limits Weight:", limits_weight)

final_score = (
    (
        attendees_weight
        + relatives_weight
        + form_weight
        + receipt_weight
        + approvals_weight
        + limits_weight
    )
    / 11
) * 5

print("Resultado da análise de risco:")
print(final_score)

risk_grade(final_score)
