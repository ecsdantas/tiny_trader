# 🚀 TinyTrader Bot - Binance    
Um bot de **auto-trade** para Binance, que compra e vende criptomoedas automaticamente com base em estratégias predefinidas. Implementado em **Python** usando a API oficial da Binance.  

## 📌 Recursos    
✅ Compra e vende ativos automaticamente baseado em regras definidas    
✅ Suporte a múltiplos pares de moedas (ex: **ETHUSDT**, **BTCUSDT**)  
✅ Configuração de parâmetros como capital inicial, taxa de compra/venda e tempo de verificação  
✅ Executável em **Railway**, **Google Colab**, **servidores na nuvem** ou **PC local**  

---

## 🛠️ **Instalação**    
**Clonar o repositório e instalar pré-requisitos**    
```bash
git clone https://github.com/ecsdantas/tiny_trader .
pip install -r requirements.txt
```

## 🔑 Defina suas chaves     
Obter chaves da api em: https://testnet.binance.vision/   
Rodar no Linux
```bash
export API_KEY="sua_api_key"
export API_SECRET="sua_api_secret"
```
ou no Windows
```bash
set API_KEY="sua_api_key"
set API_SECRET="sua_api_secret"
```

## ➡️ Rodar o script python   
```bash
python main.py
```

## ⚙️ Configuração de Estratégia    
Os parâmetros do bot podem ser ajustados no arquivo bot_data.json.Para modificar a moeda negociada, edite a entrada "symbol" no JSON.    

**Exemplo**: Alterar de Ethereum (ETH) para Bitcoin (BTC)    
```bash
{
    "symbol": "BTCUSDT",
    "capital": 1000,
    "investment_amount": 30,
    "tax_rate": 0.001,
    "min_drop_to_buy": 0.15,
    "profit_threshold": 0.05,
    "max_consecutive_buys": 9,
    "check_interval": 60
}
```

## 📂 Estrutura do projeto   
```python
📂 root
 ├── 📄 main.py                # Código principal do bot
 ├── 📄 config.py              # Configuração de parâmetros e API
 ├── 📄 bot_data.json          # Configurações da estratégia de trading (criado após primeira execução)
 ├── 📄 requirements.txt       # Dependências do projeto
 ├── 📄 README.md              # Documentação do projeto 🚀
```

## 📊 Parâmetros do Bot   
Os parâmetros podem ser ajustados para otimizar a estratégia de trading.    
| Parâmetro	| Descrição	| Padrão |
| --- | --- | --- |
| symbol | Par de moedas negociado | "ETHUSDT" |
| capital | Capital inicial em USDT | 1000 |
| investment_amount | Valor investido em cada compra | 30 |
| tax_rate | Taxa cobrada pela Binance por transação | 0.001 (0.1%) |
| min_drop_to_buy | Queda mínima para considerar uma compra | 0.15 (15%) |
| profit_threshold | Percentual mínimo de lucro antes de vender | 0.05 (5%) |
| max_consecutive_buys | Número máximo de compras seguidas | 9 |
| check_interval | Tempo entre verificações de preço (em segundos) | 60 |

