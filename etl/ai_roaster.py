import os
from groq import Groq
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class AIRoaster:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key:
            self.client = Groq(api_key=self.api_key)

    def generate_roast(self, metrics: dict) -> str:
        """
        Recebe as métricas técnicas e retorna um texto sarcástico gerado por IA.
        """
        if not self.client:
            return "⚠️ IA não configurada (Adicione a GROQ_API_KEY no .env para ver a mágica)."

        # Prompt Engineering: A "persona" do Data Engineer irritado
        prompt = f"""
        Aja como um Engenheiro de Dados Sênior muito rabugento e sarcástico (estilo Gordon Ramsay dos dados).
        Analise estas métricas de um dataset que acabaram de me enviar e faça um comentário curto (máx 3 frases) e ácido sobre a qualidade.
        
        Métricas:
        - Linhas: {metrics['shape'][0]}
        - Colunas: {metrics['shape'][1]}
        - Memória: {metrics['memory_mb']} MB
        - Linhas Duplicadas: {metrics['duplicates']}
        - Porcentagem de Nulos: {metrics['null_percent']}

        Se houver duplicatas ou muitos nulos, seja impiedoso. Se estiver limpo, desconfie.
        Responda em Português do Brasil. Use termos técnicos (ETL, Pipeline, Schema).
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Você é um assistente especialista em qualidade de dados."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192", # Modelo Open Source da Meta (Rápido e Free na Groq)
                temperature=0.7,
                max_tokens=150,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"A IA tentou analisar, mas teve um kernel panic: {str(e)}"