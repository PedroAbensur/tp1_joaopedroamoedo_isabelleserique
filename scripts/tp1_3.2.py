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
conn.autocommit = True

# Cria novo banco de dados
cur.execute("CREATE DATABASE IF NOT EXISTS tp1db;")
create_query = [
    '''
    CREATE TABLE IF NOT EXISTS product(
    product_id INT UNIQUE NOT NULL,
    asin VARCHAR(20),
    title VARCHAR(500),
    product_group VARCHAR(20),
    salesrank INT,
    PRIMARY KEY(asin)
    );
    ''',
    '''
    CREATE TABLE IF NOT EXISTS similar_prod(
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
    CREATE TABLE IF NOT EXISTS reviews(
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
    '''
]

# Finaliza conexão e fecha cursor
cur.close()
conn.close()

class product:
    def __init__(self, id, asin, title, group, salesrank):
        self.id = id
        self.asin = asin
        self.title = title
        self.group = group
        self.salesrank = salesrank

    def print_product(self):
        print("=====================================================")
        print(f"id: {self.id}")
        print(f"asin: {self.asin}")
        print(f"title: {self.title}")
        print(f"group: {self.group}")
        print(f"salesrank: {self.salesrank}")

class similar:
    def __init__(self, asin_product, asin_similar):
        self.asin_product = asin_product
        self.asin_similar = asin_similar

    def print_similar(self):
        print("=====================================================")
        print(f"asin_product: {self.asin_product}")
        print(f"asin_similar: {self.asin_similar}")

class category:
    def __init__(self, id, name, parent_id):
        self.id = id
        self.name = name
        self.parent_id = parent_id

    def print_category(self):
        print("=====================================================")
        print(f"id: {self.id}")
        print(f"name: {self.name}")
        print(f"parent_id: {self.parent_id}")

class review:
    def __init__(self, asin_product, customer_id, review_date, rating, votes, helpful):
        self.asin_product = asin_product
        self.customer_id = customer_id
        self.review_date = review_date
        self.rating = rating
        self.votes = votes
        self.helpful = helpful
    
    def print_reviews(self):
        print("=====================================================")
        print(f"asin_product: {self.asin_product}")
        print(f"customer_id: {self.customer_id}")
        print(f"review_date: {self.rating}")
        print(f"votes: {self.votes}")
        print(f"helpful = {self.helpful}")

class catprod:
    def __init__(self, asin_product, cat_id):
        self.asin_product = asin_product
        self.cat_id = cat_id
    
    def print_catprod(self):
        print("=====================================================")
        print(f"asin_product: {self.asin_product}")
        print(f"cat_id = {self.cat_id}")

f = open("amazon-meta.txt", "+r")
f.readline() #Desconsidera "comment"
items = f.readline().split()[2]
f.readline() #Pula linha vazia"

#Lendo os produtos individualmente
for _ in range(int(items)):
    id = f.readline().split()[1]
    asin = f.readline().split()[1]
    line = f.readline().split()
    if(line[0] == 'discontinued'):
        prod = product(id, asin, 'NULL', 'NULL', 'NULL')
    else:
        #Lendo características do produto
        title = ' '.join(line[1:]).replace("'","''")
        group = f.readline().split()[1]
        salesrank = f.readline().split()[1]
        prod = product(id, asin, title, group, salesrank)

        #Lendo similares ao produto
        line = f.readline().split()
        similar_list = line[2:]
        for i in range(int(line[1])):
            sim = similar(prod.asin, similar_list[i])

        #Lendo categorias (mãe e filhas) do produto 
        line = f.readline().split()[1]
        cat_line_qtd = int(line)
        for _ in range(cat_line_qtd):
            line = f.readline().replace("\n","").split('|')
            parent_id = 'NULL'
            for cat_str in line[1:]:
                cat_parts = cat_str.split('[')
                cat = category(cat_parts[1][:-1], cat_parts[0], parent_id)
                parent_id = cat_parts[1][:-1]
                cp = catprod(prod.asin, cat.id) #Tupla CatProd (prod_asin, cat_id)!
        
        #Lendo reviews do produto
        line = f.readline() 
        rev = line.strip("reviews: total: ")
        rev_linha = rev.split()
        n_rev = (int) (rev_linha[2])

        for r in range(n_rev):
            line = f.readline() 
            rev_content = line.split()
            review_date = rev_content[0]
            customer_id = rev_content[2]
            rating = rev_content[4]
            votes = rev_content[6]
            helpful = rev_content[8]
            revi = review(asin, customer_id, review_date, rating, votes, helpful)