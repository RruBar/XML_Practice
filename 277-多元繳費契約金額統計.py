import requests
import urllib.request as httplib
from xml.etree import ElementTree
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False


URL="https://data.kcg.gov.tw/dataset/8543b32a-a4dd-4755-929c-3d21fbdcdf9b/resource/9eeee388-c7c6-43d3-b4f3-5b4ecd3635c4/download/xml108.107.xml"
# req = httplib.Request(URL,data=None,
#     headers={ 'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"})
# reponse = httplib.urlopen(req)               # 開啟連線動作
# if reponse.code==200:                        # 當連線正常時
#     contents=reponse.read()                  # 讀取網頁內容
#     contents=contents.decode("utf-8")        # 轉換編碼為 utf-8
#     # 把取得的XML 資料，存在檔案中
response=requests.get(URL)
response.raise_for_status()
data=response.text
# TODO 1.自己找 XML, ，把資料取得，並列印出來
# print(data)
# with open('高雄市多元繳稅方式契稅金額統計表.xml', 'w', encoding="utf-8",newline="") as fr:
#     # 進行寫入檔案時，發現都會多空一行，可以透過newline=""的引數指令，來消除多餘的空行
# TODO 2.上面2題，把取得的XML資料，存在檔案 xml 中
     # fr.write(data)

# 加載XML文件
root = ElementTree.fromstring(data)
row = root.findall("多元繳稅方式契稅金額統計表")

elements_list=[]
for ele in root.iter():
    # 透過找出每一個root.iter，可以所有xml檔中的標籤
    elements_list.append(ele.tag)
elements_list=list(set(elements_list))
# 透過set的方式排除掉重複向，在使用list轉為列表
# print(elements_list)

# TODO 3 進行matplotlib繪圖前置資料處理
year_label=[]
payment_way_list=[]
payment_way_financial_institution=[] # 金融機構臨櫃
payment_way_convenience_store=[] #便利商店繳費
payment_way_web_trans=[]    # 晶片金融卡網際網路轉帳
payment_way_ATM=[]  # ATM
payment_way_trans=[] # 活期(儲蓄)存款帳戶轉帳
payment_way_credit_card=[] # 信用卡
payment_way_trans_by_postoffice=[]  # 郵局轉帳
payment_way_trans_by_fina=[]        # 金融機構轉帳
def get_number(obj):
    number = obj.findall("金額")[0].text
    if "-" in number:
        number = 0
    elif "," in number:
        # number=number.strip(',')
        # strip只能作用在首尾，無法移除掉字串"中間"的符號
        number = number.replace(",", "")
    return number

for i in row:
    if i.findall("年度")[0].text not in year_label:
        year_label.append(i.findall("年度")[0].text)
    if i.findall("繳費方式")[0].text not in payment_way_list:
        payment_way_list.append(i.findall("繳費方式")[0].text)
    if i.findall("繳費方式")[0].text =="金融機構臨櫃繳納":
        number = get_number(i)
        payment_way_financial_institution.append(int(number))
    elif i.findall("繳費方式")[0].text =="便利商店繳納":
        number = get_number(i)
        payment_way_convenience_store.append(int(number))
    elif i.findall("繳費方式")[0].text =="晶片金融卡網際網路轉帳":
        number = get_number(i)
        payment_way_web_trans.append(int(number))
    elif i.findall("繳費方式")[0].text =="自動櫃員機(ATM)轉帳":
        number = get_number(i)
        payment_way_ATM.append(int(number))
    elif i.findall("繳費方式")[0].text =="活期(儲蓄)存款帳戶轉帳":
        number = get_number(i)
        payment_way_trans.append(int(number))
    elif i.findall("繳費方式")[0].text =="信用卡繳納":
        number = get_number(i)
        payment_way_credit_card.append(int(number))
    elif i.findall("繳費方式")[0].text =="長期約定轉帳-郵局":
        number = get_number(i)
        payment_way_trans_by_postoffice.append(int(number))
    elif i.findall("繳費方式")[0].text == "長期約定轉帳-金融機構":
        number = get_number(i)
        payment_way_trans_by_fina.append(int(number))

payment_way = [payment_way_financial_institution,
               payment_way_convenience_store,
               payment_way_web_trans,
               payment_way_ATM,
               payment_way_trans,
               payment_way_credit_card,
               payment_way_trans_by_postoffice,
               payment_way_trans_by_fina]


fig, ax = plt.subplots()
list_for_x_axis=[x for x in range(len(year_label))] # [0, 1, 2, 3, 4]
# print(list_for_x_axis)
for i in range(len(payment_way_list)):
    list_date_bar = [j + (i / len(payment_way_list)) for j in list_for_x_axis]
    ax.bar(list_date_bar,payment_way[i],label=payment_way_list[i],width=0.1)


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('金額')
ax.set_title('104~108年度多元繳稅契約統計')
ax.set_xticks([0,1,2,3,4],year_label)
ax.set_xlabel("年度")
ax.legend()


fig.tight_layout()

plt.show()

for i in range(len(payment_way)):
    print(f"繳費方式:{payment_way_list[i]}繳費合計{sum(payment_way[i])}千元；繳費平均值{sum(payment_way[i])/len(year_label)}千元")