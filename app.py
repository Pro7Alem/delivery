from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import exec_command, exec_query
import time
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/novo_pedido')
def novo_pedido():
    menu = exec_query("SELECT id, name, price FROM menu_items WHERE active = 1")
    return render_template('novo_pedido.html', menu=menu)

@app.route('/admin')
def admin():
    return render_template('admin.html')

def add_financial_entry(tipo, categoria, valor_cents, descricao, ref_id=None):
    agora = int(time.time())
    exec_command("INSERT INTO financial_entries (type, category, value_cents, description, ref_id, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                 (tipo, categoria, valor_cents, descricao, ref_id, agora))


@app.post('/lancar')
def criar_pedido():
    cliente = request.form.get('cliente')
    rua = request.form.get('rua')
    numero = request.form.get('numero', '').strip()
    bairro = request.form.get('bairro')
    notas = request.form.get('notas')

    # Recebe o JSON dos itens
    itens_json = request.form.get('itens_json')
    itens_front = json.loads(itens_json)

    agora = int(time.time())

    # 1. Insere o endereço
    addr_id = exec_command(
        "INSERT INTO addresses (street, number, district, city) VALUES (?, ?, ?, ?)",
        (rua, numero, bairro, "BETIM")
    )

    # 2. Busca os preços reais do banco e calcula o total
    total_centavos = 0
    itens_validados = []

    for item_front in itens_front:
        # Busca o item real no banco
        item_db = exec_query(
            "SELECT id, name, price FROM menu_items WHERE id = ? AND active = 1",
            (item_front['id'],)
        )

        if not item_db:
            # Se o item não existir ou estiver inativo, ignora
            continue

        item_real = item_db[0]
        qtd = int(item_front['quantity'])

        itens_validados.append({
            'id': item_real['id'],
            'name': item_real['name'],
            'price': item_real['price'],
            'quantity': qtd
        })

        total_centavos += item_real['price'] * qtd

    # 3. Insere o pedido com o valor REAL
    order_id = exec_command(
        """INSERT INTO orders
               (status, created_at, address_id, customer_name, total_value, notes)
           VALUES (?, ?, ?, ?, ?, ?)""",
        ("PENDING", agora, addr_id, cliente, total_centavos, notas)
    )

    # 4. Insere cada item validado
    for item in itens_validados:
        exec_command(
            """INSERT INTO order_items
                   (order_id, menu_item_id, name, quantity, unit_price)
               VALUES (?, ?, ?, ?, ?)""",
            (order_id, item['id'], item['name'], item['quantity'], item['price'])
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