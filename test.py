import json

# stocks.json 파일을 읽어옵니다.
with open("stocks.json", "r") as file:
    data = json.load(file)

# NVDA와 AAPL 주식의 가격을 추출합니다.
for stock in data:
    if stock["name"] == "NVDA":
        nvda_price = stock["price"]
    elif stock["name"] == "AAPL":
        aapl_price = stock["price"]

print(f"NVDA 주식 가격: ${nvda_price:.2f}")
print(f"AAPL 주식 가격: ${aapl_price:.2f}")
