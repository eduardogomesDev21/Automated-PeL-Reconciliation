# 🏎️ Automated P&L Reconciliation Engine

## 📊 Visão Geral (The "Finance" Side)

Este motor de reconciliação foi desenvolvido para automatizar a validação de P&L (Profit & Loss) entre sistemas de Front Office e Back Office.  

Em ambientes de alta frequência ou grandes volumes de tesouraria, divergências de centavos podem esconder erros operacionais graves.

### O que este projeto resolve:
- **Cálculo de Mark-to-Market (MtM):** Validação em tempo real do P&L teórico  
- **Classificação de Risco:** Identificação imediata de erros Críticos, Warnings e variações aceitáveis  
- **Audit Trail:** Geração automática de relatórios de divergência para Compliance e Auditoria  

---

## 💻 Diferenciais Técnicos (The "Dev" Side)

Para profissionais de tecnologia, o foco deste motor é a escalabilidade e resiliência.

- **Vetorização com NumPy/Pandas:** Utiliza `np.select` para processamento paralelo, evitando loops `for` e garantindo performance sub-milissegundo em 10k+ registros  
- **Sanitização de Dados:** Tratamento robusto de `NaN` (valores nulos) e tipagem forçada para evitar quebras em dados corrompidos  
- **Logging Industrial:** Implementação da biblioteca `logging` para monitoramento de processos em background (servidor)  

---

## 🚀 Como Executar

### Instale as dependências:
```bash
pip install -r requirements.txt
```
Rode o motor:
python pnl_recon_engine.py

📈 Output e Resultados

O sistema gera um Exposure Report consolidado.

Abaixo, o resultado da execução processando operações de ativos como PETR4, VALE3 e MGLU3:

<img width="1061" height="498" alt="image" src="https://github.com/user-attachments/assets/2b308352-3584-46a5-b2c5-533fdbeea266" />


⚙️ Thresholds de Risco Configurados
| Status   | Diferença Absoluta  | Ação                                            |
| -------- | ------------------- | ----------------------------------------------- |
| OK       | < R$ 1,00           | Ignorar (Variação de arredondamento)            |
| WARNING  | R$ 1,00 - R$ 100,00 | Revisão em D+1 (Taxas/Custos)                   |
| CRITICAL | > R$ 100,00         | Intervenção Imediata (Erro de Preço/Quantidade) |

🛠️ Tecnologias Utilizadas
Python 3.x
Pandas – Manipulação e agregação de dados
NumPy – Cálculos matemáticos de alta performance
Logging – Rastreabilidade operacional
👨‍💻 Autor

Desenvolvido por Eduardo Gomes
Foco em Automação, Dados e Performance Financeira
