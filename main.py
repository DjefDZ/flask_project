from flask import *
import sqlite3

app = Flask(__name__)


@app.route("/")
def root():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, name, price, description, image FROM items')
        itemData = cur.fetchall()
    itemData = parse(itemData)   
    return render_template('index.html', itemData=itemData)




@app.route("/removeItem")
def removeItem():
    itemId = request.args.get('itemId')
    with sqlite3.connect('database.db') as conn:
        try:
            cur = conn.cursor()
            cur.execute('DELETE FROM items WHERE itemID = ?', (itemId, ))
            conn.commit()
            msg = "Deleted successsfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()
    print(msg)
    return redirect(url_for('root'))



@app.route("/itemDescription")
def itemDescription():
    itemId = request.args.get('itemId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, name, price, description, image FROM items WHERE id = ?', (itemId, ))
        itemData = cur.fetchone()
    conn.close()
    return render_template("itemDescription.html", data=itemData)

@app.route("/addToCart")
def addToCart():
    itemId = int(request.args.get('itemId'))
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    try:
        cur.execute(f"INSERT INTO cart(itemId) VALUES({itemId})")
        conn.commit()
        msg = "Added successfully"
    except:
        conn.rollback()
        msg = "Error occured"
    conn.close()
    return redirect(url_for(f'root'))

@app.route("/cart")
def cart():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    items = cur.execute("SELECT items.id, items.name, items.price, items.description, items.image FROM items, cart WHERE items.id = cart.itemId").fetchall()
    totalPrice = 0
    for row in items:
        totalPrice += row[2]
    return render_template("cart.html", items=items, totalPrice=totalPrice)

@app.route("/removeFromCart")
def removeFromCart():
    itemId = int(request.args.get('itemId'))
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM cart WHERE itemId = {itemId}")
        conn.commit()
        msg = "removed successfully"
    except:
        conn.rollback()
        msg = "error occured"
    conn.close()
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
