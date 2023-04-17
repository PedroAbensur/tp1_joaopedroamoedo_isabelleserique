import psycopg2

# Conexão Default Postgres Database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="postgres"
)

# Objeto de Cursor
cur = conn.cursor()
# conn.autocommit = True

# Cria novo banco de dados
# cur.execute("CREATE DATABASE tp1db;")
create_query = [
    '''
    CREATE TABLE IF NOT EXISTS product(
    product_id INT UNIQUE NOT NULL,
    asin VARCHAR(20),
    title VARCHAR(500),
    product_group VARCHAR(300),
    salesrank INT,
    PRIMARY KEY(asin)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS similarprod(
    asin_product VARCHAR(20),
    asin_similar VARCHAR(20),
    PRIMARY KEY (asin_product, asin_similar),
    FOREIGN KEY (asin_product)
    REFERENCES product (asin)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS category(
    cat_id INT,
    name VARCHAR(200),
    parent_id INT,
    PRIMARY KEY (cat_id),
    FOREIGN KEY (parent_id)
    REFERENCES category (cat_id)
    );

    ''',
    '''
    CREATE TABLE IF NOT EXISTS catprod(
    asin_prod VARCHAR(20),
    cat_id INT,
    PRIMARY KEY (asin_prod, cat_id),
    FOREIGN KEY (asin_prod)
    REFERENCES product(asin),
    FOREIGN KEY (cat_id)
    REFERENCES category (cat_id)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS review(
    review_id SERIAL,
    asin_product VARCHAR(20) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    review_date DATE,
    rating INT,
    votes INT,
    helpful INT,
    PRIMARY KEY (review_id),
    FOREIGN KEY (asin_product)
    REFERENCES product (asin)
    );
    ''']

for query in create_query:
    cur.execute(query)

conn.commit()

class product:
    def __init__(self, id, asin, title, group, salesrank):
        if(title != 'NULL'):
            title = "'" + title + "'"
            group = "'" + group + "'"

        self.id = id
        self.asin = "'" + asin + "'"
        self.title = title
        self.group = group
        self.salesrank = salesrank

    def insert_product(self, cur):
        values = f"{self.id},{self.asin}, {self.title}, {self.group},{self.salesrank}"
        query = f"INSERT INTO product VALUES ({values});"

        try:
            cur.execute(query)
            conn.commit()
        except Exception as err:
            print(err)

class similar:
    def __init__(self, asin_product, asin_similar):
        self.asin_product = asin_product
        self.asin_similar = "'" + asin_similar + "'"
    
    def insert_similar(self, cur):
        values = f"{self.asin_product},{self.asin_similar}"
        query = f"INSERT INTO similarprod VALUES ({values});"
        try:
            cur.execute(query)
            conn.commit()
        except Exception as err:
            print(err)
            exit(-1)


class category:
    def __init__(self, id, name, parent_id):
        self.id = id
        self.name = "'" + (name.replace("'", "''")) + "'"
        self.parent_id = parent_id

    def insert_category(self, cur):
        values = f"{self.id},{self.name},{self.parent_id}"
        query = f"INSERT INTO category VALUES ({values}) ON CONFLICT (cat_id) DO NOTHING;"
        try:
            cur.execute(query)
            conn.commit()
        except Exception as err:
            print(err)
            exit(-1)


class review:
    def __init__(self, asin_product, customer_id, review_date, rating, votes, helpful):
        self.asin_product = asin_product
        self.customer_id = "'" + customer_id + "'"
        self.review_date = "'" + review_date + "'"
        self.rating = rating
        self.votes = votes
        self.helpful = helpful

    def insert_review(self, cur):
        columns = "asin_product, customer_id, review_date, rating, votes, helpful"
        values = f"{self.asin_product},{self.customer_id},{self.review_date}, {self.rating}, {self.votes}, {self.helpful}"
        query = f"INSERT INTO review ({columns}) VALUES ({values});"
        try:
            cur.execute(query)
            conn.commit()
        except Exception as err:
            print(err)
            exit(-1)

class catprod:
    def __init__(self, asin_product, cat_id):
        self.asin_product = asin_product
        self.cat_id = cat_id
    
    def insert_catprod(self, cur):
        values = f"{self.asin_product},{self.cat_id}"
        query = f"INSERT INTO catprod VALUES ({values}) ON CONFLICT (asin_prod, cat_id) DO NOTHING;"
        try:
            cur.execute(query)
            conn.commit()
        except Exception as err:
            print(err)
            exit(-1)

f = open("amazon-meta.txt", "+r")
f.readline()  # Pula comentário
items = f.readline().split()[2]
f.readline()  # Ignora linha vazia
for _ in range(int(items)):
    id = f.readline().split()[1]
    asin = f.readline().split()[1]
    line = f.readline().split()
    if (line[0] == 'discontinued'):
        prod = product(id, asin, 'NULL', 'NULL', 'NULL')
        prod.insert_product(cur)
    else:
        title = ' '.join(line[1:]).replace("'", "''")
        group = f.readline().split()[1]
        salesrank = f.readline().split()[1]
        prod = product(id, asin, title, group, salesrank)
        prod.insert_product(cur)

        # Lendo similares ao produto
        line = f.readline().split()
        similar_list = line[2:]
        for i in range(int(line[1])):
            sim = similar(prod.asin, similar_list[i])
            sim.insert_similar(cur)

        # Lendo Categorias do produto
        line = f.readline().split()[1]
        cat_line_qtd = int(line)
        for _ in range(cat_line_qtd):
            line = f.readline().replace("\n", "").split('|')
            parent_id = 'NULL'
            for cat_str in line[1:]:
                cat_parts = cat_str.split('[')
                if(len(cat_parts) > 2):
                    for i in range(1,len(cat_parts)-1):
                        cat_parts[i] = '[' + cat_parts[i]
                cat = category(cat_parts[-1][:-1], ''.join(cat_parts[0:-1]), parent_id)
                cat.insert_category(cur)
                parent_id = cat_parts[1][:-1]
                # catprod tuple
                cp = catprod(prod.asin, cat.id)
                cp.insert_catprod(cur)

        # Lendo reviews dos produtos
        line = f.readline()
        rev = line.strip("reviews: total: ")
        rev_linha = rev.split()
        n_rev = (int)(rev_linha[2])

        for r in range(n_rev):
            line = f.readline()
            rev_content = line.split()
            review_date = rev_content[0]
            customer_id = rev_content[2]
            rating = rev_content[4]
            votes = rev_content[6]
            helpful = rev_content[8]
            revi = review(prod.asin, customer_id, review_date,
                          rating, votes, helpful)
            revi.insert_review(cur)

    f.readline()

# Finaliza conexão e fecha cursor
cur.close()
conn.close()