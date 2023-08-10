from flask import Flask, render_template, flash, redirect, url_for, session, request
import sqlite3

app = Flask(__name__)
app.secret_key="123456"

#Login 
@app.route('/login',methods=["GET","POST"])
def login():
    if 'email' in session:
        return redirect(url_for("home"))
    else:
        if request.method=='POST':
            email=request.form['email']
            password=request.form['password']
            con=sqlite3.connect("fbeauty.db")
            con.row_factory=sqlite3.Row
            cur=con.cursor()
            cur.execute("SELECT * FROM customer WHERE email=? AND password=?",(email,password))
            data=cur.fetchone()
            con.close()
            if data:
                session["email"]=data["email"]
                session["password"]=data["password"]
                return redirect(url_for("home"))
            else:
                flash("Username and Password Mismatch","danger")
    return render_template('login.html')

#Register 
@app.route('/register',methods=['GET','POST'])
def register():
    if 'email' in session:
        return redirect(url_for("home"))
    else:
        if request.method=='POST':
            try:
                name=request.form['name']
                surname=request.form['surname']
                email=request.form['email']
                phone=request.form['phone']
                password=request.form['password']
                con=sqlite3.connect("fbeauty.db")
                cur=con.cursor()
                cur.execute("INSERT INTO customer (name,surname,email,phone,password) VALUES (?,?,?,?,?)", (name,surname,email,phone,password))
                con.commit()
                flash("Record Added  Successfully","success")
                con.close()
            except:
                flash("Error in Insert Operation","danger")
            finally:
                return redirect(url_for("login"))
    return render_template('register.html')

#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

#Home-page 
@app.route("/")
def home():
        con = sqlite3.connect("fbeauty.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT product.product_id, product.category_id, product.title, product.brand, \
                        product.description, product.price, category.category_id, category.category_name, product.stock, product.url \
                        FROM product, category WHERE product.category_id = category.category_id and product.stock > 0")
        products = cur.fetchall()
        con.close()
        return render_template("home.html", products=products)

#All products
@app.route("/allproducts")
def allproducts():
        con = sqlite3.connect("fbeauty.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT product.product_id, product.category_id, product.title, product.brand, \
                        product.description, product.price, category.category_id, category.category_name, product.stock, product.url \
                        FROM product, category WHERE product.category_id = category.category_id and product.stock > 0")
        products = cur.fetchall()
        con.close()
        return render_template("allproducts.html", products=products)

#Eyeliner
@app.route("/eyeliner")
def eyeliner():
        con = sqlite3.connect("fbeauty.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT product.product_id, product.category_id, product.title, product.brand, \
                    product.description, product.price, category.category_id, category.category_name, product.stock, product.url \
                    FROM product, category WHERE product.category_id = category.category_id and product.category_id = 1 and product.stock > 0")
        products = cur.fetchall()
        con.close()
        return render_template("eyeliner.html", products=products)

#Lipstick
@app.route("/lipstick")
def lipstick():
        con = sqlite3.connect("fbeauty.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT product.product_id, product.category_id, product.title, product.brand, \
                        product.description, product.price, category.category_id, category.category_name, product.stock, product.url \
                        FROM product, category WHERE product.category_id = category.category_id and product.category_id = 2 and product.stock > 0")
        products = cur.fetchall()
        con.close()
        return render_template("lipstick.html", products=products)

#Mascara
@app.route("/mascara")
def mascara():
        con = sqlite3.connect("fbeauty.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT product.product_id, product.category_id, product.title, product.brand, \
                        product.description, product.price, category.category_id, category.category_name, product.stock, product.url \
                        FROM product, category WHERE product.category_id = category.category_id and product.category_id = 3 and product.stock > 0")
        products = cur.fetchall()
        con.close()
        return render_template("mascara.html", products=products)

#Concealer
@app.route("/concealer")
def concealer():
        con = sqlite3.connect("fbeauty.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(f"SELECT product.product_id, product.category_id, product.title, product.brand, \
                        product.description, product.price, category.category_id, category.category_name, product.stock, product.url \
                        FROM product, category WHERE product.category_id = category.category_id and product.category_id = 4 and product.stock > 0")
        products = cur.fetchall()
        con.close()
        return render_template("concealer.html", products=products)


#Buy Product
@app.route('/basket',methods=["GET","POST"])
def buyproduct():
    if 'email' in session:
        if request.method=='POST':
            try:
                product_id=request.form['product_id']
                address=request.form['address']
                payment_method=request.form['payment_method']
                con = sqlite3.connect("fbeauty.db")          
                cur = con.cursor()
                cur.execute("SELECT product_id FROM product WHERE product_id = '" + product_id + "' AND stock > 0")
                product = cur.fetchone()[0]
                cur.execute("SELECT customer_id FROM customer WHERE email = '" + session['email'] + "'")
                customer_id = cur.fetchone()[0]
                cur.execute("INSERT INTO cart (customer_id, product_id, payment_method, address) VALUES (?, ?, ?, ?)", (customer_id, product, payment_method, address))
                con.commit()
                flash("Added successfully")
                cur.execute("SELECT stock FROM product WHERE product_id = '" + product_id + "'")
                stock = cur.fetchone()[0]
                cur.execute(f"""UPDATE product SET stock = {int(stock)-1} WHERE product_id = {product_id}""")
                con.commit()
                con.close()
                return redirect(url_for("success"))
            except:
                flash("Wrong product ID or insufficient stock. Please try again.","danger")
                return render_template('basket.html')
        else:
            return render_template('basket.html')
    else:
       return redirect(url_for("login"))

#My Orders
@app.route('/order',methods=["GET","POST"])
def order():
    if 'email' in session:
        con = sqlite3.connect("fbeauty.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT customer_id FROM customer WHERE email = '" + session['email'] + "'")
        customer_id = cur.fetchone()[0]
        cur.execute(f"""SELECT product.product_id, cart.order_id, product.title, product.brand, \
                        product.price, product.url, cart.customer_id, cart.payment_method, cart.address \
                        FROM product, cart WHERE product.product_id = cart.product_id AND cart.customer_id = {customer_id} ORDER BY cart.order_id DESC""")
        products = cur.fetchall()
        con.close()
        return render_template("order.html", products=products)
    else:
        return redirect(url_for("login"))

#Success Page
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
