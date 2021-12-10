from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


page_counter = -108

url = "https://www.public.gr/search/public/searchResultsSN.jsp?sn.q=%CE%B2%CE%B9%CE%B2%CE%BB%CE%B9%CE%B1&sn.l=108&sn.o="
#Path may change
chrome_driver_path = r"C:\\Users\\k.kivotos\\Desktop\\scrapper\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--headless')
s=Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s,options=options, executable_path=chrome_driver_path)


print("  _____       _     _ _        ____              _        ")
print(" |  __ \     | |   | (_)      |  _ \            | |       ")
print(" | |__) |   _| |__ | |_  ___  | |_) | ___   ___ | | _____ ")
print(" |  ___/ | | | '_ \| | |/ __| |  _ < / _ \ / _ \| |/ / __|")
print(" | |   | |_| | |_) | | | (__  | |_) | (_) | (_) |   <\__ \\")
print(" |_|    \__,_|_.__/|_|_|\___| |____/ \___/ \___/|_|\_\___/")
print("____________________________________________________\n")
user_input = int(input("\nGive a discount price:"))
pages_to_scan = int(input("Give a number of pages to scan:"))
print("____________________________________________________\n")                                            

for i in range(0,pages_to_scan):
	page_counter+=108
	browser.get(url+str(page_counter))
	html = browser.page_source
	soup = BeautifulSoup(html, features="html.parser")

	books = soup.find_all('div', class_ = "col-sm-6 col-lg-4")

	# In every book div
	for tag in books:
		# Get the url of each book we are processing
		book_url = tag.get('data-sna-url')
		# Get all the children div that have the class
		discount = tag.find("div", class_ = "discount web-offer")
		if(discount==None):
			continue
		else:
			if(user_input<=int(discount.text.strip()[1:3])):
				print(book_url[2:])



browser.quit()