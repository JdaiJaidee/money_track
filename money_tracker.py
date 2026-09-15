# โปรแกรมบันทึกรายรับ-รายจ่ายส่วนตัว
# เก็บข้อมูลไว้ใน list

import datetime


def show_menu():
    print("\n===== โปรแกรมบันทึกรายรับ-รายจ่าย =====")
    print("1. เพิ่มรายการ")
    print("2. แสดงรายการทั้งหมด")
    print("3. สรุปยอดเงิน")
    print("4. ลบรายการ")
    print("5. แก้ไขรายการ")
    print("6. สรุปรายเดือน")
    print("7. สรุปตามหมวดหมู่")
    print("8. กราฟแท่งตามหมวดหมู่")
    print("9. Top 3 หมวดใช้จ่าย")
    print("10. ออกจากโปรแกรม")


def ask_date():
    # วันที่ต้องเป็นรูปแบบ ปปปป-ดด-วว เป็นตัวเลขเท่านั้น ห้ามใส่ตัวอักษร
    # วนถามซ้ำจนกว่าจะได้ค่าที่ถูกต้อง
    while True:
        date = input("วันที่ (ปปปป-ดด-วว เช่น 2026-09-14): ")
        date_parts = date.split("-")

        if len(date_parts) != 3:
            print("รูปแบบวันที่ไม่ถูกต้อง ต้องเป็น ปปปป-ดด-วว")
            continue

        year_text, month_text, day_text = date_parts

        if year_text.isdigit() == False or month_text.isdigit() == False or day_text.isdigit() == False:
            print("วันที่ต้องเป็นตัวเลขเท่านั้น")
            continue

        try:
            valid_date = datetime.date(int(year_text), int(month_text), int(day_text))
        except ValueError:
            print("วันที่นี้ไม่มีอยู่จริงในปฏิทิน")
            continue

        return valid_date.strftime("%Y-%m-%d")


def ask_type():
    print("1. รายรับ")
    print("2. รายจ่าย")
    type_choice = input("ประเภท: ")

    if type_choice == "1":
        return "รายรับ"
    elif type_choice == "2":
        return "รายจ่าย"
    else:
        return None


def ask_amount():
    # วนถามซ้ำจนกว่าจะได้จำนวนเงินที่เป็นตัวเลขและมากกว่า 0
    while True:
        amount_text = input("จำนวนเงิน: ")

        if amount_text.replace(".", "", 1).isdigit() == False:
            print("จำนวนเงินต้องเป็นตัวเลขมากกว่า 0 กรุณากรอกใหม่")
            continue

        amount = float(amount_text)

        if amount <= 0:
            print("จำนวนเงินต้องเป็นตัวเลขมากกว่า 0 กรุณากรอกใหม่")
            continue

        return amount


def ask_category():
    return input("หมวดหมู่: ")


def get_sorted_transactions(transactions):
    # เรียงตามวันที่จริง (แปลงเป็นตัวเลขก่อน กันกรณีไม่ได้ใส่เลข 0 นำหน้าเดือน/วัน)
    return sorted(transactions, key=lambda t: [int(part) for part in t["date"].split("-")])


def print_transaction_list(transactions):
    for i, transaction in enumerate(transactions, 1):
        print(
            i,
            transaction["date"],
            transaction["detail"],
            transaction["category"],
            transaction["type"],
            transaction["amount"],
            "บาท"
        )


def calculate_summary(transactions):
    income = 0
    expense = 0

    for transaction in transactions:
        if transaction["type"] == "รายรับ":
            income += transaction["amount"]
        elif transaction["type"] == "รายจ่าย":
            expense += transaction["amount"]

    balance = income - expense
    return income, expense, balance


def calculate_category_summary(transactions):
    # รวมยอดรายจ่ายแยกตามหมวดหมู่ เรียงจากมากไปน้อย
    category_totals = {}

    for transaction in transactions:
        if transaction["type"] == "รายจ่าย":
            category = transaction["category"]
            category_totals[category] = category_totals.get(category, 0) + transaction["amount"]

    return sorted(category_totals.items(), key=lambda item: item[1], reverse=True)


