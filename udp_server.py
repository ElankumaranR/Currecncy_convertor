import socket
import os

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = int(os.environ.get("PORT", 12345))  # Use the dynamic port assigned by Render

def currency(src, des, amt):
    rates = {
        'INR': 1.0,      # Indian Rupee
        'USD': 83.0,     # US Dollar
        'AED': 22.0,     # UAE Dirham
        'EUR': 88.0,     # Euro
        'GBP': 102.0,    # British Pound
        'JPY': 0.56,     # Japanese Yen
        'AUD': 53.0,     # Australian Dollar
        'CAD': 61.0,     # Canadian Dollar
        'CNY': 11.0,     # Chinese Yuan
        'SGD': 61.0,     # Singapore Dollar
        'CHF': 90.0,     # Swiss Franc
        'MYR': 17.8,     # Malaysian Ringgit
        'ZAR': 5.4,      # South African Rand
        'BRL': 16.0,     # Brazilian Real
        'RUB': 1.1,      # Russian Ruble
        'KRW': 0.063,    # South Korean Won
        'THB': 2.3,      # Thai Baht
        'MXN': 4.6,      # Mexican Peso
        'VND': 0.0034,   # Vietnamese Dong
        'IDR': 0.0054,   # Indonesian Rupiah
        'SAR': 22.0      # Saudi Riyal
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

# UDP Server setup
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))

    print(f"Server is listening on port {PORT}...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        print("Received from", addr)
        if not data:
            continue
        src, des, amt = data.decode().split()
        res = str(currency(src, des, amt))
        server_socket.sendto(res.encode(), addr)
