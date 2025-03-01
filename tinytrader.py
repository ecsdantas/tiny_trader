import os
import time
import json
from datetime import datetime
from binance.client import Client

# Bot de autotrade
class BinanceTradingBot:
    def __init__(self):
        # Parâmetros gerais
        self.symbol = "ETHUSDT"         # Moeda que será negociada ("ETHUSDT", "BTCUSDT", etc)
        self.capital = 1000             # Capital inicial em USDT
        self.investment_amount = 30     # Valor máximo por compra
        self.tax_rate = 0.001           # Taxa sobre cada venda (0.1% da binance)
        self.min_drop_to_buy = 0.15     # Queda mínima para considerar uma compra
        self.profit_threshold = 0.05    # Percentual mínimo para vender com lucro
        self.max_consecutive_buys = 9   # Número máximo de compras seguidas
        self.check_interval = 60        # Intervalo de verificação (em segundos)
        # Parametros internos
        self.transactions = []          # Histórico de compras
        self.consecutive_buys = 0       # Contador de compras seguidas
        # Inicializar cliente da Binance
        # Credenciais para Binance Testnet (obtenha as suas em: https://testnet.binance.vision/)
        self.client = Client(
            api_key=os.getenv("API_KEY"),
            api_secret=os.getenv("API_SECRET")
        )
        self.client.API_URL = 'https://testnet.binance.vision/api'
        # Arquivos para dados e log
        self.data_file = "bot_data.json"
        self.log_file = "bot_log.txt"
        self.prices_file = "bot_prices.txt"
        # Carregar dados anteriores (se existirem)
        self.load_data()
        print(f"Bot iniciado para {self.symbol}! Aguardando oportunidades...")

    def get_price(self):
        """ Obtém o preço atual da moeda na Binance Testnet """
        ticker = self.client.get_symbol_ticker(symbol=self.symbol)
        price = float(ticker['price'])
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.prices_file, "a") as f:
            f.write(f"[{timestamp}] {self.symbol}: {price}\n")
        return price

    def buy_crypto(self, price):
        """ Executa uma compra """
        crypto_to_buy = self.investment_amount / price
        self.capital -= self.investment_amount
        self.transactions.append((price, crypto_to_buy))
        self.consecutive_buys += 1
        self.save_data()
        self.log_transaction("Compra", price, crypto_to_buy)
        print(f"Comprado {crypto_to_buy:.6f} {self.symbol[:-4]} por ${price:.2f}")

    def sell_crypto(self, price):
        """ Executa uma venda """
        for transaction in self.transactions[:]:
            buy_price, crypto_amount = transaction
            if price > buy_price * (1 + self.profit_threshold):
                sale_value = crypto_amount * price * (1 - self.tax_rate)
                self.capital += sale_value
                self.transactions.remove(transaction)
                self.consecutive_buys = 0  # Resetar compras seguidas
                self.save_data()
                self.log_transaction("Venda", price, crypto_amount)
                print(f"Vendido {crypto_amount:.6f} {self.symbol[:-4]} por ${price:.2f}, saldo: ${self.capital:.2f}")

    def save_data(self):
        """ Salva dados do bot em um arquivo JSON """
        data = {k: v for k, v in self.__dict__.items() if not k.startswith("__") and not callable(v) and not k.startswith("client")}
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        """ Carrega dados do bot em um arquivo JSON """
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                for key, value in data.items():
                    setattr(self, key, value)
                print(f"Dados carregados com sucesso para {self.symbol}!")
        else:
            self.save_data()

    def log_transaction(self, action, price, amount):
        """ Registra transações em um arquivo separado """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {action}: {amount:.6f} {self.symbol[:-4]} a ${price:.2f}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)

    def run(self):
        """ Executa o bot de trading """
        last_price = None
        while True:
            current_price = self.get_price()
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Preço atual de {self.symbol}: ${current_price:.2f}")

            if last_price:
                # Verificar se o preço caiu mais que o limite para compra
                if (last_price - current_price) / last_price > self.min_drop_to_buy and self.consecutive_buys < self.max_consecutive_buys:
                    self.buy_crypto(current_price)

                # Verificar se o preço subiu para venda
                self.sell_crypto(current_price)

            last_price = current_price
            time.sleep(self.check_interval)
