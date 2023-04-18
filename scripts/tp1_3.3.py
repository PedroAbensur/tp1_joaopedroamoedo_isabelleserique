import psycopg2
import os

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

def welcome_dashboard():
    print("DASHBOARD DE CONSULTAS\n\n")
    print("Escolha a consulta a ser feita:\n")
    print("a - Dado um produto, listar os 5 comentarios mais uteis e com maior avaliacao e os 5 comentarios mais uteis e com menor avaliacao.")
    print("b - Dado um produto, listar os produtos similares com maiores vendas do que ele.")
    print("c - Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada.")
    print("d - Listar os 10 produtos líderes de venda em cada grupo de produtos.")
    print("e - Listar os 10 produtos com a maior média de avaliações úteis positivas por produto.")
    print("f - Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto.")
    print("g - Listar os 10 clientes que mais fizeram comentários por grupo de produto.\n")
    print("h - Finalizar\n\n")

while (True):
    os.system('cls' if os.name == 'nt' else 'clear')

    welcome_dashboard()

    cons = input("Escolha uma consulta: ")
    os.system('cls' if os.name == 'nt' else 'clear')


    if (cons == 'a'):
        asin = input("Insira o ASIN do produto: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")
        try:

            consulta = f"(SELECT * FROM (SELECT * FROM review WHERE review.asin_product = '{asin}') AS aux  ORDER BY helpful DESC, rating DESC LIMIT 5) UNION"
            consulta += f"(SELECT * FROM (SELECT * FROM review WHERE review.asin_product = '{asin}') AS aux2 ORDER BY helpful ASC, rating ASC LIMIT 5)"
            cur.execute(consulta)

            colnames = [desc[0] for desc in cur.description]
            print(colnames)

            resultado = cur.fetchall()
            for tupla in resultado:
                print(tupla)

        except (Exception, psycopg2.DatabaseError) as error:
                print(error)

        print("")
        print("")
        input("Digite qualquer coisa para continuar\n")
        os.system('cls' if os.name == 'nt' else 'clear')


    if(cons == 'b'):
        asin = input("Insira o ASIN do produto: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:
            consulta = f"SELECT * FROM (SELECT * FROM product WHERE asin in (SELECT asin_similar FROM similarprod WHERE asin_product = '{asin}')) "
            consulta += f"AS prods WHERE salesrank > (SELECT salesrank FROM product WHERE asin = '{asin}')"

            cur.execute(consulta)
            colnames = [desc[0] for desc in cur.description]
            print(colnames)

            resultado = cur.fetchall()
            for tupla in resultado:
                print(tupla)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        print("")
        print("")
        input("Digite qualquer coisa para continuar\n")
        os.system('cls' if os.name == 'nt' else 'clear')


    if(cons == 'c'):
        asin = input("Insira o ASIN do produto: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:

            consulta = f"SELECT review_date, AVG(rating) FROM (SELECT * FROM review WHERE review.asin_product = '{asin}') as aux GROUP BY review_date ORDER BY review_date ASC"
            cur.execute(consulta)

            colnames = [desc[0] for desc in cur.description]
            print(colnames)

            resultado = cur.fetchall()
            for tupla in resultado:
                print(tupla)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        print("")
        print("")
        input("Digite qualquer coisa para continuar\n")
        os.system('cls' if os.name == 'nt' else 'clear')


    if(cons == 'd'):
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:

            consulta = "(SELECT * from product where product_group='Video Games' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='Toy' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='Sports' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='DVD' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='Baby Product' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='Video' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='Music' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='Book' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='Software' order by salesrank DESC LIMIT 10)"
            consulta += "UNION (SELECT * from product where product_group='CE' order by salesrank LIMIT 10) order by product_group, salesrank DESC"

            cur.execute(consulta)

            colnames = [desc[0] for desc in cur.description]
            print(colnames)

            resultado = cur.fetchall()
            for tupla in resultado:
                print(tupla)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        print("")
        print("")
        input("Digite qualquer coisa para continuar\n")
        os.system('cls' if os.name == 'nt' else 'clear')


    if(cons == 'e'):
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:

            consulta = "SELECT product_id, asin, title, product_group,salesrank"
            consulta +=" from product JOIN (select avg(helpful),asin_product from"
            consulta +=" review GROUP BY asin_product ORDER BY avg(helpful) DESC "
            consulta +="LIMIT 10) as top10 ON product.asin = top10.asin_product;"
               
            cur.execute(consulta)

            colnames = [desc[0] for desc in cur.description]
            print(colnames)

            resultado = cur.fetchall()
            for tupla in resultado:
                print(tupla)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        print("")
        print("")
        input("Digite qualquer coisa para continuar\n")
        os.system('cls' if os.name == 'nt' else 'clear')


    if(cons == 'f'):
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:
                
            consulta = "SELECT category.cat_id, category.name, category.parent_id"
            consulta+=" FROM category JOIN (SELECT catprod.cat_id,"
            consulta+=" avg(avghelpful.avg) from catprod JOIN"
            consulta+=" (select avg(helpful),asin_product from review"
            consulta+=" GROUP BY asin_product ORDER BY avg(helpful) DESC)"
            consulta+=" as avghelpful ON catprod.asin_prod = "
            consulta+="avghelpful.asin_product GROUP BY cat_id ORDER BY"
            consulta+=" avg(avghelpful.avg) DESC LIMIT 5) AS top5cat"
            consulta+=" ON category.cat_id = top5cat.cat_id;"
            cur.execute(consulta)

            resultado = cur.fetchall()

            colnames = [desc[0] for desc in cur.description]
            print(colnames)

            for tupla in resultado:
                print(tupla)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        print("")
        print("")
        input("Digite qualquer coisa para continuar\n")
        os.system('cls' if os.name == 'nt' else 'clear')

    if(cons == 'g'):
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:

            consulta = """
            SELECT DISTINCT ON (p.product_group) p.product_group, r.customer_id, COUNT(*) as num_reviews
            FROM review r
            INNER JOIN product p ON r.asin_product = p.asin
            GROUP BY p.product_group, r.customer_id
            ORDER BY p.product_group, num_reviews DESC
            LIMIT 10;
            """
            cur.execute(consulta)

            colnames = [desc[0] for desc in cur.description]
            print(colnames)

            resultado = cur.fetchall()
            for tupla in resultado:
                print(tupla)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        print("")
        print("")
        input("Digite qualquer coisa para continuar\n")
        os.system('cls' if os.name == 'nt' else 'clear')

    if(cons == 'h'):
        break

    else:
        print("Entrada inválida. Tente outra entrada:")
        continue