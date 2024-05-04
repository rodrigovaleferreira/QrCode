import sqlite3
import qrcode

def generate_qr_codes():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Selecionar todos os nomes ativos no banco de dados
    c.execute('SELECT nome FROM nomes WHERE status = "ativo"')
    nomes = c.fetchall()

    # Endereço local do servidor Flask
    endereco_local = 'http://127.0.0.1:5000/'

    # Para cada nome, gerar um código QR e salvar como um arquivo PNG
    for nome in nomes:
        url = f"{endereco_local}qrcode/{nome[0]}"  # Constrói a URL com o endereço local
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"qrcodes/{nome[0]}.png")

    # Fechar a conexão com o banco de dados
    conn.close()

if __name__ == '__main__':
    generate_qr_codes()
