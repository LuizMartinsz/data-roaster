import pandas as pd
import numpy as np
from etl.ai_roaster import AIRoaster

class DataRoaster:
    """
    Classe principal de processamento de dados.
    Responsável por extrair métricas técnicas e orquestrar a geração de insights (Regras + IA).
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.metrics = {}
        self.roast_comments = []

    def analyze(self) -> dict:
        """Executa o profiling completo do dataset e chama a IA."""
        
        # 1. Cálculo de Métricas Técnicas (Hard Skills)
        self.metrics['shape'] = self.df.shape
        # Converte bytes para MB
        self.metrics['memory_mb'] = round(self.df.memory_usage(deep=True).sum() / (1024 ** 2), 2)
        self.metrics['duplicates'] = self.df.duplicated().sum()
        self.metrics['columns'] = list(self.df.columns)
        
        # Análise de Nulos (% por coluna)
        null_counts = self.df.isnull().sum()
        self.metrics['null_percent'] = ((null_counts / len(self.df)) * 100).round(2).to_dict()
        
        # 2. Geração de Roasts Baseados em Regras (Lógica de Negócio)
        self._generate_rule_based_roasts()
        
        # 3. Geração de Roast via IA (Llama 3 / Groq)
        # try/except para garantir que o sistema funcione mesmo sem API Key
        try:
            ai = AIRoaster()
            ai_comment = ai.generate_roast(self.metrics)
            # Insere o comentário da IA no topo da lista com destaque
            self.roast_comments.insert(0, f"🤖 [AI OPINION]: {ai_comment}")
        except Exception as e:
            # Falha silenciosa da IA, logamos apenas no console
            print(f"Warning: AI Roast failed via API. Reason: {e}")
            self.roast_comments.append("⚠️ [SYSTEM]: A IA está tirando um cochilo (Verifique sua API Key), mas as regras manuais rodaram.")

        return self.metrics

    def _generate_rule_based_roasts(self):
        """Gera comentários baseados em regras estáticas (Fallback e Segurança)."""
        
        # Regra 1: Integridade de Linhas (Duplicatas)
        if self.metrics['duplicates'] > 0:
            pct_dup = (self.metrics['duplicates'] / self.metrics['shape'][0]) * 100
            if pct_dup > 10:
                self.roast_comments.append(f"🔥 ALERTA CRÍTICO: {self.metrics['duplicates']} linhas duplicadas ({pct_dup:.1f}% do total). Isso distorce qualquer KPI.")
            else:
                self.roast_comments.append(f"⚠️ Atenção: Encontramos {self.metrics['duplicates']} duplicatas. Remova antes do load.")

        # Regra 2: Qualidade dos Dados (Sparsity/Nulls)
        clean_dataset = True
        for col, pct in self.metrics['null_percent'].items():
            if pct > 40:
                clean_dataset = False
                self.roast_comments.append(f"🗑️ A coluna '{col}' é praticamente lixo ({pct}% nula). Avalie dropar do schema.")
            elif pct > 10:
                clean_dataset = False
                self.roast_comments.append(f"⚠️ '{col}' tem {pct}% de dados faltantes. Cuidado com joins nessa chave.")

        # Regra 3: Otimização de Performance
        if self.metrics['memory_mb'] > 100:
            self.roast_comments.append(f"🐌 Dataset pesado ({self.metrics['memory_mb']}MB). Se for processar isso no Pandas sem Chunking, vai estourar a RAM.")

        # Elogio (raro, mas possível)
        if clean_dataset and self.metrics['duplicates'] == 0:
            self.roast_comments.append("✅ (Regra): Estruturalmente o dado parece sólido. Surpreendente.")

    def get_roast(self) -> list:
        """Retorna a lista final de feedbacks."""
        return self.roast_comments