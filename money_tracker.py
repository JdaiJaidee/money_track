# โปรแกรมบันทึกรายรับ-รายจ่ายส่วนตัว
# เก็บข้อมูลไว้ใน list


def show_menu():
    print("\n===== โปรแกรมบันทึกรายรับ-รายจ่าย =====")
    print("1. เพิ่มรายการ")
    print("2. แสดงรายการทั้งหมด")
    print("3. สรุปยอดเงิน")
    print("4. ลบรายการ")
    print("5. แก้ไขรายการ")
    print("6. ออกจากโปรแกรม")


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

        month = int(month_text)
        day = int(day_text)

        if month < 1 or month > 12:
            print("เดือนต้องอยู่ระหว่าง 1-12")
            continue

        if day < 1 or day > 31:
            print("วันต้องอยู่ระหว่าง 1-31")
            continue

        return date


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
    # ถ้าพิมพ์จำนวนเงินไม่ใช่ตัวเลข หรือใส่ค่าไม่เกิน 0 จะได้ None กลับไป
    amount_text = input("จำนวนเงิน: ")

    if amount_text.replace(".", "", 1).isdigit() == False:
        print("จำนวนเงินต้องเป็นตัวเลขเท่านั้น")
        return None

    amount = float(amount_text)

    if amount <= 0:
        print("จำนวนเงินต้องมากกว่า 0")
        return None

    return amount


def print_transaction_list(transactions):
    for i, transaction in enumerate(transactions, 1):
        print(
            i,
            transaction["date"],
            transaction["detail"],
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


def add_transaction(transactions):
    print("\n--- เพิ่มรายการ ---")

    date = ask_date()
    detail = input("รายละเอียด: ")

    transaction_type = ask_type()
    if transaction_type is None:
        print("เลือกประเภทไม่ถูกต้อง")
        return

    amount = ask_amount()
    if amount is None:
        return

    transaction = {
        "date": date,
        "detail": detail,
        "type": transaction_type,
        "amount": amount
    }

    transactions.append(transaction)
    print("บันทึกรายการเรียบร้อยแล้ว")


def show_all_transactions(transactions):
    print("\n--- รายการทั้งหมด ---")

    if len(transactions) == 0:
        print("ยังไม่มีรายการ")
        return

    print(f"{'ลำดับ':<6}{'วันที่':<14}{'รายการ':<16}{'ประเภท':<10}{'จำนวนเงิน':>12}")
    print("-" * 58)

    for i, transaction in enumerate(transactions, 1):
        print(f"{i:<6}{transaction['date']:<14}{transaction['detail']:<16}{transaction['type']:<10}{transaction['amount']:>10.2f} บาท")

    income, expense, balance = calculate_summary(transactions)

    print("-" * 58)
    print("รายรับรวม :", income, "บาท")
    print("รายจ่ายรวม:", expense, "บาท")
    print("คงเหลือ   :", balance, "บาท")


def show_summary(transactions):
    income, expense, balance = calculate_summary(transactions)

    print("\n--- สรุปยอดเงิน ---")
    print("รายรับทั้งหมด :", income, "บาท")
    print("รายจ่ายทั้งหมด:", expense, "บาท")
    print("เงินคงเหลือ   :", balance, "บาท")


def ask_valid_index(transactions, question):
    # หมายเลขต้องเป็นตัวเลขและต้องอยู่ในรายการจริง ไม่งั้น list จะ error
    index_text = input(question)

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

    print_transaction_list(transactions)
    index = ask_valid_index(transactions, "ลบรายการที่ (ใส่หมายเลข): ")
    if index is None:
        return

    transactions.pop(index)
    print("ลบรายการเรียบร้อยแล้ว")


def edit_transaction(transactions):
    print("\n--- แก้ไขรายการ ---")

    if len(transactions) == 0:
        print("ยังไม่มีรายการ")
        return

    print_transaction_list(transactions)
    index = ask_valid_index(transactions, "แก้ไขรายการที่ (ใส่หมายเลข): ")
    if index is None:
        return

    print("กรอกข้อมูลใหม่แทนของเดิม")

    new_date = ask_date()
    new_detail = input("รายละเอียด: ")

    new_type = ask_type()
    if new_type is None:
        print("เลือกประเภทไม่ถูกต้อง ยกเลิกการแก้ไข")
        return

    new_amount = ask_amount()
    if new_amount is None:
        return

    transactions[index] = {
        "date": new_date,
        "detail": new_detail,
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
            print("ออกจากโปรแกรม")
            break
        else:
            print("กรุณาเลือกเมนู 1-6")


main()
