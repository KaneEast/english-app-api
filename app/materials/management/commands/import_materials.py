import os
from django.core.management.base import BaseCommand
from materials.models import Material

class Command(BaseCommand):
    help = "Import materials from a folder of TXT files"

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str, help="Path to the folder containing TXT files")
        parser.add_argument(
            '--clean',
            action='store_true',
            help="Clear all existing materials before importing"
        )

    def handle(self, *args, **options):
        folder_path = options['folder_path']
        clear_existing = options['clean']

        # 清空现有数据（如果指定了 --clean 参数）
        if clear_existing:
            Material.objects.all().delete()
            self.stdout.write(self.style.WARNING("All existing materials have been deleted."))

        if not os.path.exists(folder_path):
            self.stdout.write(self.style.ERROR(f"Folder {folder_path} does not exist"))
            return

        # 遍历指定文件夹下的所有文件
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                file_path = os.path.join(folder_path, filename)

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # 提取文件中的数据
                link = lines[0].strip()
                title = lines[1].strip()
                category = lines[2].strip()
                content = ''.join(lines[4:]).strip()

                # 检查数据库中是否存在相同的 title
                if Material.objects.filter(title=title).exists():
                    self.stdout.write(self.style.WARNING(f"Material '{title}' already exists. Skipping."))
                    continue

                # 创建新的 Material 记录
                Material.objects.create(
                    link=link,
                    title=title,
                    category=category,
                    content=content
                )

                self.stdout.write(self.style.SUCCESS(f"Imported '{title}' successfully"))
