import socket
from flask import Flask, render_template, request

app = Flask(__name__)

def currency_conversion_client_tcp(server_addr, source_currency, destination_currency, amount):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_addr)
        message = f"{source_currency} {destination_currency} {amount}"
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        return data.decode()

def currency_conversion_client_udp(server_addr, source_currency, destination_currency, amount):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"{source_currency} {destination_currency} {amount}"
    client_socket.sendto(message.encode(), server_addr)
    data, _ = client_socket.recvfrom(1024)
    client_socket.close()
    return data.decode()

available_currencies = ['INR', 'USD', 'AED', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CNY', 'SGD', 
                        'CHF', 'MYR', 'ZAR', 'BRL', 'RUB', 'KRW', 'THB', 'MXN', 'VND', 'IDR', 'SAR']

@app.route('/')
def index():
    return render_template('index.html', currencies=available_currencies)

@app.route('/convert', methods=['POST'])
def convert():
    source_currency = request.form['source_currency']
    destination_currency = request.form['destination_currency']
    amount = request.form['amount']
    protocol = request.form['protocol'] 

   
    server_ip = '192.168.210.228'
    server_port = 12345
    server_adr = (server_ip, server_port)

    
    if protocol == 'TCP':
        response = currency_conversion_client_tcp(server_adr, source_currency, destination_currency, amount)
    else:
        response = currency_conversion_client_udp(server_adr, source_currency, destination_currency, amount)

    
    return render_template('index.html', currencies=available_currencies, response=response)

if __name__ == '__main__':
    app.run(debug=True)
