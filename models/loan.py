# models/loan.py
from datetime import datetime, timedelta


class Loan:
    def __init__(self, loan_id: int, member_id: str | int, book_id: int, 
                 loan_date: str  = None, due_date: str = None, 
                 return_date: str = None, status: str = "대출중"):
        
        self.loan_id = loan_id
        self.member_id = member_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status
        
    def to_dict(self) -> dict:
        """객체를 JSON 저장을 위한 딕셔너리로 변환"""
        return {
            "loan_id": self.loan_id,
            "member_id": self.member_id,
            "book_id": self.book_id,
            "loan_date": self.loan_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        """JSON 딕셔너리를 Loan 객체로 생성"""
        return cls(
            data["loan_id"],
            data["member_id"],
            data["book_id"],
            data["loan_date"],
            data["due_date"],
            data["return_date"],
            data["status"]
        )