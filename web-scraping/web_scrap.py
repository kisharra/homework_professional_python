import bs4
import requests
import json
from fake_headers import Headers
from pprint import pprint



def get_fake_headers():
    '''Get fake headers'''
    return Headers(browser="chrome", os="linux").generate()  # Get fake headers


def get_data(url):
    '''Get data from url'''
    response = requests.get(url, headers=get_fake_headers())  # Get response from url
    page_data = bs4.BeautifulSoup(response.text, features='lxml')
    vacancies = page_data.find_all(class_='serp-item serp-item_simple serp-item_link serp-item-redesign')

    data = []  # Create an empty list
    for vacancy in vacancies:  # Go through the list
        h2_tag = vacancy.find('h2', class_='bloko-header-section-2')  # Find tags what we need
        a_tag = h2_tag.find('a')  
        title = a_tag.find('span').text.strip()
        link = a_tag['href']

        div_tag = vacancy.find('div', class_='compensation-labels--xC4zhiLojEYQtDuE4Qcf')  #Find salary with condition - "If selary is not specified then 'зарплата не указана'"
        if div_tag:
            selaty_tag = div_tag.find('span', class_='bloko-text')
            if selaty_tag:
                selary = selaty_tag.text
            else:
                selary = 'зарплата не указана'
        else:
            selary = 'зарплата не указана'

        company = vacancy.find('span', class_='company-info-text--O32pGCRW0YDmp3BHuNOP').text  
        city_tag =  vacancy.find('div', class_='info-section--u_omJryeVsCvqQyS23m_')
        city = city_tag.find('span', class_='fake-magritte-primary-text--qmdoVdtVX3UWtBb3Q7Qj').text

        description_response = requests.get(link, headers=get_fake_headers())  # Get response from link in vacancy and find description
        description_page = bs4.BeautifulSoup(description_response.text, features='lxml')
        description = description_page.find('div', class_='vacancy-description').text

        if 'Django' in description and 'Flask' in description:  # Check if Django or Flask in description then add all data to list with dictionary
            data.append({
                'Vacancy': title,
                'Link': link,
                'Selary': selary,
                'Company': company,
                'City': city
                })
    return data


def save_to_json(data):
    '''Save data to json file'''
    with open('/file_storage/homework_rep/web-scraping/vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    '''Get data from url and save to json file'''
    url = input('Enter url: ')
    data = get_data(url)
    save_to_json(data)
    