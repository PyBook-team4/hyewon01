from services.loan_service import borrow, return_book

# 1. 도서 대출 테스트
borrow_result = borrow("test@naver.com", "점프 투 파이썬","박응용")
print("대출 성공 여부:", borrow_result)

# 2. 반납 테스트
# loans.json에 새로 생성된 대출 기록의 ID를 확인해야 함
return_result = return_book(1)
print("반납 성공 여부:", return_result)
