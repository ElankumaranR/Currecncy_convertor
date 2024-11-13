import socket

HOST = '0.0.0.0'
PORT = 12345

def currency(src, des, amt):
    rates = {
        'INR': 1.0, 'USD': 83.0, 'AED': 22.0, 'EUR': 88.0, 'GBP': 102.0, 'JPY': 0.56,
        'AUD': 53.0, 'CAD': 61.0, 'CNY': 11.0, 'SGD': 61.0, 'CHF': 90.0, 'MYR': 17.8,
        'ZAR': 5.4, 'BRL': 16.0, 'RUB': 1.1, 'KRW': 0.063, 'THB': 2.3, 'MXN': 4.6,
        'VND': 0.0034, 'IDR': 0.0054, 'SAR': 22.0
    }
    try:
        amt = float(amt)
    except ValueError:
        return "Invalid amount"

    if src in rates and des in rates:
        inr_value = amt * rates[src]
        result = inr_value / rates[des]
        return f"{amt} {src} = {result:.2f} {des}"
    else:
        return "Invalid currency codes"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f"Server is listening on port {PORT}...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        if not data:
            continue
        src, des, amt = data.decode().split()
        res = currency(src, des, amt)
        server_socket.sendto(res.encode(), addr)
