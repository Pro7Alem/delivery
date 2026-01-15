from database import get_conn

def criar_tabelas():
    with get_conn() as conn:
        cur = conn.cursor()

        '''ENDEREÇOS
        cur.execute("""
            CREATE TABLE IF NOT EXISTS addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                street TEXT NOT NULL,
                number TEXT,
                district TEXT,
                city TEXT NOT NULL,
                reference TEXT,
                latitude REAL,
                longitude REAL
            )
        """)
'''
        '''CARDÁPIO
        cur.execute("""
            CREATE TABLE IF NOT EXISTS menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                elements TEXT NOT NULL
            )
        """)
'''
        '''FUNCIONÁRIOS
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT,
                active INTEGER NOT NULL DEFAULT 1,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL
            )
        """)
'''
        '''MOTOBOYS
        cur.execute("""
            CREATE TABLE IF NOT EXISTS couriers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                active INTEGER NOT NULL DEFAULT 1
            )
        """)
'''
        '''PATRIMÔNIO
        cur.execute("""
            CREATE TABLE IF NOT EXISTS company_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                value INTEGER NOT NULL,
                acquired_at INTEGER NOT NULL,
                notes TEXT
            )
        """)
'''
        '''PEDIDOS
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                finished_at INTEGER,
                address_id INTEGER NOT NULL,
                customer_name TEXT,
                customer_phone TEXT,
                total_value INTEGER NOT NULL,
                delivery_fee INTEGER NOT NULL DEFAULT 0,
                payment_method TEXT,
                notes TEXT,
                FOREIGN KEY (address_id) REFERENCES addresses(id)
            )
        """)
'''
        '''ITENS DO PEDIDO
        cur.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                menu_item_id INTEGER,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price INTEGER NOT NULL,
                checked INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
            )
        """)
'''
        '''VIAGENS
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                started_at INTEGER,
                finished_at INTEGER,
                courier_id INTEGER,
                maps_url TEXT,
                FOREIGN KEY (courier_id) REFERENCES couriers(id)
            )
        """)
'''
        '''PEDIDOS DA VIAGEM
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trip_orders (
                trip_id INTEGER NOT NULL,
                order_id INTEGER NOT NULL,
                PRIMARY KEY (trip_id, order_id),
                FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
        """)
'''

        # FINANCEIRO
        cur.execute("""
            CREATE TABLE IF NOT EXISTS financial_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                value_cents INTEGER NOT NULL,
                description TEXT,
                ref_id INTEGER,
                created_at INTEGER NOT NULL
            )
        """)


        # ÍNDICES (PERFORMANCE)
        # Índice para buscar pedidos por endereço (útil para análise de regiões/bairros mais atendidos)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_address ON orders(address_id)")

        # Índice para filtrar pedidos por status (PENDING, PREPARING, DELIVERING, COMPLETED, CANCELLED)
        # Essencial para dashboards e listagens de "pedidos ativos"
        cur.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status)")

        # Índice para buscar todos os itens de um pedido específico (acelera a montagem de detalhes do pedido)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id)")

        # Índice para buscar todas as viagens de um motoboy específico (relatórios de entregas por entregador)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_trips_courier ON trips(courier_id)")

        # 1. Para filtrar por Pedido/Funcionário/Motoboy rapidamente
        cur.execute("CREATE INDEX IF NOT EXISTS idx_financial_ref ON financial_entries(ref_id)")

        # 2. Para gráficos de "Gastos por Categoria" (Pizza/Barras)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_financial_category ON financial_entries(category)")

        # 3. O MAIS IMPORTANTE: Para filtros de data (Hoje, Últimos 7 dias, Mensal)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_financial_date ON financial_entries(created_at)")

        conn.commit()
        print("✅ Todas as tabelas criadas com sucesso!")

criar_tabelas()