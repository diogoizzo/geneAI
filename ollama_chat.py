import ollama
from datetime import datetime


def res_to_bool(texto):
    # Listas de variantes para "sim" e "não"
    positivos = {"sim", "yes"}  # Adicione variantes conforme necessário
    negativos = {"não", "nao", "no"}  # Adicione variantes conforme necessário

    # Converter texto para minúsculas e remover espaços extras
    texto = texto.strip().lower()

    # Verificar se o início do texto contém um valor positivo ou negativo
    for pos in positivos:
        if texto.startswith(pos):
            return True
    for neg in negativos:
        if texto.startswith(neg):
            return False

    # Retornar None se não for reconhecido como "sim" ou "não"
    return None


class Chat:

    def __init__(self, model="gemma2:latest"):
        self.model = model
        # Definindo a regra de sistema padrão
        self.system_rule = "Você deve extrair as respostas no Contexto passado para você antes da pergunta. A resposta deve ser exclusivamente com base nesse contexto e em português"
        self.context = None

    def set_context(self, context):
        """Define o contexto que será incluído em todas as perguntas, se existir."""
        self.context = context

    def set_system_rule(self, rule):
        """Altera a regra de sistema."""
        self.system_rule = rule

    def ask(self, question):
        """Faz uma pergunta ao modelo, incluindo a regra de sistema e o contexto, se definido."""

        # Cria o array de mensagens, incluindo a regra de sistema
        messages = [
            {
                "role": "system",
                "content": self.system_rule,
            }
        ]

        # Adiciona o contexto, se existir
        if self.context:
            messages.append(
                {
                    "role": "user",
                    "content": f"[Contexto: {self.context}] [Question: {question}]",
                }
            )
        else:
            # Adiciona a pergunta do usuário
            messages.append(
                {
                    "role": "user",
                    "content": question,
                }
            )
        # Envia a pergunta para o modelo
        response = ollama.chat(model=self.model, messages=messages)

        # Retorna a resposta do modelo
        return response["message"]["content"]

    def get_value(self):
        self.set_system_rule(
            "Você deve extrair as respostas no Contexto passado para você antes da pergunta. Responda somente com o número do valor, sem mais nenhuma letra ou palavras, extraia apenas o valor. Sempre separando as casas decimais com a vírgula"
        )
        resposta = self.ask(
            "Extraia do texto fornecido somente seu valor total da nota, de produtos ou serviços realizados. Responda somente com o número do valor, sem mais nenhuma letra ou palavras, extraia apenas o valor que deve ser o total do recibo, o valor total dos produtos. Enfim, os somatório  de todos os itens, o valor total encontrado no texto que eu estou fornecendo em conjunto com essa pergunta"
        )
        print("Pergunta: Qual o valor total desse recibo?")
        print("Resposta:", resposta.strip())
        resposta = resposta.replace(",", ".")
        return float(resposta.strip())

    def get_date(self):
        self.set_system_rule(
            "Você deve extrair as respostas no Contexto passado para você antes da pergunta. Extraia do texto fornecido somente a data e não inclua mais nenhuma palavra ou letra a mais. A data deve ser respondida no formato em que for encontrada, apenas reproduza exatamente da forma que esta no contexto"
        )

        res = self.ask(
            "Extraia do texto fornecido a data de emissao desse recibo, comprovante ou nota fiscal. Você devo procurar um por uma data que esteja perto da palavra emissao, emissão, data ou dia, , em último caso pegue a única data encontrada (no formato dia, mês e ano).Somente apresente uma data que esteja no contexto passado, nunca invente uma data. Extraia  somente a data e não inclua mais nenhuma palavra ou letra a mais."
        )
        print("Pergunta: Qual a data desse recibo?")
        print("Resposta:", res.strip())
        return datetime.strptime(res.strip(), "%d/%m/%Y")

    def get_category(self, category):
        self.set_system_rule(
            "Você deve responder com base no texto passado em contexto e apenas com SIM ou NÃO, sem mais nenhuma letra na resposta e deve verificar se os itens listados no contexto são do tipo que é especificado na pregunta. Se forem, você deve responder com SIM, se não forem, você deve responder com NÃO"
        )
        res = self.ask(
            f"Do Contexto passado junto com essa pergunta, verifique se todos os itens estão na categoria ou relacionados extensivamente a categoria de {category}. Alimentação inclui bebidas e outras compras de supermercado. Hospedagem também inclui bebidas e tudo que esta relacionado a um estadia, incluindo transporte e etc"
        )
        print(f"Pergunta: O recibo esta na categoria de {category}?")
        print("Resposta:", res.strip())
        return res_to_bool(res.strip())

    def is_receipt(self):
        self.set_system_rule(
            "Você deve responder com base no texto passado em contexto e apenas com SIM ou NÃO, sem mais nenhuma letra na resposta ou qualquer outra explicação."
        )
        res = self.ask(
            "Analise o texto passado em contexto e determine se ele se trata de um recibo, nota fiscal ou comprovante fiscal completo e real. Verifique se contém os seguintes elementos essenciais: Lista de itens com descrições e preços individuais. Valor total do recibo, preferencialmente destacado. Data e hora da transação. Identificação do estabelecimento (nome, endereço, ou outros detalhes). Informações adicionais, como formas de pagamento ou imposto. Responda com 'SIM' se o recibo é completo, 'NÃO' se está incompleto"
        )
        print("Pergunta: O recibo esta completo e é um recibo real?")
        print("Resposta:", res)
        return res_to_bool(res)
