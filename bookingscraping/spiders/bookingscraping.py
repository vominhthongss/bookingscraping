import scrapy
import requests
import datetime
today = datetime.datetime.now()  # lấy ngày hiện tại
tomorrow = today + datetime.timedelta(1)  # lấy ngày hôm sau


class BookingScraping(scrapy.Spider):
    name = 'bookingscraping'

    def __init__(self, city='', *args, **kwargs):
        super(BookingScraping, self).__init__(*args, **kwargs)
        self.city = city
        print("city = "+city)

    def start_requests(self):
        for offset in range(0, 2000, 25):
            url = "https://www.booking.com/searchresults.vi.html?checkin_month={in_month}" \
                "&checkin_monthday={in_day}&checkin_year={in_year}&checkout_month={out_month}" \
                "&checkout_monthday={out_day}&checkout_year={out_year}&group_adults={people}" \
                "&group_children=0&order=price&ss={city}%2C%20&offset={offset}"\
                .format(in_month=today.strftime("%m"),  # tháng hôm nay
                        in_day=today.strftime("%d"),  # ngày hôm nay
                        in_year=today.strftime("%Y"),  # năm hôm nay
                        out_month=tomorrow.strftime("%m"),  # tháng ngày mai
                        out_day=tomorrow.strftime("%d"),  # ngày mai
                        out_year=tomorrow.strftime("%Y"),  # năm ngày mai
                        people='2',  # mặc định là 2 người
                        city=getattr(self, 'city'),
                        offset=offset)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
                'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            }
            yield scrapy.http.Request(url, headers=headers)

    def parse(self, response):
        for ti in response.css('div.sr_item'):
            yield{
                'tenks': ti.css('span.sr-hotel__name::text').get(),
                'gia': ti.css('div.bui-price-display__value::text').get(),
                'loai_phong': ti.css('strong::text').get(),
                'giuong': ti.css('div.c-beds-configuration::text').get(),
                'diem': ti.css('div.bui-review-score__badge::text').get(),
                'danh_gia': ti.css('div.bui-review-score__title::text').get(),
                'so_danh_gia': ti.css('div.bui-review-score__text::text').get(),
                'url': ti.css('a.hotel_name_link::attr(href)').get()
            }