def add_transaction(transactions):
    print("\n--- เพิ่มรายการ ---")

    date = ask_date()
    detail = input("รายละเอียด: ")
    category = ask_category()

    transaction_type = ask_type()
    if transaction_type is None:
        print("เลือกประเภทไม่ถูกต้อง")
        return

    amount = ask_amount()

    transaction = {
        "date": date,
        "detail": detail,
        "category": category,
        "type": transaction_type,
        "amount": amount
    }

    transactions.append(transaction)
    print("บันทึกสำเร็จ")


def show_all_transactions(transactions):
    print("\n--- รายการทั้งหมด ---")

    if len(transactions) == 0:
        print("ยังไม่มีรายการ")
        return

    print(f"{'ลำดับ':<6}{'วันที่':<14}{'รายการ':<16}{'หมวดหมู่':<12}{'ประเภท':<10}{'จำนวนเงิน':>12}")
    print("-" * 70)

    for i, transaction in enumerate(get_sorted_transactions(transactions), 1):
        print(f"{i:<6}{transaction['date']:<14}{transaction['detail']:<16}{transaction['category']:<12}{transaction['type']:<10}{transaction['amount']:>10.2f} บาท")

    income, expense, balance = calculate_summary(transactions)

    print("-" * 70)
    print(f"รายรับรวม : {income:,.2f} บาท")
    print(f"รายจ่ายรวม: {expense:,.2f} บาท")
    print(f"คงเหลือ   : {balance:,.2f} บาท")


def show_summary(transactions):
    income, expense, balance = calculate_summary(transactions)

    print("\n--- สรุปยอดเงิน ---")
    print(f"รายรับทั้งหมด : {income:,.2f} บาท")
    print(f"รายจ่ายทั้งหมด: {expense:,.2f} บาท")
    print(f"เงินคงเหลือ   : {balance:,.2f} บาท")


def show_monthly_summary(transactions):
    print("\n--- สรุปรายเดือน ---")
    month = input("ระบุเดือน (ปปปป-ดด เช่น 2026-09): ")
    month_transactions = get_sorted_transactions([t for t in transactions if t["date"].startswith(month)])

    if len(month_transactions) == 0:
        print("ไม่มีรายการในเดือนนี้")
        return

    print("1. สรุปรวม")
    print("2. สรุปรายรับ")
    print("3. สรุปรายจ่าย")
    print("0. ย้อนกลับ")
    summary_choice = input("เลือกประเภทสรุป: ")

    if summary_choice == "0":
        return

    income, expense, balance = calculate_summary(month_transactions)

    if summary_choice == "2":
        print(f"พบ {len(month_transactions)} รายการในเดือน {month}")
        print_transaction_list([t for t in month_transactions if t["type"] == "รายรับ"])
        print(f"รายรับรวม: {income:,.2f} บาท")
    elif summary_choice == "3":
        print(f"พบ {len(month_transactions)} รายการในเดือน {month}")
        print_transaction_list([t for t in month_transactions if t["type"] == "รายจ่าย"])
        print(f"รายจ่ายรวม: {expense:,.2f} บาท")
    else:
        print(f"พบ {len(month_transactions)} รายการในเดือน {month}")
        print_transaction_list(month_transactions)
        print(f"รายรับรวม : {income:,.2f} บาท")
        print(f"รายจ่ายรวม: {expense:,.2f} บาท")


def show_category_summary(transactions):
    print("\n--- สรุปตามหมวดหมู่ (รายจ่าย) ---")
    category_summary = calculate_category_summary(transactions)

    if len(category_summary) == 0:
        print("ยังไม่มีรายการรายจ่าย")
        return

    for category, total in category_summary:
        print(f"{category} {total:,.2f} บาท")


