# 기술적 분석 지표 계산을 위한 전략 모듈
def calculate_moving_average(prices, window):
    # 최근 가격 리스트를 받아 평균을 산출함
    return sum(prices[-window:]) / window

def is_buy_signal(current, ma):
    # 골든크로스 신호 판단
    return current > ma

def is_sell_signal(current, buy_price, target_rate):
    # 목표 수익 도달 여부 판단
    return current >= buy_price * (1 + target_rate)
