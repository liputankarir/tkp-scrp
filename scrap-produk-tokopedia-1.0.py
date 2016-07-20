'''
SCRAP TOKOPEDIA.COM PRODUCTS
Versi 1. created 8 Juli 2016 by Ardya

Pre-requirements:
01. User must provide a file consisting products url (one url per-line)
02. This script use mobile version URL (m.tokopedia.com) not full website URL (www.tokopedia.com)

Input Argument:
01. URL of products file 
02. Ouput Data File (where the scrape results stored)
03. Target directory to save image of products

Notes:
01. After run this script, please inspect the results manually
'''
#import module
import sys, re, urllib2, time, random, csv, urllib
#import beautifulsoup module
from bs4 import BeautifulSoup  

#file consisting products url
namafileurl = sys.argv[1]
#output file whare the scrape data stored
namafiledataproduk = sys.argv[2]
#target directory where the images of products stored
namafoldergambarproduk = sys.argv[3] 
#product columns initialization
#Nama Produk = product name, Harga Ecer = retail price, Minimal Pembelian = min. purchase quantity, Berat Produk = product weight, Asuransi = insurance, Kondisi Product = Product condition, Kategori = category, Deskripsi = description, Kuantitas Grosir = wholesale quantity, Harga Grosir = wholesale price
fieldproduk = ['Nama Produk', 'Harga Ecer', 'Minimal Pembelian', 'Berat Produk', 'Asuransi', 'Kondisi Produk', 'Kategori 1', 'Kategori 2', 'Kategori 3', 'Deskripsi', 'Kuantitas Grosir 1', 'Harga Grosir 1', 'Kuantitas Grosir 2','Harga Grosir 2', 'Kuantitas Grosir 3','Harga Grosir 3']

#open input file (url of products file)
with open(namafileurl) as fileurlproduk, open(namafiledataproduk, "wb") as filedataproduk:
    #csv writer initialization
    writer = csv.DictWriter(filedataproduk, fieldnames=fieldproduk) 
    #product counter
    counter_produk = 1
    #take url from file. one url per-line
    for urlproduk in fileurlproduk:
        #print "URL Produk = " + urlproduk
        dataproduk = urllib2.urlopen(urlproduk).read()
        dataproduk = BeautifulSoup(dataproduk, 'html.parser')
        
        #get product name. 
        for temp in dataproduk.find_all('h1'):
            namaproduk = temp.get_text() 
            #print "Nama Produk = " + namaproduk
        
        #get detail information of product
        for temp in dataproduk.find_all("div", "detail-info"):
            info = temp.get_text()
            #get product weight
            berat = re.search( r'Berat(.*?)Terjual', info)
            berat = berat.group(1)
            #print "Berat = " + berat.group(1)

            #get insurance (there are two option, wajib = need insurance or opsional = insurance is optional)
            asuransi = re.search( r'Asuransi(.*?)Kondisi', info)
            asuransi = asuransi.group(1)
            #print "Asuransi = " + asuransi.group(1) 
            
            #get product condition (new or used/secondhand)
            kondisi = re.search( r'Kondisi(.*?)Pemesanan', info)
            kondisi = kondisi.group(1)
            #print "Kondisi = " + kondisi.group(1)

            #get minimum purchase quantity. I get problem using regex for this one, so I just use find
            minpemesanan = info[(info.find("Min") + 4):]
            #print "Pemesanan Min. = " + minpemesanan
        
        #get product description
        for temp in dataproduk.find_all("p", itemprop= "description"):
            deskripsi = temp.get_text()
            #print "Deskripsi = " + deskripsi
        
        #get retail price of product
        for temp in dataproduk.find_all("div", class_= "product-pricetag"):
            hargaproduk = temp.get_text()
            #print "Harga Produk = " + hargaproduk
        
        #initialize empty list for product category
        kategoriproduk = []
        #get product category. from h2 tag
        kategoriproduk_soup = dataproduk.find_all("h2")
        #the category can be divided into. MAIN CATEGORY => SUB-MAIN CATEGORY => MINOR CATEGORY. and when using h2 tag to get category, there will be also 2 unnecessary result 
        #the unnecessary result or data located at the beginning and at the end. thats why i use for loop starting from 1 (not 0) until category result - 1 (not just category result)
        for x in range(1, len(kategoriproduk_soup)-1):
            kategoriproduk.append(kategoriproduk_soup[x].get_text())
            #print "Kategori Produk = " + kategoriproduk[x-1]
        
        #get data for wholesale price if any. if there is no wholesale price for the product, this process will return empty list.
        for temp in dataproduk.find_all("ul", class_= "product-ratingstat", limit=1): 
            #create a new string data to be "soup-ed".
            grosirhtml = str(temp) 
            #this is the new soup
            grosirdata = BeautifulSoup(grosirhtml, 'html.parser')
            #get wholesale quantity
            grosirdata_kuantiti = grosirdata.find_all("span", class_= "product-ratingstat_quantity") 
            #get wholesale price
            hargagrosir_list = grosirdata.find_all("span", class_= "bold")
            kuantitigrosir = []
            hargagrosir = []
            for x in range(0,len(grosirdata_kuantiti)):
                #tried to group wholesale quantity with it corresponding wholesale price
                kuantitigrosir.append(grosirdata_kuantiti[x].get_text()) 
                hargagrosir.append(hargagrosir_list[x].get_text())
                #print "Range kuantitas = " + kuantitigrosir[x] + " Harga Grosir = " + hargagrosir[x]
        
        #get url for product image. using same method with scraping wholesale quantity and prices above.
        for temp in dataproduk.find_all("div", class_= "product-image-holder", limit = 1): 
            #create a new string data to be soup-ed
            datagambar = str(temp)
            #make a new soup
            datagambar_soup = BeautifulSoup(datagambar, 'html.parser')
            
            #extracting image url
            image_counter = 0
            for linkgambar_list in datagambar_soup.find_all('a'):
                temp_gambar = linkgambar_list.get('href')
                #remove "#" from result
                if temp_gambar != "#":
                    image_counter = image_counter + 1
                    #save image
                    urllib.urlretrieve(temp_gambar, namafoldergambarproduk + namaproduk + "-" + str(image_counter) + ".jpg")
                    #print "Link Gambar = " + str(linkgambar)
        
        #check the category result. if there are less than 3 category (sub-category) than, append "-" to make it three.
        if len(kategoriproduk) < 3:
            for x in range(len(kategoriproduk),3):
                kategoriproduk.append("-")
        if len(kuantitigrosir) < 3:
            for x in range(len(kuantitigrosir),3):
                kuantitigrosir.append("-")
                hargagrosir.append("-")

        #write the result as csv file
        writer.writerow({fieldproduk[0]: namaproduk, fieldproduk[1]: hargaproduk, fieldproduk[2]: minpemesanan, fieldproduk[3]: berat, fieldproduk[4]: asuransi, fieldproduk[5]: kondisi, fieldproduk[6]: kategoriproduk[0], fieldproduk[7]: kategoriproduk[1], fieldproduk[8]: kategoriproduk[2], fieldproduk[9]: deskripsi, fieldproduk[10]: kuantitigrosir[0], fieldproduk[11]: hargagrosir[0], fieldproduk[12]: kuantitigrosir[1], fieldproduk[13]: hargagrosir[1], fieldproduk[14]: kuantitigrosir[2], fieldproduk[15]: hargagrosir[2]})
        #print the product counter into terminal
        print counter_produk
        counter_produk = counter_produk + 1
        #give some short delay before scraping next product
        time.sleep(random.randrange(2, 6))
