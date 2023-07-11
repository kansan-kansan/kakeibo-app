import datetime
from pathlib import Path
import pandas as pd
import re
import sqlite3
import openpyxl

now = datetime.datetime.now()
this_year = now.strftime('%Y')
this_month = now.strftime('%m')
this_day = now.strftime('%d')

class Core:
    def Register(self,path_to_file,enter_month): #登録処理
        print("登録は自動で登録させますか？")
        
        while True:
            date = str(input("日付は今日ですか? y or n>>"))
            if date == "y":
                enter_day = this_day
                break
            elif date == "n":       #正規表現
                enter_day = int(input("日付を入力>>"))
                break
            else:
                print("もう一度入力してください")

        print("\n1:食費\n2:コンビニ\n3:日用品\n4:通信費\n5:交際費\n6:医療費\n7:雑費")
        classification_goods = str(input("内訳は何ですか？>>"))
        goods = {"1":"食費","2":"コンビニ","3":"日用品","4":"通信費","5":"交際費","6":"医療費","7":"雑費"}
        value_goods = goods[classification_goods]

        money = int(input("\n金額はいくらですか?>>"))

        print("\n1:クレジットカード\n2:現金\n3:paypay\n4:ナナコ\n5交通系IC\n6:チャージ\n7その他")#\n7:雑費")
        method_of_payment = str(input(">>"))
        payment = {"1":"クレジットカード","2":"現金","3":"paypay","4":"ナナコ","5":"交通系IC","6":"チャージ","7":"その他"}
        value_payment = payment[method_of_payment]
        
        print(f"{enter_day}日,{value_goods},{money}円,{value_payment}")     #確認(内訳、金額、支払い方法)
        choice_write = str(input("この記入内容でこれでよろしいですか？ y or n>>"))
        if choice_write == "y":
            conn = sqlite3.connect(path_to_file)
            cur = conn.cursor()
            cur.execute(f'INSERT INTO main(日付,内訳_id,円,支払い方法_id) values("{this_month}/{enter_day}","{classification_goods}","{money}","{method_of_payment}")')
            #print("DB入力完了")

            #df = pd.read_sql('SELECT * FROM main', conn)            
            #print(df)    
            conn.commit()
            conn.close()
            #print("DB　コミット完了")
                            

    def List_all(self,path_to_file):
        conn = sqlite3.connect(path_to_file)
        cur = conn.cursor()
        df = pd.read_sql('SELECT 日付,内訳,円,支払い方法 FROM main,支払い方法,内訳 WHERE main.内訳_id=内訳.内訳_id AND main.支払い方法_id=支払い方法.支払い方法_id', conn)
        print(df)    
        conn.commit()
        conn.close()
        #print("List(表示)にきたよ")


    def Delete(self):
        print("Deleteにきたよ")

    
    def Sort(self,path_to_file):
        conn = sqlite3.connect(path_to_file)
        cur = conn.cursor()
        df = pd.read_sql('SELECT 日付,内訳,円,支払い方法 FROM main,支払い方法,内訳 WHERE main.内訳_id=内訳.内訳_id AND main.支払い方法_id=支払い方法.支払い方法_id', conn)
        print(df)    
        conn.commit()
        conn.close()
        print("日付を昇順に並び替えます。")


    def Output(self,path_to_file,enter_year,enter_month):
        print("同じファイルで")
        print("出力のファイル形式(excel,csv,txt)はどれですか？")
        choice_format = str(input("e(excel) or c(csv) or t(txt)>>"))
        if choice_format == "e":
            print("excelで出力します")
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet['A1'].value = '日付'
            sheet['B1'].value = '内訳'
            sheet['C1'].value = '金額'
            sheet['D1'].value = '支払い方法'
            conn = sqlite3.connect(path_to_file)
            cur = conn.cursor()
            cur.execute('SELECT 日付,内訳,円,支払い方法 FROM main,支払い方法,内訳 WHERE main.内訳_id=内訳.内訳_id AND main.支払い方法_id=支払い方法.支払い方法_id')
            for i, row in enumerate (cur):
                sheet['A' + str(i+2)].value = row[0] #年月日
                sheet['B' + str(i+2)].value = row[1] #平均気温
                sheet['C' + str(i+2)].value = row[2] #最高気温
                sheet['D' + str(i+2)].value = row[3] #最低気温 
            conn.commit()
            conn.close()
            print(f"出力名は{enter_year}_{enter_month}.xlsxです。")
            workbook.save(f"{enter_year}_{enter_month}.xlsx")
            print("出力しました。")            

        if choice_format == "c":
            print("csvで出力します")

        if choice_format == "t":
            print("txtで出力します")
        print("出力(ExPort)にきたよ")

    def main(self):
        #print(self)
        flag = False
        choice_month = str(input(f"{this_year}年{this_month}月の家計簿でよろしいですか？ y or n>>"))
        if choice_month == "y":
            enter_year,enter_month = this_year,this_month
            #print(year,month)
        elif choice_month == "n":
            enter_year = int(input("何年かを(西暦で)入力してください>>"))
            enter_month = int(input("何月かを入力してください>>"))
            print(f"{enter_year}年{enter_month}月で登録します。")
        

        path_to_file = f'{enter_year}_{enter_month}.db'
        path = Path(path_to_file)
        if path.is_file():
            print('過去のファイルがあるため、それを流用します。')
        else:
            choice_file_create = str(input('過去のファイルがないため、新規作成してもよろしいでしょうか？ y or n>>'))
            if choice_file_create == "y":
                print("新規ファイルを作成します。")
                conn = sqlite3.connect(path_to_file)
                cur = conn.cursor()                
                print(f"ファイル名は{path_to_file}です。")
                cur.execute('CREATE TABLE main(日付 DATE,内訳_id INTEGER,円 INTEGER,支払い方法_id INTEGER)')
                cur.execute('Create table 内訳(内訳_id INTEGER PRIMARY KEY,内訳 VARCHAR)')
                cur.execute('Create table 支払い方法(支払い方法_id INTEGER PRIMARY KEY,支払い方法 VARCHAR)')
                #print("Table 全て作成完了。")
                cur.execute('INSERT INTO 支払い方法(支払い方法_id,支払い方法) values("1","クレジットカード")')
                cur.execute('INSERT INTO 支払い方法(支払い方法_id,支払い方法) values("2","現金")')
                cur.execute('INSERT INTO 支払い方法(支払い方法_id,支払い方法) values("3","paypay")')
                cur.execute('INSERT INTO 支払い方法(支払い方法_id,支払い方法) values("4","ナナコ")')
                cur.execute('INSERT INTO 支払い方法(支払い方法_id,支払い方法) values("5","交通系IC")')
                cur.execute('INSERT INTO 支払い方法(支払い方法_id,支払い方法) values("6","チャージ")')
                cur.execute('INSERT INTO 支払い方法(支払い方法_id,支払い方法) values("7","その他")')
                #print("初期設定、支払い方法終了")
                cur.execute('INSERT INTO 内訳(内訳_id,内訳) values("1","食費")')
                cur.execute('INSERT INTO 内訳(内訳_id,内訳) values("2","コンビニ")')
                cur.execute('INSERT INTO 内訳(内訳_id,内訳) values("3","日用品")')
                cur.execute('INSERT INTO 内訳(内訳_id,内訳) values("4","通信費")')
                cur.execute('INSERT INTO 内訳(内訳_id,内訳) values("5","交際費")')
                cur.execute('INSERT INTO 内訳(内訳_id,内訳) values("6","医療費")')
                cur.execute('INSERT INTO 内訳(内訳_id,内訳) values("7","趣味")')
                cur.execute('INSERT INTO 内訳(内訳_id,内訳) values("8","雑費")')
                conn.commit()
                conn.close()
                #print("DB初期設定終了")


        while True:
            print("\n1:登録\n2:表示\n3:削除\n4:保存\n5:日付順に並び替え\n6:出力\n9:終了")
            choice = int(input("番号を選んでください>>"))
            print()#改行

            if choice == 1:
                self.Register(path_to_file,enter_month)
                flag = False

            elif choice == 2:
                self.List_all(path_to_file)

            elif choice == 3:
                self.Delete(path_to_file)
                print()
                
            elif choice == 4:
                flag = True
                print("保存しました")

            elif choice == 5:
                if flag == True:
                    print("日付順に並び替えます。")
                    self.Sort(path_to_file)

                else:
                    print("保存していないため、並び替えできません。")
                    print("保存してから並び替えしてください。")

            elif choice == 6:
                if flag == True:
                    print("出力します。")
                    self.Output(path_to_file,enter_year,enter_month)

                else:
                    print("保存していないため、並び替えできません。")
                    print("保存してから並び替えしてください。")

            elif choice == 9:
                if flag == False :
                    print("終了します。")
                break
            else:
                print("もう一度お願いいたします。")

if __name__ == '__main__':
    a = Core()
    a.main()
