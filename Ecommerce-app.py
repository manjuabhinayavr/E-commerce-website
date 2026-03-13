from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "Mora Spices and Blends"

# ========== PRODUCTS ==========
products = [
    {"id": 1, "name": "Turmeric Powder",    "price": 99,  "category": "Spices",       "emoji": "🟡"},
    {"id": 2, "name": "Red Chilli Powder",  "price": 89,  "category": "Spices",       "emoji": "🔴"},
    {"id": 3, "name": "Coriander Powder",   "price": 79,  "category": "Spices",       "emoji": "🟤"},
    {"id": 4, "name": "kids health mix",    "price": 149, "category": "Health Mix",   "emoji": "🌾"},
    {"id": 5, "name": "karupu kavani Mix",  "price": 129, "category": "Millet Mix",   "emoji": "🌿"},
    {"id": 6, "name": "mapillai samba laddu","price": 139, "category": "Millet Mix",   "emoji": "🌱"},
    {"id": 7, "name": "Moringa Powder",     "price": 199, "category": "Health Mix",   "emoji": "💚"},
    {"id": 8, "name": "garam masala",       "price": 249, "category": "Spice mix",   "emoji": "🌿"},
    {"id": 9, "name": "sambar powder",      "price": 299, "category": "Spice mix",   "emoji": "⭐"},
]

# ========== USERS ==========
users = {"admin": "admin123"}

# ========== HOME ==========
@app.route("/")
def home():
    category = request.args.get("category", "All")
    if category == "All":
        filtered = products
    else:
        filtered = [p for p in products if p["category"] == category]
    return render_template("index.html", products=filtered, category=category)

# ========== LOGIN ==========
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/")
        return render_template("login.html", error="Invalid credentials!")
    return render_template("login.html")

# ========== REGISTER ==========
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users:
            return render_template("register.html", error="User already exists!")
        users[username] = password
        return redirect("/login")
    return render_template("register.html")

# ========== LOGOUT ==========
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

# ========== CART ==========
@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] * item["qty"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    cart = session.get("cart", [])
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        for item in cart:
            if item["id"] == product_id:
                item["qty"] += 1
                session["cart"] = cart
                return redirect("/")
        cart.append({"id": product["id"], "name": product["name"],
                     "price": product["price"], "qty": 1})
        session["cart"] = cart
    return redirect("/")

@app.route("/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != product_id]
    session["cart"] = cart
    return redirect("/cart")

# ========== ADMIN ==========
@app.route("/admin")
def admin():
    if session.get("user") != "admin":
        return redirect("/login")
    return render_template("admin.html", products=products)

@app.route("/admin/add", methods=["POST"])
def add_product():
    if session.get("user") != "admin":
        return redirect("/login")
    new_product = {
        "id": len(products) + 1,
        "name": request.form["name"],
        "price": int(request.form["price"]),
        "category": request.form["category"],
        "emoji": request.form["emoji"]
    }
    products.append(new_product)
    return redirect("/admin")

# ========== RUN ==========
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)