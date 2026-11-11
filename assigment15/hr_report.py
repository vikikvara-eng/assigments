
from pathlib import Path
import sys
from datetime import datetime
import csv
from collections import Counter
import json
import os
import time

file_path = Path("data") / "employees.csv"
output_file = Path("output")

if file_path.exists():
    file_address = file_path.resolve()
    output_file.mkdir(exist_ok=True)
    print(file_address)
else:
    print("ფაილი ვერ მოიძებნა")
    sys.exit(1)


def backup_file(src, dst):
    line_count = 0

    with open(src, "r", encoding="utf-8", newline="") as f:
        with open(dst, "w", encoding="utf-8", newline="") as b:
            for line in f:
                b.write(line)
                line_count += 1

    return line_count


backup_lines = backup_file(file_path, output_file / "employees_backup.csv")
print(backup_lines)


def log(message):
    timestamp = datetime.now().isoformat()

    with open(output_file / "log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"{timestamp} - {message}\n")


log("პროგრამა გაეშვა წარმატებით")


try:
    with open(output_file / "lock.txt", "x", encoding="utf-8") as lock_file:
        lock_file.write(datetime.now().isoformat())

except FileExistsError:
    print("ანგარიში უკვე შექმნილია")


with open(file_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)
    print(header)

    for i in range(3):
        row = next(reader)
        print(row)


employee_count = 0

with open(file_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        employee_count += 1

print("თანამშრომლების რაოდენობა:", employee_count)


departments = {}
active_employees = []
active_count = 0
inactive_count = 0

with open(file_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        department = row["department"]
        salary = int(row["salary"])
        is_active = row["is_active"].strip().lower() == "true"

        if department not in departments:
            departments[department] = {
                "count": 0,
                "total_salary": 0
            }

        departments[department]["count"] += 1
        departments[department]["total_salary"] += salary

        if is_active:
            active_count += 1

            active_employees.append({
                "id": row["id"],
                "full_name": row["first_name"] + " " + row["last_name"],
                "department": department,
                "salary": salary
            })
        else:
            inactive_count += 1


for department, data in departments.items():
    data["avg_salary"] = data["total_salary"] / data["count"]


print("აქტიური თანამშრომლები:", active_count)
print("არააქტიური თანამშრომლები:", inactive_count)


top_three = sorted(
    active_employees,
    key=lambda employee: employee["salary"],
    reverse=True
)[:3]

print("ტოპ 3 აქტიური თანამშრომელი:", top_three)


department_stats = []

for department, data in departments.items():
    department_stats.append({
        "department": department,
        "employee_count": data["count"],
        "avg_salary": round(data["avg_salary"], 2)
    })


department_stats.sort(
    key=lambda item: item["avg_salary"],
    reverse=True
)


with open(
    output_file / "department_stats.csv",
    "w",
    encoding="utf-8",
    newline=""
) as file:

    fieldnames = ["department", "employee_count", "avg_salary"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(department_stats)


high_earners = []

for employee in active_employees:
    if employee["salary"] >= 5000:
        high_earners.append([
            employee["id"],
            employee["full_name"],
            employee["department"],
            employee["salary"]
        ])


with open(
    output_file / "high_earners.csv",
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow(["id", "full_name", "department", "salary"])
    writer.writerows(high_earners)


log("მეორე ნაწილი დასრულდა")


def safe_read(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()

    except FileNotFoundError:
        log(f"ფაილი ვერ მოიძებნა: {path}")
        return ""

    except UnicodeDecodeError:
        log(f"Unicode შეცდომა: {path}")

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="replace"
        ) as file:
            return file.read()


missing_file = safe_read(output_file / "missing.txt")
print(missing_file)


with open(output_file / "broken.txt", "wb") as file:
    file.write(bytes([99, 97, 102, 233, 32, 255]))


broken_file = safe_read(output_file / "broken.txt")
print(broken_file)


city_counter = Counter()

with open(file_path, "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        city_counter[row["city"]] += 1


top_cities = city_counter.most_common(3)

print("ტოპ 3 ქალაქი:", top_cities)


with open(output_file / "cities.txt", "w", encoding="utf-8") as file:
    print(top_cities, file=file)


def save_json_safe(data, path):
    temp_path = str(path) + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    os.replace(temp_path, path)


save_json_safe(department_stats, output_file / "summary.json")


log("მესამე ნაწილი დასრულდა")


class Timer:

    def __enter__(self):
        self.start_time = time.perf_counter()
        print("START")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.perf_counter()
        elapsed = end_time - self.start_time

        if exc_type is None:
            print("FINISH")
        else:
            print("FAILED:", exc_type.__name__)

        print("Execution time:", elapsed)

        return False


with Timer():
    print("მეორე ნაწილის შესრულება")


try:
    with Timer():
        result = 10 / 0

except ZeroDivisionError:
    print("ნულზე გაყოფა შეუძლებელია")


log("მეოთხე ნაწილი დასრულდა")


log("პროგრამა დასრულდა")
print("HR ანგარიში დასრულებულია!")
