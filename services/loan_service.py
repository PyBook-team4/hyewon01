# services/loan_service.py
from datetime import datetime, timedelta

from models.loan import Loan
from utils.file_handler import FileHandler

'''
해당 파일 구현 시 members,books,records 부분을 모두 접근해야 하기 때문에 난이도가 높을 수 있습니다.
우선 코드 구현 후 테스트 할 경우 books.json에 더미데이터 한개 생성 후 테스트하면 됩니다.

'''

# 도서 대출

def borrow(member_id: str | int, title: str, author: str) -> bool:
    """도서 대출: 재고 확인 후 대출 기록 생성 및 재고 감소"""
    books = FileHandler.load_json("data/books.json")
    loans = FileHandler.load_json("data/loans.json")

    # 1. 도서 존재 여부 및 대출 가능 재고 확인 (books.json 접근)
    book = None

    for search_book in books:
        if search_book["title"] == title and search_book["author"] == author :
            book = search_book
            break

    if book is None:
        print("해당 도서를 찾을 수 없습니다. ")
        return False

    if book["available_stock"] < 1:
        print("대출 가능한 재고가 없습니다.")
        return False
    
    # 도서 검증 확인 뒤 도서 id 추출
    book_id = book["id"]

    # 2.새로운 loan_id 생성     (loans.json 접근)
    loan_ids = [loan["loan_id"] for loan in loans] # id만 추출

    if loan_ids:  # id가 있다면 최대값에 +1 / 없다면 1을 대출 id로 지정
        new_loan_id = max(loan_ids) + 1
    else:
        new_loan_id = 1
        
    # 3. 새 대출 객체 생성 및 추가  
    loan_datetime = datetime.now()
    loan_date = loan_datetime.strftime("%Y-%m-%d")
    due_date = (loan_datetime + timedelta(days=14)).strftime("%Y-%m-%d")

    loan = Loan(
        new_loan_id,
        member_id,
        book_id,
        loan_date,
        due_date,
        None,
        "대출중"
    )

    loans.append(loan.to_dict())

    # 4. 재고 감소 (available_stock - 1) (books.json 접근)
    book["available_stock"] -= 1

    # 5. json 파일 저장
    FileHandler.save_json("data/books.json", books) 
    FileHandler.save_json("data/loans.json", loans)
    return True
    

#도서 반납

def return_book(loan_id: int) -> bool:
    """도서 반납: 대출 상태 변경, 재고 복구 및 포인트 적립"""
    loans = FileHandler.load_json("data/loans.json")
    books = FileHandler.load_json("data/books.json")
    members = FileHandler.load_json("data/members.json")
    # 1. 대출 상태 및 반납일 업데이트
    loan = None

    # 대출 상태 확인 
    for search_loan in loans:
        if search_loan["loan_id"] == loan_id:
            loan = search_loan
            break

    if loan is None:
        print("대출기록이 없습니다.")
        return False
    
    if loan["status"] != "대출중":
        print("이미 반납했거나 반납할 수 없는 상태입니다.")
        return False

    # 반납일 업데이트 
    today = datetime.now().strftime("%Y-%m-%d")

    loan["return_date"] = today
    loan["status"] = "반납완료"

    # 2. 해당 도서 재고 복구 (available_stock + 1)
    for search_book in books:
        if search_book["id"] == loan["book_id"]:
            search_book["available_stock"] += 1
            break 

    # 3. 반납 보상 포인트 지급 (예: 반납 시 10 포인트 적립)  members.json 접근
    # 대출 시 저장된 아이디를 members에서 비교해서 찾아 적립 
    for search_member in members:
        if search_member["email"] == loan["member_id"]:
            search_member["point"] += 10
            break

    # 5. 파일 저장
    FileHandler.save_json("data/loans.json", loans)
    FileHandler.save_json("data/books.json", books)
    FileHandler.save_json("data/members.json",members) 

    return True
    

    # 4. 리뷰, 평점 남길 시 (예: 10포인트 추가 적립)        records.json 접근

