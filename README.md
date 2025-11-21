# Sistema de Clientes e Pedidos com Tkinter

Este projeto é uma aplicação desktop para gerenciamento de clientes e pedidos utilizando Python, Tkinter e SQLite.

## Como rodar

1. Certifique-se de ter Python 3.10+ instalado.
2. Execute o arquivo principal:
   ```bash
   python main.py

Na aba "IA / Análise", o usuário encontra um botão "Analisar Pedidos". Ao ser acionado, o sistema executa o seguinte fluxo:

Extração de Dados: O sistema busca no banco de dados SQLite os 5 últimos pedidos registrados.

Preparação do Resumo: Os dados dos pedidos (produtos, quantidades, valores) são formatados em um resumo textual.


Envio para IA (Ollama): Este resumo textual é enviado para o modelo de IA (configurado para usar o Ollama local) através de uma chamada de API, solicitando uma análise de mercado ou insights gerenciais.


Geração de Insights: A IA processa o texto e retorna insights como "produtos mais vendidos", "ticket médio recente" e "tendências de compra".


Exibição: O resultado textual da análise é exibido em um Text widget com rolagem na própria aba de Análise.

🛠️ Prompt Utilizado no utils.py:
O prompt base utilizado para guiar a análise da IA, mantido na função analisar_pedidos() dentro de utils.py, é o seguinte:

"Você é um analista de dados. Analise o seguinte resumo dos últimos 5 pedidos do sistema e forneça insights concisos, focando em: produtos mais vendidos em termos de quantidade e valor, e o valor médio das transações (ticket médio). Retorne apenas o resumo em texto."