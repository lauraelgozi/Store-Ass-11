from bottle import route, run, template, static_file, get, post, delete, request, TEMPLATE_PATH
from sys import argv
import json
import pymysql

TEMPLATE_PATH.insert(0, '')
connection = pymysql.connect(
    host="localhost",
    user="root",
    passwd="Laura1308",
    db="assignment",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@post("/category")
def create_cat():
    name = request.POST.get("name")
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM Category"
            cursor.execute(query)
            results = cursor.fetchall()
            names = [r['name'] for r in results]
            if name == "":
                response = {
                    "STATUS": "ERROR",
                    "MSG": "Bad request",
                    "CODE": 400,
                    "CAT_ID": cursor.lastrowid
                }
                return json.dumps(response)
            elif name not in names:
                sql = "INSERT INTO Category (name) VALUES('{}')".format(name)
                cursor.execute(sql)
                connection.commit()
                response = {
                    "STATUS": "SUCCES",
                    "MSG": "",
                    "CODE": 201,
                    "CAT_ID": cursor.lastrowid
                }
                return json.dumps(response)

            elif name in names:
                response = {
                    "STATUS": "ERROR",
                    "MSG": "already exist",
                    "CODE": 200
                }

                return json.dumps(response)
    except:
        response = {
            "STATUS": "ERROR",
            "MSG": "Internal error",
            "CODE": 500}
    return json.dumps(response)


# delete categories
@route("/category/<id>", method='DELETE')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM category"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                with connection.cursor() as cursor:
                    sql = ('DELETE FROM category WHERE id = {}'.format(id))
                    cursor.execute(sql)
                    connection.commit()
                    return json.dumps({'STATUS': 'SUCCESS', 'MSG': 'The category was deleted successfully'})
            else:
                return json.dumps({'STATUS': 'ERROR', 'MSG': "category not found", 'CODE': 404})

    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "Internal error", "CODE":500})


@get("/categories")
def all_cat():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM category"
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                response = {
                    "STATUS": "SUCCES",
                    "CATEGORIES": result,
                    "CODE": 200
                }
                return json.dumps(response)
            else:
                return json.dumps({'STATUS': 'ERROR', 'MSG': "category not found", 'CODE': 404})
    except:
        response = {
            "STATUS": "ERROR",
            "MSG": "internal error",
            "CODE": 500
        }
        return json.dumps(response)


@post("/product")
def add_product():
    try:
        category = request.POST.get('category')
        title = request.POST.get('title')
        description = request.POST.get('desc')
        price = request.POST.get('price')
        favorite = request.POST.get('favorite')
        id = request.forms.get("id")
        if favorite == None:
            favorite = 0
        else:
            favorite = 1
        img_url = request.POST.get('img_url')
        with connection.cursor() as cursor:
            sql = "SELECT id FROM category WHERE id ={}".format(category)
            cursor.execute(sql)
            categories = cursor.fetchall()
            if description == "" or price == "" or img_url == "":
                return json.dumps({'STATUS': 'ERROR', 'MSG': "missing parameters", "CODE": 400})

            if not categories:
                return json.dumps({'STATUS': 'ERROR', 'MSG': "Category not found", 'CODE': 404})

            if id:
                with connection.cursor() as cursor:
                    sql = "SELECT id FROM product WHERE id = {}".format(id)
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if result:
                        with connection.cursor() as cursor:
                            sql = "UPDATE product SET title= '{0}', description ='{1}', price={2}, img_url='{3}', favorite='{4}'" \
                                  "WHERE id={5}".format(title, description, price, img_url, favorite, id)
                            cursor.execute(sql)
                            connection.commit()
                        return json.dumps({'STATUS': 'SUCCESS', 'PRODUCT_ID':id,'CODE': 201})
                    else:
                        with connection.cursor() as cursor:
                            sql2 = "INSERT INTO product (description, price,title, img_url, favorite, id) VALUES ('{0}',{1},'{2}'," \
                                   "'{3}','{4}',{5})".format(description, price, title, img_url, favorite, category)
                            cursor.execute(sql2)
                            connection.commit()
                        return json.dumps({"STATUS": "SUCCES", "CODE": 201})
            else:
                with connection.cursor() as cursor:
                    sql2 = "INSERT INTO product (description, price,title, img_url, favorite, id) VALUES ('{0}',{1},'{2}'," \
                           "'{3}','{4}',{5})".format(description, price, title, img_url, favorite, category)
                    cursor.execute(sql2)
                    connection.commit()
                return json.dumps({"STATUS": "SUCCES", "CODE": 201})

    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


@get("/product/<id>")
def load_products(id):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM product WHERE id={}'.format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            response = {
                "STATUS": "SUCCES",
                "PRODUCT": result,
                "CODE": 200
            }
            return json.dumps(response)
    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "Internal error", 'CODE': 500})


@route('/product/<id>', method='DELETE')
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id from product where id ={}".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
        if result:
            with connection.cursor() as cursor:
                sql = ('DELETE FROM product WHERE id = {}'.format(id))
                cursor.execute(sql)
                connection.commit()
                return json.dumps({'STATUS': 'SUCCES', 'MSG': '', 'CODE': 201})
        else:
            return json.dumps({'STATUS': 'ERROR', 'MSG': "product not found", 'CODE': 404})
    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "Internal error", 'CODE': 500})


@get("/products")
def load_products():
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT * FROM product')
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                return json.dumps({'STATUS': 'SUCCESS', 'PRODUCTS': result, 'CODE': 201})
            else:
                return json.dumps({'STATUS': 'ERROR', 'MSG': "product not found", 'CODE': 404})

    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "Internal error", 'CODE': 500})


@get('/category/<id>/products')
def list_products_cat(id):
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM product  WHERE  id= {}'.format(int(id))
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                return json.dumps({'STATUS': 'SUCCESS', 'PRODUCTS': result, 'CODE': 201})
            else:
                return json.dumps({'STATUS': 'ERROR', 'MSG': "product not found", 'CODE': 404})
    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "Internal error", 'CODE': 500})


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


if __name__ == "__main__":
    run(host='localhost', port=7000, debug=True)
