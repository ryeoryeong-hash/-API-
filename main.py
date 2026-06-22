import datetime
import os


# [시스템 설정] 환경 정보 관리 클래스
class TradingSystemConfig:
    SYMBOL = "005930"  # 매매 대상 종목: 삼성전자
    TARGET_PROFIT_RATE = 0.03  # 목표 수익률 3% 설정
    MOVING_AVG_WINDOW = 5  # 5일 이동평균선 사용


# [자동매매 엔진] 시스템의 핵심 로직을 담당하는 클래스
class AutoTradingSystem:
    def __init__(self):
        self.config = TradingSystemConfig()  # 설정 정보 로드
        self.log_file = "trading_log.csv"  # 거래 로그 파일 경로 지정

        # 로그 파일 초기화: 데이터 파일이 없을 경우 헤더 자동 생성
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                f.write("timestamp,symbol,type,price,profit\n")  # CSV 헤더 구조

    def get_moving_average(self, prices):
        # 기술적 분석: 이동평균선 산출로 추세 판단 근거 마련
        if len(prices) < self.config.MOVING_AVG_WINDOW:
            return None  # 데이터 부족 시 계산 방지
        return sum(prices[-self.config.MOVING_AVG_WINDOW:]) / self.config.MOVING_AVG_WINDOW

    def execute_trade(self, trade_type, price):
        # 거래 기록: 실제 매매가 발생했을 때 로그 파일에 타임스탬프와 함께 기록
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp},{self.config.SYMBOL},{trade_type},{price},None\n"
        with open(self.log_file, "a") as f:  # 파일 이어쓰기 모드(Append) 사용
            f.write(log_entry)
        print(f"[거래 실행] {trade_type} 주문 완료: {price}원")

    def run(self, market_prices, avg_buy_price):
        # 시스템 핵심 엔진: 데이터 분석 후 매매 전략 실행
        current_price = market_prices[-1]
        ma = self.get_moving_average(market_prices)  # 추세 지표 산출

        print(f"현재가: {current_price} | 5일 이동평균: {ma}")

        # 전략 1: 골든크로스(Buy) - 상승 추세 전환 시 진입
        if ma and current_price > ma:
            print("전략 신호: 매수(Buy) - 골든크로스 감지")
            self.execute_trade("BUY", current_price)

        # 전략 2: 익절(Sell) - 수익률 3% 도달 시 기계적 매도
        elif current_price >= avg_buy_price * (1 + self.config.TARGET_PROFIT_RATE):
            print("전략 신호: 매도(Sell) - 목표 수익률 달성")
            self.execute_trade("SELL", current_price)

        else:
            print("전략 신호: 관망(Hold) - 매매 조건 미달")


# 시스템 가동
if __name__ == "__main__":
    bot = AutoTradingSystem()  # 시스템 객체 생성
    sample_data = [71000, 71500, 72000, 72500, 73000]  # 가상의 시장 시세 데이터
    bot.run(sample_data, avg_buy_price=71000)  # 알고리즘 시뮬레이션 가동
