from flask import Flask, render_template

app = Flask(__name__)

# 模拟数据，每个列表包含三个交易记录，已预先按金额从大到小排序
data = {
    '1 Minute': [{'name': 'Trader A', 'amount': 10000}, {'name': 'Trader B', 'amount': 9500}, {'name': 'Trader C', 'amount': 9000}],
    '2 Minutes': [{'name': 'Trader D', 'amount': 20000}, {'name': 'Trader E', 'amount': 19500}, {'name': 'Trader F', 'amount': 19000}],
    '5 Minutes': [{'name': 'Trader G', 'amount': 50000}, {'name': 'Trader H', 'amount': 49500}, {'name': 'Trader I', 'amount': 49000}],
    '10 Minutes': [{'name': 'Trader J', 'amount': 100000}, {'name': 'Trader K', 'amount': 95000}, {'name': 'Trader L', 'amount': 90000}],
    '20 Minutes': [{'name': 'Trader M', 'amount': 200000}, {'name': 'Trader N', 'amount': 195000}, {'name': 'Trader O', 'amount': 190000}],
    '30 Minutes': [{'name': 'Trader P', 'amount': 300000}, {'name': 'Trader Q', 'amount': 295000}, {'name': 'Trader R', 'amount': 290000}]
}

@app.route('/')
def home():
    return render_template('rankings.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
