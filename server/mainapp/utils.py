import sqlite3 as s
from datetime import datetime

from mainapp.models import check_debt, generate_uid, mem_exists, new_mem, update_issue, update_mem, update_return, book_available

print("utils_start")

def issue_book(path: str, isbn: str, mem_email: str, fee: int) -> bool:

    if mem_exists(path, mem_email):
        if book_available(path,isbn):
            if check_debt( path, mem_email) == False:
                update_mem(path, isbn, mem_email, fee)

                cur_time = datetime.utcnow()
                bdata = (isbn,cur_time, fee, mem_email)

                update_issue(path, bdata)
                return True
            else:
                return False
        else:
            return False
    else:

        uid = generate_uid(path)
        mdata = (uid, mem_email, fee, isbn)
        new_mem(path, mdata)
        return True


def return_book( path: str, isbn: str, mem_email: str, fee: int) -> bool:

    if mem_exists(path, mem_email):
        fres = update_return( path, isbn, mem_email, fee)
    return fres

print("utils_end")