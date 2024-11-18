import json

from lxml import etree
from lxml.etree import _Element
from lxml.html import Element

# xpath docs:
# https://www.w3school.com.cn/xpath/xpath_operators.asp
if __name__ == '__main__':
    with open('category.html', 'r', encoding='utf-8') as f:
        root: _Element = etree.HTML(f.read())
        # firsts = root.xpath('//span[@class="_1z7oCw9a"]')

        # 获取第一层
        categories = []
        lis: list[_Element] = root.xpath('//li[@class="e75ZP_DS"]')
        for li in lis:
            a = li.xpath('./a')[0]
            href = a.attrib['href']
            text = a.xpath('.//span')[0].text
            categories.append({
                'href': href,
                'text': text
            })
            print(text, href)

        second_divs = root.xpath('//div[@class="_1kBCxUd4"]')
        for index, second_div in enumerate(second_divs):
            if 'children' not in categories[index]:
                categories[index]['children'] = []
            for a in second_div.xpath('.//a'):
                href = a.attrib['href']
                text = a.xpath('.//img')[0].attrib['alt']
                categories[index]['children'].append({
                    'href': href,
                    'text': text
                })
        print(json.dumps(categories, indent=4, ensure_ascii=False))