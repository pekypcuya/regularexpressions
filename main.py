
import csv
import re
from pprint import pprint

# Читаем адресную книгу
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# 1. Приводим ФИО к правильному формату
for contact in contacts_list[1:]:
    full_name = " ".join(contact[:3]).split()

    contact[0] = full_name[0] if len(full_name) > 0 else ""
    contact[1] = full_name[1] if len(full_name) > 1 else ""
    contact[2] = full_name[2] if len(full_name) > 2 else ""

# 2. Приводим телефоны к единому формату
def normalize_phone(phone):
    pattern = (
        r"(?:\+7|8)?\s*"
        r"\(?(\d{3})\)?[\s-]*"
        r"(\d{3})[\s-]*"
        r"(\d{2})[\s-]*"
        r"(\d{2})"
        r"(?:\s*\(?(доб\.?)\s*(\d+)\)?)?"
    )

    match = re.search(pattern, phone)

    if not match:
        return phone

    code, p1, p2, p3, ext_label, ext = match.groups()

    result = f"+7({code}){p1}-{p2}-{p3}"

    if ext:
        result += f" доб.{ext}"

    return result


for contact in contacts_list[1:]:
    contact[5] = normalize_phone(contact[5])

# 3. Объединяем дубликаты по фамилии и имени
merged = {}

for contact in contacts_list[1:]:
    key = (contact[0].strip(), contact[1].strip())

    if key not in merged:
        merged[key] = contact[:]
    else:
        existing = merged[key]

        for i in range(len(existing)):
            if not existing[i] and contact[i]:
                existing[i] = contact[i]

# Формируем итоговый список
contacts_list = [contacts_list[0]] + list(merged.values())

pprint(contacts_list)

# Сохраняем результат
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter=",")
    writer.writerows(contacts_list)

print("Готово! Результат сохранён в phonebook.csv")
