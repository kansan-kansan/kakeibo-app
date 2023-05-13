from tkinter import *
from tkinter import ttk
root = Tk()


def btn_click():

    print(goods.get())
    print(payment.get())

    print(money.get())
    print(type(money.get()))


#GUIのタイトル
root.title("家計簿アプリ")

#GUIの大きさ
root.geometry("640x470")

label_Options_classification_goods = ttk.Label(root,text="内訳を選んでください")
label_Options_classification_goods.place(x=10,y=30 )
label_Options_classification_goods.pack()

Options_classification_goods = ["食費","コンビニ","日用品","通信費","交際費", "医療費","雑費"]
goods = ttk.Combobox(root, values=Options_classification_goods, width=10, state='readonly')
goods.current(0)
goods.place(x=150, y=50)



label_Options_payment = ttk.Label(root,text="支払い方法を選んでください")
label_Options_payment.place(x=150,y=200)
label_Options_payment.pack()

Options_payment = ["クレジットカード","現金","paypay","ナナコ","チャージ", "その他"]
payment = ttk.Combobox(root, values=Options_payment, width=20, state='readonly')
payment.current(0)
payment.place(x=150, y=150)



label_money = ttk.Label(root,text="金額を入力してください")
label_money.place(x=150,y=200)
label_money.pack()

money = ttk.Entry(master=root, width=30, font=20)
money.place(x=200,y=400)


btn = ttk.Button(root, text='ボタン', command=btn_click)
btn.place(x=50, y=100)

#ウィンドウの表示
root.mainloop()
