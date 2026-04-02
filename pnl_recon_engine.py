
import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)

def processar_reconciliacao(input_path: str, output_path: str = 'divergencias_auditoria.csv') -> pd.DataFrame:
    """
    Executa a reconciliação do P&L reportado versus calculado.
    
    Parâmetros:
    - input_path (str): Caminho para o arquivo CSV de entrada (database de operações).
    - output_path (str): Caminho para o arquivo CSV de saída (auditoria de divergências).
    
    Retorna:
    - pd.DataFrame: Resumo executivo agregado por ativo e status de risco operacional.
    """
    
  
    file_path = Path(input_path)
    if not file_path.exists():
        logging.error(f"Arquivo não encontrado: {input_path}")
        return pd.DataFrame()
        
    logging.info(f"Iniciando ingestão do lote de operações: '{input_path}'...")
    

    df = pd.read_csv(input_path)
    
 
    colunas_numericas = ['quantidade', 'preco_anterior', 'preco_atual', 'pnl_reportado']
    

    colunas_presentes = [c for c in colunas_numericas if c in df.columns]
    df[colunas_presentes] = df[colunas_presentes].fillna(0.0)
    
    if 'ativo' in df.columns:
        df['ativo'] = df['ativo'].fillna('UNKNOWN')
    else:
        df['ativo'] = 'UNKNOWN'

 
    logging.info("Processando vetorização do P&L Teórico e Diferenças...")
    
 
    df['pnl_calculado'] = (df['preco_atual'] - df['preco_anterior']) * df['quantidade']
    
   
    df['diferenca_abs'] = np.abs(df['pnl_calculado'] - df['pnl_reportado'])

  
    logging.info("Aplicando thresholds de risco estabelecidos...")
    
    condicoes = [
        df['diferenca_abs'] < 1.00,
        (df['diferenca_abs'] >= 1.00) & (df['diferenca_abs'] <= 100.00),
        df['diferenca_abs'] > 100.00
    ]
    status_risco = ['OK', 'WARNING', 'CRITICAL']
    
    df['status'] = np.select(condicoes, status_risco, default='UNKNOWN')

   
    mascara_auditoria = df['status'].isin(['WARNING', 'CRITICAL'])
    df_auditoria = df[mascara_auditoria]
    
    logging.info(f"Gerando artefato de auditoria compliance: {output_path} ({len(df_auditoria)} ocorrências)")
    df_auditoria.to_csv(output_path, index=False)

    logging.info("Consolidando matriz de risco por ativo...")
    

    resumo = df.groupby(['ativo', 'status']).size().unstack(fill_value=0)
    
    
    for s in status_risco:
        if s not in resumo.columns:
            resumo[s] = 0
            
 
    resumo['TOTAL_ERROS'] = resumo['WARNING'] + resumo['CRITICAL']
    

    resumo = resumo.sort_values(by=['CRITICAL', 'TOTAL_ERROS'], ascending=[False, False])
    
    return resumo


if __name__ == "__main__":
    import io
    
    mock_csv_data = io.StringIO('''id_transacao,ativo,quantidade,preco_anterior,preco_atual,pnl_reportado
1,PETR4,1000,30.00,31.00,1000.00
2,VALE3,500,65.00,64.00,-500.00
3,ITUB4,2000,28.50,29.00,990.00
4,BBDC4,10000,14.00,13.50,-4000.00
5,WEGE3,300,40.00,42.00,500.00
6,PETR4,5000,30.50,31.00,2300.00
7,MGLU3,100000,2.10,2.00,-9500.00
8,B3SA3,4000,11.20,11.50,1100.00
''')
    
    nome_arquivo_base = 'base_operacoes.csv'
    

    df_mock = pd.read_csv(mock_csv_data)
    df_mock.to_csv(nome_arquivo_base, index=False)
    
    print("\n[SYSTEM] Inicializando Engine de Reconciliação...")
    
    resultado_risco = processar_reconciliacao(input_path=nome_arquivo_base)
    
    print("\n" + "="*60)
    print("[ RELATORIO DE EXPOSICAO ]: ATIVOS COM MAIOR INCIDENCIA DE ERROS")
    print("="*60)
    if not resultado_risco.empty:
        
        display_cols = ['OK', 'WARNING', 'CRITICAL', 'TOTAL_ERROS']
        print(resultado_risco[display_cols].head(10))
    print("="*60 + "\n")
    logging.info("Processo finalizado com sucesso. Dados de auditoria gravados.")
