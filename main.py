from tkinter import *
from tkinter import messagebox , Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap("favicon.ico")

con = sqlite3.connect("coin.db")
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()

    nav_bar()
    app_header()
    my_Portfolio()
    
def nav_bar():

    def clear_all():
        cursorObj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo("Portfolio Noticifaction","Portfolio Cleared- Add new coins")
        reset()

    def close_app():
        pycrypto.destroy()


    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio' , command= clear_all)
    file_item.add_command(label='Close App' , command= close_app)
    menu.add_cascade(label='File' , menu= file_item)

    pycrypto.config(menu=menu)


def my_Portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=9dc3e74a-37c4-42ae-8d64-35fcea5fa29a")
 
    api= json.loads(api_request.content)

    cursorObj.execute("SELECT * FROM coin")
    coins = cursorObj.fetchall()

    def font_color(amount):
        if amount >= 0:
            return"green"
        else:
            return "red"
    

    def insert_coin():
        cursorObj.execute("INSERT INTO coin( symbol,price,amount) VALUES(?,?,?)",(symbol_txt.get(), price_txt.get(), amount_txt.get()))
        con.commit()
       
        reset()
        messagebox.showinfo("Portfolio Notification", "Coin Added to Portfolio successfully")

    def update_coin():
        cursorObj.execute("UPDATE coin SET symbol=?, price=? , amount=? WHERE id=?", (symbol_update.get(), price_update.get(),amount_update.get(),portid_up.get()))
        con.commit()

        reset()
        messagebox.showinfo("Portfolio Notification", "Coin Updated successfully")
 
    def delete_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),))
        con.commit()
        
        reset()
        messagebox.showinfo("Portfolio Notification", "Coin Deleted from Portfolio ")


    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0,300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                total_paid = coin[2]*coin[3]
                current_value = coin[2]* api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                total_pl_percoin = pl_percoin * coin[2]

                total_pl += total_pl_percoin
                total_current_value += current_value
                total_amount_paid += total_paid

                
                portfolio_id = Label(pycrypto , text=coin[0], bg="#F3F4F6" , fg="black" , font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                portfolio_id.grid(row=  coin_row, column=0, sticky=N+S+E+W)

                name = Label(pycrypto , text=api["data"][i]["symbol"], bg="#F3F4F6" , fg="black" , font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                name.grid(row=  coin_row, column=1, sticky=N+S+E+W)

                price = Label(pycrypto , text= "${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                price.grid(row= coin_row , column=2, sticky=N+S+E+W)

                no_coins = Label(pycrypto , text=coin[2] , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                no_coins.grid(row= coin_row , column=3, sticky=N+S+E+W)

                amount_paid = Label(pycrypto , text=" ${0:.2f}".format(total_paid) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                amount_paid.grid(row= coin_row , column=4, sticky=N+S+E+W)

                current_value = Label(pycrypto , text=" ${0:.2f}".format(current_value) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                current_value.grid(row= coin_row , column=5, sticky=N+S+E+W)

                pl_coin = Label(pycrypto , text=" ${0:.2f}".format(pl_percoin) , bg="#F3F4F6" , fg=font_color(float("{0:.2f}".format(pl_percoin))), font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                pl_coin.grid(row= coin_row, column=6, sticky=N+S+E+W)

                totalpl = Label(pycrypto , text=" ${0:.2f}".format(total_pl_percoin) , bg="#F3F4F6" , fg=font_color(float("{0:.2f}".format(total_pl_percoin))), font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                totalpl.grid(row= coin_row , column=7, sticky=N+S+E+W)

                coin_row += 1

    #insert data

    symbol_txt = Entry(pycrypto, borderwidth=2 , relief="groove")
    symbol_txt.grid(row= coin_row + 1, column=1)

    price_txt = Entry(pycrypto, borderwidth=2 , relief="groove")
    price_txt.grid(row= coin_row + 1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2 , relief="groove")
    amount_txt.grid(row= coin_row + 1, column=3)

    add_coin = Button(pycrypto , text="Add Coin", bg="#142E54" , fg="white", command=insert_coin , font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    add_coin.grid(row= coin_row +1 , column=4, sticky=N+S+E+W)

    #update coin

    portid_up = Entry(pycrypto, borderwidth=2 , relief="groove")
    portid_up.grid(row= coin_row + 2, column=0)

    symbol_update = Entry(pycrypto, borderwidth=2 , relief="groove")
    symbol_update.grid(row= coin_row + 2, column=1)

    price_update = Entry(pycrypto, borderwidth=2 , relief="groove")
    price_update.grid(row= coin_row + 2, column=2)

    amount_update = Entry(pycrypto, borderwidth=2 , relief="groove")
    amount_update.grid(row= coin_row + 2, column=3)

    update_coin_txt = Button(pycrypto , text="Update Coin", bg="#142E54" , fg="white", command=update_coin , font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    update_coin_txt.grid(row= coin_row +2 , column=4, sticky=N+S+E+W)

    #delete coin
    portid_delete = Entry(pycrypto, borderwidth=2 , relief="groove")
    portid_delete.grid(row= coin_row + 3, column=0)

    delete_coin_txt = Button(pycrypto , text="Delete Coin", bg="#142E54" , fg="white", command=delete_coin , font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    delete_coin_txt.grid(row= coin_row +3 , column=4, sticky=N+S+E+W)



    totalap = Label(pycrypto , text=" ${0:.2f}".format(total_amount_paid) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    totalap.grid(row= coin_row , column=4, sticky=N+S+E+W)

    totalcv = Label(pycrypto , text=" ${0:.2f}".format(total_current_value) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    totalcv.grid(row= coin_row , column=5, sticky=N+S+E+W)
    
    totalpl = Label(pycrypto , text=" ${0:.2f}".format(total_pl) , bg="#F3F4F6" , fg=font_color(float("{0:.2f}".format(total_pl))), font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    totalpl.grid(row= coin_row , column=7, sticky=N+S+E+W)

    api = ""

    refresh = Button(pycrypto , text="Refresh", bg="#142E54" , fg="white", command=reset , font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    refresh.grid(row= coin_row , column=7, sticky=N+S+E+W)
    


def app_header():

    portfolio_id = Label(pycrypto , text="Portfolio_Id" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
    portfolio_id.grid(row=0 , column=0, sticky=N+S+E+W)

    name = Label(pycrypto , text="Coin name" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
    name.grid(row=0 , column=1, sticky=N+S+E+W)

    price = Label(pycrypto , text="Price" , bg="#142E54" , fg="white" , font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
    price.grid(row=0 , column=2, sticky=N+S+E+W)

    no_coins = Label(pycrypto , text="Coins Owned" , bg="#142E54" , fg="white" , font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
    no_coins.grid(row=0 , column=3, sticky=N+S+E+W)

    amount_paid = Label(pycrypto , text="Total amount paid" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
    amount_paid.grid(row=0 , column=4, sticky=N+S+E+W)

    current_value = Label(pycrypto , text="Current value" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
    current_value.grid(row=0 , column=5, sticky=N+S+E+W)

    pl_coin = Label(pycrypto , text="P/L per coin" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
    pl_coin.grid(row=0 , column=6, sticky=N+S+E+W)

    totalpl = Label(pycrypto , text="Total P/L with coin" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
    totalpl.grid(row=0 , column=7, sticky=N+S+E+W)

nav_bar()
app_header()
my_Portfolio()

pycrypto.mainloop()
print("program completed")

cursorObj.close()
con.close()

