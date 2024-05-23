from websiteinfo import get_website_data


class Storage:
    def __init__(self):
        self.website_data = get_website_data()


storage = Storage()