def show_category_chart(transactions):
    print("\n--- กราฟแท่งตามหมวดหมู่ (รายจ่าย) ---")
    category_summary = calculate_category_summary(transactions)

    if len(category_summary) == 0:
        print("ยังไม่มีรายการรายจ่าย")
        return

    max_amount = category_summary[0][1]
    total_expense = sum(total for _, total in category_summary)
    name_width = max(len(category) for category, _ in category_summary)
    bar_width = 30

    for category, total in category_summary:
        bar_length = round(total / max_amount * bar_width) if max_amount > 0 else 0
        percent = total / total_expense * 100 if total_expense > 0 else 0
        bar = "█" * bar_length
        print(f"{category:<{name_width}} │{bar:<{bar_width}}│ {total:>10,.2f} บาท ({percent:5.1f}%)")


def show_top_categories(transactions, top_n=3):
    print(f"\n--- Top {top_n} หมวดใช้จ่าย ---")
    category_summary = calculate_category_summary(transactions)

    if len(category_summary) == 0:
        print("ยังไม่มีรายการรายจ่าย")
        return

    for category, total in category_summary[:top_n]:
        print(f"{category} {total:,.2f} บาท")


def ask_valid_index(transactions, question):
    # หมายเลขต้องเป็นตัวเลขและต้องอยู่ในรายการจริง ไม่งั้น list จะ error
    # กด 0 เพื่อยกเลิกและย้อนกลับไปหน้าหลัก
    index_text = input(question + "(0 = ย้อนกลับ): ")

    if index_text == "0":
        return None

    if index_text.isdigit() == False:
        print("กรุณาใส่หมายเลขเท่านั้น")
        return None

    index = int(index_text) - 1
    if index < 0 or index >= len(transactions):
        print("ไม่มีหมายเลขนี้ในรายการ")
        return None

    return index


def delete_transaction(transactions):
    print("\n--- ลบรายการ ---")

    if len(transactions) == 0:
        print("ยังไม่มีรายการ")
        return

    sorted_transactions = get_sorted_transactions(transactions)
    print_transaction_list(sorted_transactions)
    index = ask_valid_index(sorted_transactions, "ลบรายการที่ (ใส่หมายเลข): ")
    if index is None:
        return

    selected = sorted_transactions[index]
    transactions.remove(selected)
    print("ลบรายการเรียบร้อยแล้ว")


def edit_transaction(transactions):
    print("\n--- แก้ไขรายการ ---")

    if len(transactions) == 0:
        print("ยังไม่มีรายการ")
        return

    sorted_transactions = get_sorted_transactions(transactions)
    print_transaction_list(sorted_transactions)
    index = ask_valid_index(sorted_transactions, "แก้ไขรายการที่ (ใส่หมายเลข): ")
    if index is None:
        return

    real_index = transactions.index(sorted_transactions[index])

    print("กรอกข้อมูลใหม่แทนของเดิม")

    new_date = ask_date()
    new_detail = input("รายละเอียด: ")
    new_category = ask_category()

    new_type = ask_type()
    if new_type is None:
        print("เลือกประเภทไม่ถูกต้อง ยกเลิกการแก้ไข")
        return

    new_amount = ask_amount()

    transactions[real_index] = {
        "date": new_date,
        "detail": new_detail,
        "category": new_category,
        "type": new_type,
        "amount": new_amount
    }

    print("แก้ไขรายการเรียบร้อยแล้ว")


def main():
    transactions = []

    while True:
        show_menu()
        choice = input("เลือกเมนู: ")

        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            show_all_transactions(transactions)
        elif choice == "3":
            show_summary(transactions)
        elif choice == "4":
            delete_transaction(transactions)
        elif choice == "5":
            edit_transaction(transactions)
        elif choice == "6":
            show_monthly_summary(transactions)
        elif choice == "7":
            show_category_summary(transactions)
        elif choice == "8":
            show_category_chart(transactions)
        elif choice == "9":
            show_top_categories(transactions)
        elif choice == "10":
            print("ออกจากโปรแกรม")
            break
        else:
            print("กรุณาเลือกเมนู 1-10")


main()
