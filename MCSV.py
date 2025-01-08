import csv
import glob

class CSV:
    def read_csv(self, url):
        with open(url) as file:
            csv_data = csv.reader(file, delimiter=';')
            return list(csv_data)

    def get_all_data_paths(self, url):
        list_url = glob.glob(url)
        return list_url

