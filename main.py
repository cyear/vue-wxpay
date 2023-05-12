from flask import Flask, request
import sqlite3, time, requests, json
import hashlib
from urllib.parse import urlencode

notify_url = "https://www.alywlzf.com/SDK/notify_url.php"
return_url = "http://0.0.0.0:8080/#/return"

class AlipaySubmit:
    def __init__(self, alipay_config):
        self.alipay_config = alipay_config
        self.alipay_gateway_new = self.alipay_config['apiurl'] + 'submit.php'
        self.alipay_qrcode = self.alipay_config['apiurl'] + 'qrcode.php?'

    def build_request_mysign(self, para_sort):
        prestr = '&'.join([k + '=' + str(para_sort[k]) for k in sorted(para_sort)])
        mysign = hashlib.md5((prestr + self.alipay_config['key']).encode('utf-8')).hexdigest()
        return mysign

    def build_request_para(self, para_temp):
        para_filter = {k: v for k, v in para_temp.items() if v and k != 'sign' and k != 'sign_type'}
        para_sort = {k: para_filter[k] for k in sorted(para_filter)}
        mysign = self.build_request_mysign(para_sort)
        para_sort['sign'] = mysign
        para_sort['sign_type'] = self.alipay_config['sign_type'].upper().strip()
        return para_sort

    def build_request_para_to_string(self, para_temp):
        para = self.build_request_para(para_temp)
        request_data = urlencode(para)
        return request_data

    def build_request_form(self, para_temp, method='POST', button_name='正在跳转'):
        para = self.build_request_para(para_temp)
        res = requests.post(self.alipay_gateway_new, json=para).text
        return res

    def build_request_url(self, para_temp):
        request_data = self.build_request_para(para_temp)
        url = self.alipay_qrcode + urlencode(request_data)
        return url


alipay_config = {
    # 商户ID
    'partner': 自填,
    # 商户KEY
    'key': 自填,
    # 签名方式
    'sign_type': 'MD5',
    # 字符编码格式
    'input_charset': 'utf-8',
    # 访问模式
    'transport': 'http',
    # 支付API地址
    'apiurl': 'https://ypay.alywlzf.com/'
}

def initialize_db():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    
    # 判断是否已经存在商品表
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='product'")
    table_exists = c.fetchone()
    
    # 如果不存在，则创建商品表
    if not table_exists:
        c.execute('''CREATE TABLE product
                     (n TEXT NOT NULL UNIQUE,
                      title TEXT NOT NULL,
                      price TEXT NOT NULL,
                      vipPrice TEXT NOT NULL,
                      shopDesc TEXT NOT NULL,
                      delivery TEXT NOT NULL,
                      shopName TEXT NOT NULL,
                      imgUrl TEXT NOT NULL)''')
        conn.commit()
    
    conn.close()

def add_product(id, title, price, vipPrice, shopDesc, delivery, shopName, imgUrl):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO product (n, title, price, vipPrice, shopDesc, delivery, shopName, imgUrl) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, title, price, vipPrice, shopDesc, delivery, shopName, imgUrl))
    except:
        print(id, "存在")
        conn.close()
        return False
    conn.commit()
    conn.close()
    return True

def get_products():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute('SELECT n, title, price, vipPrice, shopDesc, delivery, shopName, imgUrl FROM product')
    products = c.fetchall()
    conn.close()
    product = []
    for i in products:
        (id, title, price, vipPrice, shopDesc, delivery, shopName, imgUrl) = i
        product.append({
            "id": id,
            "title": title,
            "price": price,
            "vipPrice": vipPrice,
            "shopDesc": shopDesc,
            "delivery": delivery,
            "shopName": shopName,
            "imgUrl": imgUrl,
        })
    return product

def get_product_by_id(id):
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM product WHERE n = ?", (id,))
    product = c.fetchone()
    conn.close()
    return product


initialize_db()

add_product(
    id=1,
    imgUrl='//img10.360buyimg.com/n2/s240x240_jfs/t1/210890/22/4728/163829/6163a590Eb7c6f4b5/6390526d49791cb9.jpg!q70.jpg',
    title='活蟹】湖塘煙雨 阳澄湖大闸蟹公4.5两 母3.5两 4对8只 鲜活生鲜螃蟹现货水产礼盒海鲜水',
    price='388',
    vipPrice='378',
    shopDesc='自营',
    delivery='厂商配送',
    shopName='阳澄湖大闸蟹自营店>',
)
add_product(
    id=2,
    imgUrl='//img10.360buyimg.com/n2/s240x240_jfs/t1/210890/22/4728/163829/6163a590Eb7c6f4b5/6390526d49791cb9.jpg!q70.jpg',
    title='测试',
    price='0.01',
    vipPrice='0.01',
    shopDesc='自营',
    delivery='包邮',
    shopName='🖤自营店>',
)

app = Flask(__name__)

@app.route('/buy', methods=['POST', 'OPTION'])
def buy():
    data = request.get_json()
    print(data)
    id, title, price, vipPrice, shopDesc, delivery, shopName, imgUrl = get_product_by_id(data["id"])
    #res = requests.post("http://0.0.0.0:8080/SDK/buy", data=f"type=wxpay&WIDsubject={title.encode('utf-8')}&WIDtotal_fee={vipPrice}&WIDout_trade_no={int(time.time()*10)}").text
    #print(res)
    out_trade_no = int(time.time()*100)
    type = "wxpay"
    name = title.encode("UTF-8").decode()
    money = vipPrice
    sitename = "一个🖤商店"
    parameter = {
        "pid": 1495,
        "type": type,
        "notify_url": notify_url,
        "return_url": return_url,
        "out_trade_no": out_trade_no,
        "name": name,
        "money": money,
        "sitename": sitename
    }
    print(parameter)
    alipay_submit = AlipaySubmit(alipay_config)
    res = alipay_submit.build_request_form(parameter)
    print(res)
    return "https://ypay.alywlzf.com" + res[30:-11]
    #return 'Success'

@app.route('/get', methods=['GET', 'OPTION'])
def get():
    return get_products()

if __name__ == '__main__':
    print("return url:", return_url)
    app.run(host='0.0.0.0', port=8079, debug=True)
