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

def welcome_func():
    print("DASHBOARD DE CONSULTAS")
    print("")
    print("")
    print("Escolha a consulta a ser feita:")
    print("")
    print("1 - Dado um produto, listar os 5 comentarios mais uteis e com maior avaliacao e os 5 comentarios mais uteis e com menor avaliacao.")
    print("2 - Dado um produto, listar os produtos similares com maiores vendas do que ele.")
    print("3 - Dado um produto, mostrar a evolução diária das médias de avaliação ao longo do intervalo de tempo coberto no arquivo de entrada.")
    print("4 - Listar os 10 produtos líderes de venda em cada grupo de produtos.")
    print("5 - Listar os 10 produtos com a maior média de avaliações úteis positivas por produto.")
    print("6 - Listar a 5 categorias de produto com a maior média de avaliações úteis positivas por produto.")
    print("7 - Listar os 10 clientes que mais fizeram comentários por grupo de produto.")
    print("")
    print("8 - Finalizar")
    print("")
    print("")

while (True):
    os.system('cls' if os.name == 'nt' else 'clear')

    welcome_func()

    cons = input("Escolha uma consulta: ")
    os.system('cls' if os.name == 'nt' else 'clear')

    # FIXAR URGENTE(NÃO FUNCIONANDO)
    if (cons == '1'):
        asin = input("Insira o ASIN do produto: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")
        try:

            consulta = f"(SELECT * FROM (SELECT * FROM review WHERE asin_prod = '{asin}') AS aux ORDER BY helpful DESC, votes DESC LIMIT 5) UNION "
            consulta += f"(SELECT * FROM (SELECT * FROM Reviews WHERE asin_prod = '{asin}') AS aux2 ORDER BY "
            consulta += "helpful DESC, votes LIMIT 5);"
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

    # FIXAR URGENTE (PARCIAL)
    if(cons == '2'):
        asin = input("Insira o ASIN do produto: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:
            consulta = f"SELECT * FROM (SELECT * FROM product WHERE asin in (SELECT asin_similar FROM similarprod WHERE asin_prod = '{asin}')) "
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

    #Fixar urgente (Parcial)
    if(cons == '3'):
        asin = input("Insira o ASIN do produto: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:

            consulta = f"SELECT review_date, AVG(rating) as avg FROM (SELECT * FROM review WHERE review.asin_prod = '{asin}') as aux GROUP BY review.review_date ORDER BY review ASC"
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


    if(cons == '4'):
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
            consulta += "UNION (SELECT * from product where product_group='CE' order by salesrank LIMIT 10) order by product_group, rank DESC"

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


    if(cons == '5'):
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

    if(cons == '6'):
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

    # Fixar (socorro) (deus me ajude)
    if(cons == '10'):
        print("")
        print("")
        print("RESULTADO DA CONSULTA:")
        print("")
        print("")

        try:

            consulta = "((SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='Book') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='Video Games') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='Sports') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='DVD') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='Baby Product') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='Video') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='Music') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='Software') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='CE') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10) "
            consulta += "UNION (SELECT r.id_cliente,p.grupo,count(r.id_cliente) "
            consulta += "AS qtd_reviews FROM reviews as r JOIN produtos as p ON r.asin_prod = p.asin where asin_prod IN "
            consulta += "(SELECT asin FROM produtos where grupo='Toy') GROUP BY r.id_cliente, p.grupo ORDER BY qtd_reviews DESC LIMIT 10)) ORDER BY grupo, qtd_reviews DESC"
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

    if(cons == '8'):
        break

    else:
        print("Entrada inválida. Tente outra entrada:")
        continue