from flask import *
import sqlite3

app = Flask(__name__)


@app.route("/")
def root():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    itemData = parse(cur.execute('SELECT id, name, price, description, image FROM items').fetchall())
    return render_template('index.html', itemData=itemData)


@app.route("/removeItem")
def removeItem():
    itemId = request.args.get('itemId')
    con = sqlite3.connect('database.db')
    try:
        cur = con.cursor()
        cur.execute('DELETE FROM items WHERE itemID = ?', (itemId,))
        con.commit()
    except:
        con.rollback()
    con.close()
    return redirect(url_for('root'))


@app.route("/itemDescription")
def itemDescription():
    itemId = request.args.get('itemId')
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    itemData = cur.execute('SELECT id, name, price, description, image FROM items WHERE id = ?', (itemId,)).fetchone()
    con.close()
    return render_template("itemDescription.html", data=itemData)


@app.route("/addToCart")
def addToCart():
    itemId = int(request.args.get('itemId'))
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    try:
        cur.execute(f"INSERT INTO cart(itemId) VALUES({itemId})")
        con.commit()
    except:
        con.rollback()
    con.close()
    return redirect(url_for(f'root'))


@app.route("/cart")
def cart():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    items = cur.execute(
        "SELECT items.id, items.name, items.price, items.description, items.image FROM items, cart WHERE items.id = cart.itemId").fetchall()
    totalPrice = 0
    for row in items:
        totalPrice += row[2]
    return render_template("cart.html", items=items, totalPrice=totalPrice)


@app.route("/removeFromCart")
def removeFromCart():
    itemId = int(request.args.get('itemId'))
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    try:
        cur.execute(f"DELETE FROM cart WHERE itemId = {itemId}")
        con.commit()
    except:
        con.rollback()
    con.close()
    return redirect(url_for('cart'))


def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans


if __name__ == '__main__':
    app.run(debug=True)
