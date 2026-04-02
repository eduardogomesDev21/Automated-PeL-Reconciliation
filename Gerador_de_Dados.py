import pandas as pd
import numpy as np

def gerar_massa_xp(n_linhas=10000):
    np.random.seed(42)
    ativos = ['PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'SOLO11', 'DOLAR_FUT', 'WINJ26']
    
    data = {
        'id_transacao': [f'XP-{1000+i}' for i in range(n_linhas)],
        'ativo': np.random.choice(ativos, n_linhas),
        'quantidade': np.random.randint(100, 5000, n_linhas),
        'preco_anterior': np.random.uniform(10.0, 100.0, n_linhas).round(2),
        'preco_atual': np.random.uniform(10.0, 105.0, n_linhas).round(2),
    }
    
    df = pd.DataFrame(data)
    
    df['pnl_calculado'] = ((df['preco_atual'] - df['preco_anterior']) * df['quantidade']).round(2)
    
    df['pnl_reportado'] = df['pnl_calculado'].copy()
    
    idx_centavos = df.sample(frac=0.1).index
    df.loc[idx_centavos, 'pnl_reportado'] += np.random.uniform(0.01, 0.99, len(idx_centavos)).round(2)
    
    idx_critico = df.sample(frac=0.05).index
    df.loc[idx_critico, 'pnl_reportado'] += np.random.uniform(101.0, 5000.0, len(idx_critico)).round(2)
    
    df.to_csv('base_operacoes_xp.csv', index=False)
    print(" Massa de dados com 10.000 operações gerada com sucesso!")

gerar_massa_xp()