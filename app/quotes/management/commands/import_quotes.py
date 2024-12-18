import csv
from django.core.management.base import BaseCommand
from quotes.models import Celebrity, Quote

class Command(BaseCommand):
    help = 'Import celebrities and their quotes from a CSV file, with optional cleanup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clean',
            action='store_true',
            help='Clean existing data before importing new data'
        )

    def handle(self, *args, **options):
        # 检查是否需要清理旧数据
        if options['clean']:
            self.stdout.write("Cleaning existing data...")
            Quote.objects.all().delete()  # 清空 Quotes 表
            Celebrity.objects.all().delete()  # 清空 Celebrities 表
            self.stdout.write(self.style.SUCCESS("Existing data has been cleaned."))

        # 导入新数据
        file_path = 'quotes_data.csv'  # CSV 文件路径
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                celeb, created = Celebrity.objects.get_or_create(
                    name=row['name'],
                    title=row['title']
                )
                Quote.objects.create(
                    content=row['content'],
                    tag=row['tag'],
                    celebrity=celeb
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported quotes!'))
