import sqlite3 as s
import random
import string
from typing import Dict, List


def lib_user(path: str):
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS admin(Id INTEGER PRIMARY KEY,Email varchar(200) UNIQUE, Password TEXT)"

    cur.execute(tbl)
    conn.commit()


def create_member(path: str):
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS member(Mem_id varchar(16) PRIMARY KEY, Email varchar(200) UNIQUE, Debt INTEGER, ISBN varchar(200) UNIQUE)"

    cur.execute(tbl)
    conn.commit()


def create_issue(path: str):
    conn = s.connect(path)
    cur = conn.cursor()

    tbl = "CREATE TABLE IF NOT EXISTS issues(ISBN varchar(30) PRIMARY KEY , Issue_Date TEXT, Fee INTEGER, Mem_Email varchar(200))"

    cur.execute(tbl)
    conn.commit()


def generate_uid(path: str) -> str:
    """Generates a unique user id
    Args:
        None
    Returns:
        str
    """
    conn = s.connect(path)
    cur = conn.cursor()

    uid = "".join(
        random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits
        )
        for _ in range(16)
    )

    chk_uid = f"select Mem_id from member where Mem_id = '{uid}'"
    cur.execute(chk_uid)
    chk_uid_res = cur.fetchall()

    if(len(chk_uid_res)) == 0:
        return uid
    else:
        uid = generate_uid()


def new_mem(path: str, data: tuple):
    conn = s.connect(path)
    cur = conn.cursor()

    add_mem = f"insert into member values{data}"

    cur.execute(add_mem)
    conn.commit()


def mem_exists(path: str, mem_email: str) -> bool:
    #check if member exists
    conn = s.connect(path)
    cur = conn.cursor()

    mem_chk = f"select * from member where Email='{mem_email}'"

    cur.execute(mem_chk)
    mem_chk_res = cur.fetchone()

    if mem_chk_res is None:
        return False
    else:
        return True


def book_available(path: str, isbn: str) -> bool:
    #if book is not already issued to sm1 else
    conn = s.connect(path)
    cur = conn.cursor()

    chk_issue = f"select * from issues where ISBN = '{isbn}'"

    cur.execute(chk_issue)
    chk_issue_res = cur.fetchone()

    if chk_issue_res is None:
        return True
    else:
        return False


def check_debt(path: str, mem_email: str) -> bool:
    #if mem debt < 500
    conn = s.connect(path)
    cur = conn.cursor()

    chk_debt = f"select Debt from member where Email = '{mem_email}'"

    cur.execute(chk_debt)
    chk_debt_res = cur.fetchone()

    if chk_debt_res[0] > 500:
        return True
    else:
        return False


def update_mem(path: str, isbn: str, mem_email: str, fee: int):

    conn = s.connect(path)
    cur = conn.cursor()

    mem_debt = f"update member set Debt = Debt + {fee} where Email = '{mem_email}'"

    get_isbn = f"select ISBN from member where Email = '{mem_email}'"
    cur.execute(get_isbn)
    get_isbn_res = cur.fetchall()

    new_isbn_str = get_isbn_res[0][0] + ',' + isbn
    mem_isbn = f"update member set ISBN = '{new_isbn_str}' where Email = '{mem_email}'"

    cur.execute(mem_debt)
    cur.execute(mem_isbn)
    conn.commit()


def update_issue(path: str, data: tuple):
    conn = s.connect(path)
    cur = conn.cursor()

    issued = f"insert into issues values{data}"

    cur.execute(issued)
    conn.commit()


def update_return(path: str, isbn: str, mem_email: str, fee: int) -> bool:
    conn = s.connect(path)
    cur = conn.cursor()

    chk_isbn = f"select ISBN from member where Email = '{mem_email}'"
    cur.execute(chk_isbn)
    chk_isbn_res = cur.fetchall()

    
    if chk_isbn_res is None:
        return False
    else:
        isbn_li = chk_isbn_res[0][0].split(",")
        for book_isbn in isbn_li:
            if book_isbn == isbn:
                isbn_li.remove(isbn)
                updated_isbn = ','.join(isbn_li)

                mem_return = f"update member set ISBN = '{updated_isbn}' where Email = '{mem_email}'"
                cur.execute(mem_return)

                mem_return = f"update member set Debt = Debt - {fee} where Email = '{mem_email}'"
                cur.execute(mem_return)

                issue_return = f"delete from issues where ISBN = '{isbn}'"
                cur.execute(issue_return)

                conn.commit()
                return True

    return False


def get_email(path: str):
    """Gets all user emails from table
    Args:
        path: Path to database
    """

    conn = s.connect(path)
    cur = conn.cursor()

    get_mail = "select Email from admin"

    cur.execute(get_mail)
    emails = cur.fetchall()

    return emails


def chk_admin_exist(path: str, ad_email: str) -> bool:
    """Checks if user exists in database
    Args:
        path: Path to database
        email: User email id
    Returns:
        bool
    """
    conn = s.connect(path)
    cur = conn.cursor()

    chk_admin = f"select * from admin where Email='{ad_email}'"
    cur.execute(chk_admin)
    res = cur.fetchall()

    if len(res) == 0:
        return False
    else:
        return True


def chk_pass(path: str, ad_email: str, passw: str) -> bool:
    conn = s.connect(path)
    cur = conn.cursor()

    chk_passw = f"select Password from admin where Email='{ad_email}'"
    cur.execute(chk_passw)
    chk_passw_res = cur.fetchall()

    if chk_passw_res[0][0] == passw:
        return True
    else:
        return False


def check_errors(data: Dict[str, List]) -> bool:
    """Utility to check for errors in respones

    Args:
        response (Dict[str]): response from API

    Returns:
        bool: True if errors exist
    """
    if 'error' in data.keys():
        return True

    if len(data['message']) == 0:
        return True

    if len(data['message']) > 1:
        return data['message'][0]

    return
