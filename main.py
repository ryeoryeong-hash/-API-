import datetime
import os

# [시스템 설정]
class TradingSystemConfig:
    SYMBOL = "005930"             # 매매 종목
    TARGET_PROFIT_RATE = 0.03     # 목표 수익률 3%
    MOVING_AVG_WINDOW = 5         # 5일 이동평균선

# [자동매매 엔진]
class AutoTradingSystem:
    def __init__(self):
        self.config = TradingSystemConfig()
        self.log_file = "trading_log.csv"
        # 로그 파일 없으면 헤더 생성
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("timestamp,symbol,type,price,profit\n")

    def get_moving_average(self, prices):
        # 이동평균선 산출
        if len(prices) < self.config.MOVING_AVG_WINDOW: return None
        return sum(prices[-self.config.MOVING_AVG_WINDOW:]) / self.config.MOVING_AVG_WINDOW

    def execute_trade(self, trade_type, price):
        # 거래 로그 기록
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp},{self.config.SYMBOL},{trade_type},{price},None\n")
        print(f"[거래 실행] {trade_type} 주문 완료: {price}원")

    def run(self, market_prices, avg_buy_price):
        # 매매 로직 판단
        current_price = market_prices[-1]
        ma = self.get_moving_average(market_prices)
        if ma and current_price > ma:
            self.execute_trade("BUY", current_price)
        elif current_price >= avg_buy_price * (1 + self.config.TARGET_PROFIT_RATE):
            self.execute_trade("SELL", current_price)

if __name__ == "__main__":
    bot = AutoTradingSystem()
    bot.run([71000, 71500, 72000, 72500, 73000], 71000)
