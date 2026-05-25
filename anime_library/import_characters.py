import os
import django
import openpyxl
from datetime import datetime, date

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_library.settings')
django.setup()

from anime.models import Anime
from characters.models import Character


def parse_birthday(birthday):
    if not birthday:
        return None
    if isinstance(birthday, (datetime, date)):
        return birthday.strftime('%Y-%m-%d')

    b_str = str(birthday).strip().split(' ')[0]
    b_str = b_str.replace('..', '.').replace('/', '.')

    try:
        parts = b_str.split('.')
        if len(parts) == 3:
            day, month, year = parts[0], parts[1], parts[2]
            if len(year) == 4:
                return f"{year}-{int(month):02d}-{int(day):02d}"
            elif len(day) == 4:
                year, month, day = parts[0], parts[1], parts[2]
                return f"{year}-{int(month):02d}-{int(day):02d}"
    except Exception:
        pass

    return None


def import_from_excel():
    file_name = 'anime_data.xlsx'

    if not os.path.exists(file_name):
        print(f"❌ Ошибка: Файл '{file_name}' не найден!")
        return

    print("Начинаю великое переселение персонажей из Excel 🐾")

    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row or len(row) < 3 or not row[2]:
            continue

        anime_title = row[1]  # аніме
        char_name = row[2]  # ім'я
        role = row[3]  # роль
        age = row[4]  # вік
        description = row[5]  # опис персонажа
        birthday = row[6]  # день народження
        family = row[7]  # сім'я

        # Безопасное приведение возраста к числу
        try:
            age_val = int(age) if age is not None else None
        except (ValueError, TypeError):
            age_val = None

        birthday_val = parse_birthday(birthday)

        # Получаем или создаем аниме (чисто по названию)
        anime_obj, _ = Anime.objects.get_or_create(title=anime_title)

        try:
            # Ищем или создаем персонажа
            character_obj, created = Character.objects.get_or_create(
                name=char_name,
                anime=anime_obj,
                defaults={
                    'role': role if role else '',
                    'age': age_val,
                    'description': description if description else '',
                    'birthday': birthday_val,
                }
            )

            # МАГИЯ ОБНОВЛЕНИЯ: Если персонаж уже был, мы всё равно обновляем ему описание,
            # чтобы применить красивые переносы строк из Excel!
            if not created and description:
                character_obj.description = description
                character_obj.role = role if role else character_obj.role
                character_obj.age = age_val if age_val is not None else character_obj.age
                character_obj.birthday = birthday_val if birthday_val else character_obj.birthday
                character_obj.save()
                print(f"🔄 Принудительно обновлены данные для: {char_name}")

            # Обработка связей "Семья"
            if family:
                try:
                    for name in str(family).split(','):
                        name = name.strip()
                        if name:
                            fam_char, _ = Character.objects.get_or_create(name=name, anime=anime_obj)
                            character_obj.family.add(fam_char)
                except Exception as m2m_err:
                    print(f"⚠️ Не удалось связать поле family для {char_name}: {m2m_err}")

            if created:
                print(f"✨ Добавлен персонаж: {char_name} ({anime_title})")

        except Exception as e:
            print(f"❌ Ошибка при добавлении {char_name}: {e}")

    print("Магия завершена! Все персонажи занесены в твои архивы. 🎉")


if __name__ == '__main__':
    import_from_excel()