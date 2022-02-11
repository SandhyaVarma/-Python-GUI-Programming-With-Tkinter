from tkinter import *
import requests
import json

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap("favicon.ico")

def font_color(amount):
    if amount >= 0:
        return"green"
    else:
        return "red"



def my_Portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=9dc3e74a-37c4-42ae-8d64-35fcea5fa29a")
 
    api= json.loads(api_request.content)

    coins =[    
    {
     "symbol":"BTC",
     "amount_owned":2,
     "price_per_coin":3200
    },
    
     {
     "symbol":"ADA",
     "amount_owned":100,
     "price_per_coin":2.05
     },
     
     {
     "symbol":"EOS",
     "amount_owned":50,
     "price_per_coin":3.10 
     },

     {
     "symbol":"LTC",
     "amount_owned":75,
     "price_per_coin":25  
     },

     {
      "symbol":"XMR",
     "amount_owned":10,
     "price_per_coin":250 
     }] 

    total_pl = 0
    coin_row = 1
    total_current_value = 0

    for i in range(0,300):
        for coin in coins:
            if api["data"][i]["symbol"] == coin["symbol"]:
                total_paid = coin["amount_owned"]*coin["price_per_coin"]
                current_value = coin["amount_owned"]* api["data"][i]["quote"]["USD"]["price"]
                pl_percoin = api["data"][i]["quote"]["USD"]["price"] - coin["price_per_coin"]
                total_pl_percoin = pl_percoin * coin["amount_owned"]

                total_pl = total_pl + total_pl_percoin
                total_current_value = total_current_value + current_value


                # print(api["data"][i]["name"]+ " - " + api["data"][i]["symbol"])
                # print("price- ${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]))
                # print("Number of coins:",coin["amount_owned"])
                # print("Total amount Paid:"," ${0:.2f}".format(total_paid))
                # print("Current Value:"," ${0:.2f}".format(current_value))
                # print("P/L Per Coin:"," ${0:.2f}".format(pl_percoin))
                # print("Total P/L with Coin:"," ${0:.2f}".format(total_pl_percoin))

                # print("--------------------")

                name = Label(pycrypto , text=api["data"][i]["symbol"], bg="#F3F4F6" , fg="black" , font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                name.grid(row=  coin_row, column=0, sticky=N+S+E+W)

                price = Label(pycrypto , text= "${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                price.grid(row= coin_row , column=1, sticky=N+S+E+W)

                no_coins = Label(pycrypto , text=coin["amount_owned"] , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                no_coins.grid(row= coin_row , column=2, sticky=N+S+E+W)

                amount_paid = Label(pycrypto , text=" ${0:.2f}".format(total_paid) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                amount_paid.grid(row= coin_row , column=3, sticky=N+S+E+W)

                current_value = Label(pycrypto , text=" ${0:.2f}".format(current_value) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                current_value.grid(row= coin_row , column=4, sticky=N+S+E+W)

                pl_coin = Label(pycrypto , text=" ${0:.2f}".format(pl_percoin) , bg="#F3F4F6" , fg=font_color(float("{0:.2f}".format(pl_percoin))), font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                pl_coin.grid(row= coin_row, column=5, sticky=N+S+E+W)

                totalpl = Label(pycrypto , text=" ${0:.2f}".format(total_pl_percoin) , bg="#F3F4F6" , fg=font_color(float("{0:.2f}".format(total_pl_percoin))), font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
                totalpl.grid(row= coin_row , column=6, sticky=N+S+E+W)

                coin_row = coin_row + 1


    totalcv = Label(pycrypto , text=" ${0:.2f}".format(total_current_value) , bg="#F3F4F6" , fg="black", font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    totalcv.grid(row= coin_row , column=4, sticky=N+S+E+W)
    
    totalpl = Label(pycrypto , text=" ${0:.2f}".format(total_pl) , bg="#F3F4F6" , fg=font_color(float("{0:.2f}".format(total_pl))), font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    totalpl.grid(row= coin_row , column=6, sticky=N+S+E+W)
    # print("Total P/L for portfolio:"," ${0:.2f}".format(total_pl))

    api = ""

    update = Button(pycrypto , text="Update", bg="#142E54" , fg="white", command=my_Portfolio , font="lato 12", padx="2" , pady="2" , borderwidth=2 , relief="groove" )
    update.grid(row= coin_row , column=6, sticky=N+S+E+W)
    



name = Label(pycrypto , text="Coin name" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
name.grid(row=0 , column=0, sticky=N+S+E+W)

price = Label(pycrypto , text="Price" , bg="#142E54" , fg="white" , font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
price.grid(row=0 , column=1, sticky=N+S+E+W)

no_coins = Label(pycrypto , text="Coins Owned" , bg="#142E54" , fg="white" , font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
no_coins.grid(row=0 , column=2, sticky=N+S+E+W)

amount_paid = Label(pycrypto , text="Total amount paid" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
amount_paid.grid(row=0 , column=3, sticky=N+S+E+W)

current_value = Label(pycrypto , text="Current value" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
current_value.grid(row=0 , column=4, sticky=N+S+E+W)

pl_coin = Label(pycrypto , text="P/L per coin" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
pl_coin.grid(row=0 , column=5, sticky=N+S+E+W)

totalpl = Label(pycrypto , text="Total P/L with coin" , bg="#142E54" , fg="white", font= " lato 12 bold" , padx="5" , pady="5" , borderwidth=2 , relief="groove")
totalpl.grid(row=0 , column=6, sticky=N+S+E+W)

my_Portfolio()

pycrypto.mainloop()
print("program completed")

