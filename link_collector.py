from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

pd.set_option('max_columns', None)

def get_parameter_html_table(url):    
    try:
        if url and url[0:7] != "http://" and url[0:8] != "https://" and url[0:6]:
            url = "http://" + url

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # create lists
        urls = []

        for link in soup.find_all('a'):
            a = link.get('href')
            a = a.split('?', 1)
            a = a if len(a) == 2 else [a[0], None]

            url_part1 = a[0]

            try:
                r = requests.get(url_part1, headers={'User-agent': 'link-checker', 'text': ''})

                if r.status_code == 200:
                    status = 'Success'
                elif r.status_code == 404:
                    status == 'Not Found'
                else:
                    status = 'Unknown'
            except:
                status = 'Unknown'

            if re.match('^\w+', url_part1):
                url_part1 = f'<a href="{url_part1}">{url_part1}</a>'
            else:
                url_part1 = f'<a href="{url + url_part1}">{url_part1}</a>'

            parameters = a[1].split('&') if a[1] is not None else [a[1]]

            a_text = link.string
            a_text =  f'{a_text[:40]}...' if (a_text is not None) and (len(a_text) > 40) else a_text
            
            a_img = link.find('img').get('src') if link.find('img') is not None else None
            if a_img is not None and re.match('^\w+', a_img):
                a_img = f'<a href="{a_img}" target="_blank">Image</a>' if a_img is not None else None
            elif a_img is not None:
                a_img = f'<a href="{url + a_img}" target="_blank">Image</a>' if a_img is not None else None

            record = [url_part1, status, a_text, a_img]
            record.extend(parameters)

            urls.append(record)
            
        df = pd.DataFrame(data=urls)
        new_header = ['URL', 'Status', 'Text', 'Image']
        for i in range(4, len(df.columns)):
            new_header.append(f'Parameter_{i-3}')
        df.columns = new_header
        df.index += 1 
        df.fillna('', inplace=True)
        table = df.to_html(table_id='result-table', justify='left', na_rep='', escape=False, classes=['table-responsive-sm', 'table-striped', 'table-responsive', 'fixed-table-body'])
        return (table)
    except Exception as e:
        return '<h2>Sorry, something went wrong.  Please, try again.</h2>'

if __name__ == "__main__":
    url = "https://www.google.com/"
    get_parameter_html_table(url)