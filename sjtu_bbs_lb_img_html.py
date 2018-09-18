import urllib.request
from urllib.request import urlretrieve
import os

def read_page(url): #通过url读取页面可读信息生成str
    file = urllib.request.urlopen(url)
    data = file.read()
    g = open("read_page.txt",'w',encoding ='gbk')
    g.write(str(data))
    g.close()
    g = open('read_page.txt', 'r')
    g = g.read()
    os.remove("read_page.txt")
    return g

def find_sub_page(main_page_content): #找到子页面链接并生成list
    f = main_page_content
    list1 = []
    a = f.find("reid,");
    b = f.find(".html")+5
    part_url = f[a:b]
    while len(part_url) != 0:
        son_url = "https://bbs.sjtu.edu.cn/bbstcon,board,LoveBridge,"+str(part_url)
        list1.append(str(son_url))
        f = f[b:]
        a = f.find("reid,");
        b = f.find(".html")+5
        part_url = f[a:b]   
    return list1

def find_img(sub_page_content, sub_page_url): #需要页面信息和页面url两个参数，找到页面图片链接并分别生成多个子页面的图片list
    f = sub_page_content
    list2= []
    a = f.find("IMG SRC=")
    b = f.find("onload=")
    img_num = f[a:b][9:-2]
    while len(f[a:b]) !=0:
        img_url = "https://bbs.sjtu.edu.cn"+str(img_num)
        spu = sub_page_url
        list_temp = [img_url,spu]
        list2.append(list_temp)
        f= f[(b+10):]
        a = f.find("IMG SRC=")
        b = f.find("onload=")
        img_num = f[a:b][9:-2]
    return list2

def dl_img(url): #下载图片到文件夹
    purl = url
    pic_data = urllib.request.urlopen(url)
    pic_data = pic_data.read()
    ID = str(purl[-8:-4])
    ftype = str(purl[-3:])
    g = open(str(ID)+"."+str(ftype),'wb')
    g.write(pic_data)
    g.close()
    pic_name = str(ID)+"."+str(ftype)
    pic_html_element ="<img src=\""+str(pic_name)+"\" alt=\"figure\" width=\"22%\">\n"
    return pic_html_element

#用户输入及界面显示的内容
rng = input("起始页面号码：")
page = input("所需要的页数：")
print("下载中。。。。。。")


content = ""
list3 = []

#调用函数下载（无异常处理模块）
for i in range(int(page)):
    url = "https://bbs.sjtu.edu.cn/bbstdoc,board,LoveBridge,page,"+str(int(rng)-int(i))+".html"

    var1 = read_page(url)
    var2 = find_sub_page(var1)
    
    
    for each in range(len(var2)):
        var3 = read_page((var2[each]))
        var4 = find_img(var3,var2[each])
        list3.extend(var4)

for each in range(len(list3)):
    dl_img(list3[each][0])
    content = content+"<a href=\""+str(list3[each][1])+"\">"+str(dl_img(list3[each][0]))+"</a>\n"


html = "<!DOCTYPE html>\n<html>\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>Gallary</title>\n</head>\
\n<body>\n"+content+"\n</body></html>"
    
html_file = open("gallary.html",'w')
html_file.write(html)
html_file.close()

print("下载完成！！！")


