def main():
    import requests
    from bs4 import BeautifulSoup

    webpage = requests.get("https://www.foxnews.com/")
    src = webpage.content
    soup = BeautifulSoup(src, 'html.parser')

    articles = []

    for h2_tag in soup.find_all("h2"):
        a_tag = h2_tag.find('a')
        h_ref_attribute = a_tag.attrs['href']
        if "video" in h_ref_attribute:
            continue
        if h_ref_attribute[0] == "/":
            h_ref_attribute = "https:" + h_ref_attribute
        articles.append(h_ref_attribute)

    search_word = input("Select the word you want to search\n")

    f = open("output.txt", "a")

    for article in articles:
        webpage = requests.get(article)
        newsoup = BeautifulSoup(webpage.content,'html.parser')
        for p_tag in newsoup.find_all('p'):
            if search_word in p_tag.getText():
                f.write(p_tag.getText().strip() + "\n")

    f.close()


if __name__ == "__main__":
    main()