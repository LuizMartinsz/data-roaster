import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
import numpy as np
from etl.roaster import DataRoaster

# Fixture: cria dados falsos para teste
@pytest.fixture
def dirty_df():
    data = {
        'id': [1, 2, 2, 4, 5],
        'valor': [100, 200, 200, np.nan, 300], 
        'categoria': ['A', 'B', 'B', 'C', 'C']
    }
    return pd.DataFrame(data)

def test_roaster_metrics(dirty_df):
    """Testa se o motor calcula as métricas corretamente (Hard Skills)"""
    roaster = DataRoaster(dirty_df)
    metrics = roaster.analyze()

    assert metrics['shape'] == (5, 3)
    assert metrics['duplicates'] == 1 # Agora vai dar 1 duplicata real
    
    # Com os dados novos: temos 1 NaN na linha 4 (índice 3). 
    # 1 nulo em 5 linhas = 20%
    assert metrics['null_percent']['valor'] == 20.0 

def test_roaster_rules(dirty_df):
    """Testa se as regras de negócio estão gerando alertas"""
    roaster = DataRoaster(dirty_df)
    roaster.analyze()
    comments = roaster.get_roast()
    has_dup_warning = any("duplica" in c.lower() for c in comments if "AI OPINION" not in c)
    
    # Para debug: se falhar, imprime o que foi gerado
    if not has_dup_warning:
        print(f"\nComentários gerados: {comments}")

    assert has_dup_warning