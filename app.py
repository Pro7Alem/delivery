from flask import Flask, render_template, request, redirect, url_for
from database import exec_command
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novo_pedido')
def novo_pedido():
    return render_template('novo_pedido.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.post('/lancar')
def criar_pedido():
    cliente = request.form.get('cliente')
    rua = request.form.get('rua')
    numero = request.form.get('numero', '').strip()
    bairro = request.form.get('bairro')
    valor_total = request.form.get('valor', '').strip()
    notas = request.form.get('notas')

    # Converte o valor de R$ para centavos (inteiro)
    valor_centavos = int(float(valor_total) * 100)

    # Timestamp atual em s (sistema utiliza epoch)
    agora = int(time.time())

    # 1. Insere o endereço e pega o ID
    addr_id = exec_command(
        "INSERT INTO addresses (street, number, district, city) VALUES (?, ?, ?, ?)",
        (rua, numero, bairro, "BETIM")
    )

    # 2. Insere o pedido usando o addr_id
    exec_command(
        """INSERT INTO orders
               (status, created_at, address_id, customer_name, total_value, notes)
           VALUES (?, ?, ?, ?, ?, ?)""",
        ("PENDING", agora, addr_id, cliente, valor_centavos, notas)
    )

    return redirect(url_for('index'))

@app.post('/admin/add_courier')
def add_motoboy():
    nome = request.form.get('nome')
    telefone = request.form.get('telefone', '').strip()

    exec_command("INSERT INTO couriers (name, phone, active) VALUES (?, ?, ?)",
                 (nome, telefone, 1))

    return redirect(url_for('admin'))

@app.post('/admin/add_employee')
def add_funcionario():
    nome = request.form.get('nome')
    cargo = request.form.get('cargo')

    agora = int(time.time())

    exec_command("INSERT INTO employees (name, role, active, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                 (nome, cargo, 1, agora, agora))

    return redirect(url_for('admin'))

@app.post('/admin/add_product')
def add_product():
    nome = request.form.get('nome')
    preco = request.form.get('preco', '').strip()
    elementos = request.form.get('elementos')

    preco_centavos = int(float(preco) * 100)

    agora = int(time.time())

    exec_command("INSERT INTO menu_items (name, price, created_at, updated_at, active, elements) VALUES (?, ?, ?, ?, ?, ?)",
                    (nome, preco_centavos, agora, agora, 1, elementos))

    return redirect(url_for('admin'))


@app.post('/admin/add_c_assets')
def add_c_asset():
    nome = request.form.get('nome')
    categoria = request.form.get('categoria')
    preco = request.form.get('preco', '').strip()
    notas = request.form.get('notas')

    preco_centavos = int(float(preco) * 100)

    agora = int(time.time())

    exec_command(
        "INSERT INTO company_assets (name, category, value, acquired_at, notes) VALUES (?, ?, ?, ?, ?)",
        (nome, categoria, preco_centavos, agora, notas))

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)