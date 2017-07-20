
import csv
import urllib.request
from bs4 import BeautifulSoup

BASE_URL = 'https://www.weblancer.net/jobs/'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup('ul')[3:4]
    lis = [li for ul in paggination for li in ul.findAll('li')][-1]
    for link in lis.find_all('a'):
        var1 = (link.get('href'))

    var2 = var1[-3:]
    #print(var1)
    return int(var2)


def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Тема', 'Описание', 'Цена', 'Заявки'))

        for project in projects:
            writer.writerow((project['title'], project['description'], project['price'], project['application']))

def parse(html):
    soup = BeautifulSoup(html,'html.parser')
    table = soup.find('div', class_='container-fluid cols_table show_visited')

    projects = []

    for row in table.find_all('div', class_='row'):
        cols = row.find_all('div')



        projects.append({
            'title':cols[0].a.text,
            #'categories' : [category.text for category in cols[3].find_all('a', class_='text-muted')],  #
            'description' : cols[3].text.strip(),
            'price' : cols[1].text.strip(),
            'application' : cols[2].text.strip()
        })

    for project in projects:
        print(project)



    #print(rows)

def main():
    page_count = get_page_count(get_html(BASE_URL))

    print('Всего найдено страниц %d'%page_count)

    projects = []

    for page in range(1, page_count+1):
        print('Парсинг %d%%'%(page/page_count * 100))
        projects.extend(parse(get_html(BASE_URL + '?page=%d'%page)))

    #for project in projects:
     #   print(project)
    save(projects, 'projects.csv')

if __name__ == '__main__':
    main()
