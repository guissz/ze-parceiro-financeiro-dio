# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `transacoes.json` | JSON | Armazenar o saldo atual e o histórico de entradas e saídas de valores do usuário para monitoramento em tempo real. |
| `diretrizes.txt` | TXT | Fornecer as regras de comportamento, tom de voz (foco na Geração Z) e limites de atuação para a IA. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Foram criados dados simulados na pasta `data/` com transações fictícias de entradas (como freelas) e saídas (como rolês e delivery) para representar a realidade financeira do público-alvo. Esses dados são atualizados dinâmicamente pelo código à medida que o usuário registra novas movimentações.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos da pasta `data` são carregados pelo código em Python no início da sessão e lidos/atualizados a cada nova interação do usuário no chat.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

O conteúdo de `transacoes.json` e as regras do `diretrizes.txt` são injetados dinamicamente no contexto do System Prompt enviado à API do Google Gemini, garantindo que a LLM conheça o saldo e o histórico recente antes de responder.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Diretrizes: Você é um assistente financeiro empático e descontraído para a Geração Z. Zero julgamento. Use emojis e linguagem leve.

Dados Atuais do Usuário:
- Nome: Guilherme
- Saldo atual: R$ 450,00

Últimas transações:
- 2026-06-01 | Entrada | R$ 1.200,00 | Freela de Design (Renda)
- 2026-06-02 | Saída | R$ 450 | Rolê no bar (Lazer)
- 2026-06-03 | Saída | R$ 35,50 | iFood (Delivery)

Mensagem do Usuário: "Gatei 50 conto na Steam hoje"
...
```