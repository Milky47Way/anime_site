import os
import django
import openpyxl
from datetime import datetime, date
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
            if len(parts[2]) == 4:
                day, month, year = parts[0], parts[1], parts[2]
                return f"{year}-{int(month):02d}-{int(day):02d}"
            elif len(parts[0]) == 4:
                year, month, day = parts[0], parts[1], parts[2]
                return f"{year}-{int(month):02d}-{int(day):02d}"
    except Exception:
        pass

    return b_str


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

        number = row[0]  # №
        anime_title = row[1]  # аніме
        char_name = row[2]  # ім'я
        role = row[3]  # роль
        age = row[4]  # вік
        description = row[5]  # опис
        birthday = row[6]  # день народження
        family = row[7]  # сім'я

        try:
            age_val = int(age) if age is not None else None
        except (ValueError, TypeError):
            age_val = None

        birthday_val = parse_birthday(birthday)
        anime_obj, _ = Anime.objects.get_or_create(title=anime_title)

        try:
            character_obj, created = Character.objects.get_or_create(
                name=char_name,
                anime=anime_obj,
                defaults={
                    'role': role if role else '',
                    'age': age_val,
                    'description': description if description else '',
                    'birthday': birthday_val if birthday_val else None,
                }
            )

            if family:
                try:
                    related_model = Character._meta.get_field('family').remote_field.model

                    if related_model == Character:
                        for name in str(family).split(','):
                            name = name.strip()
                            if name:
                                fam_char, _ = Character.objects.get_or_create(name=name, anime=anime_obj)
                                character_obj.family.add(fam_char)
                    else:
                        fam_obj, _ = related_model.objects.get_or_create(name=str(family).strip())
                        character_obj.family.add(fam_obj)
                except Exception as m2m_err:
                    print(f"⚠️ Предупреждение для {char_name}: не удалось связать поле family ({m2m_err})")

            if created:
                print(f"✨ Добавлен персонаж: {char_name} ({anime_title})")
            else:
                print(f" Пропущен (уже есть в базе): {char_name}")

        except Exception as e:
            print(f"❌ Ошибка при добавлении {char_name}: {e}")
            return

    print("Магия завершена! Все персонажи успішно занесені в твої архіви. 🎉")


if __name__ == '__main__':
    import_from_excel()