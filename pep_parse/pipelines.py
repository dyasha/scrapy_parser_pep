import csv
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATE = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

class PepParsePipeline:

    def open_spider(self, spider):
        self.status = {}

    def process_item(self, item, spider):
        self.status[item['status']] = self.status.get(item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        file_name = f'status_summary_{DATE}.csv'
        file_path = results_dir / file_name
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            writer = csv.writer(f, dialect='unix')
            writer.writerows(self.status.items())
            f.write(f'Total,{sum(self.status.values())}\n')
