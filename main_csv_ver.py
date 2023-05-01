import datetime
from pathlib import Path
import pandas as pd

now = datetime.datetime.now()
this_year = now.year
this_month = now.month
this_day = now.day

class Core:
    def Register(self,path_to_file,enter_month): #登録処理
        while True:
            date = str(input("日付は今日ですか? y or n>>"))
            if date == "y":
                enter_day = now.day
                break
            elif date == "n":
                enter_day = int(input("日付を入力>>"))
                break
            else:
                print("もう一度入力してください")

        print("\n1:食費\n2:コンビニ\n3:日用品\n4:通信費\n5:交際費\n6:医療費\n7:雑費")
        classification_goods = str(input("内訳は何ですか？>>"))
        goods = {"1":"食費","2":"コンビニ","3":"日用品","4":"通信費","5":"交際費","6":"医療費","7":"雑費"}
        value_goods = goods[classification_goods]

        money = int(input("\n金額はいくらですか?>>"))

        print("\n1:クレジットカード\n2:現金\n3:paypay\n4:ナナコ\n5:チャージ\n6その他")#\n7:雑費")
        method_of_payment = str(input(">>"))
        payment = {"1":"クレジットカード","2":"現金","3":"paypay","4":"ナナコ","5":"チャージ","6":"その他"}
        value_payment = payment[method_of_payment]
        
        print(f"{enter_day}日,{value_goods},{money}円,{value_payment}")     #確認(内訳、金額、支払い方法)
        choice_write = str(input("この記入内容でこれでよろしいですか？ y or n>>"))
        if choice_write == "y":
            df = pd.DateFrame([f"{enter_month}","{value_goods}","",""])

            with open (path_to_file,mode="a",encoding="utf-8") as file:
                enter_day = str(enter_day)
                enter_month = str(enter_month)
                file.write(f"\n{enter_month}/{enter_day},{value_goods},{money},{value_payment},{this_month}/{this_day}")
                file.write("")
                
        
    def List_all(self,path_to_file):
        with open (path_to_file,mode="r",encoding="utf-8") as file:
            for line in file:
                print(line)

    def Delete(self):
        print("Deleteにきたよ")
    
    def Sort(self,path_to_file):
        print("日付を昇順に並び替えます。")
        data = pd.read_csv(path_to_file)
        data =  pd.to_datetime(data['日付'], infer_datetime_format= True)
        data.sort_values(by = '日付', ascending = True, inplace = True) 
        print(data)

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
        

        path_to_file = f'{enter_year}.{enter_month}.csv'
        path = Path(path_to_file)
        if path.is_file():
            print('過去のファイルがあるため、それを流用します。')
        else:
            choice_file_create = str(input('過去のファイルがないため、新規作成してもよろしいでしょうか？ y or n>>'))
            if choice_file_create == "y":
                print("新規ファイルを作成します。")
                print(f"ファイル名は{path_to_file}です。")
                with open (path_to_file,"w",encoding="utf-8") as file:
                    file.write("日付,内訳,金額,支払い方法,記入日")


        while True:
            print("\n1:登録\n2:表示\n3:削除\n4:保存\n5:日付順に並び替え\n9:終了")
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

            elif choice == 9:
                if flag == False :
                    print("終了します。")
                break
            else:
                print("もう一度お願いいたします。")

if __name__ == '__main__':
    a = Core()
    a.main()
