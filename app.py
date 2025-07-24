from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_VDS(vin):
    url = 'https://thuxe.vn/'
    data = {'vin': vin}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://thuxe.vn/',
        'Origin': 'https://thuxe.vn'
    }

    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        search_box = soup.find("p", class_="vin-result")
        if not search_box:
            return None

        VDS = search_box.text[3:]  # Bỏ 3 ký tự đầu
        parts = VDS.rsplit(' ', 2)  # Model, Year, Country
        if len(parts) != 3:
            return None
        return {"model": parts[0], "year": parts[1], "country": parts[2]}
    except Exception as e:
        return None

@app.route("/")
def home():
    return "VIN Lookup API đang chạy!"

@app.route("/lookup", methods=["GET"])
def lookup():
    vin = request.args.get("vin")
    if not vin:
        return jsonify({"error": "Missing VIN"}), 400

    result = get_VDS(vin)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Không tìm thấy hoặc lỗi"}), 404
