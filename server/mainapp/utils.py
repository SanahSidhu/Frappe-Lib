import sqlite3 as s
from datetime import date

from mainapp.models import (
    book_available, 
    update_return,
    generate_uid,
    update_issue,
    mem_exists,
    check_debt,
    update_mem,
    new_mem 
)


def issue_book(path: str, isbn: str, mem_email: str, fee: int) -> bool:
    """
    Issues book to a member

    Args:
        path: path to database
        isbn: isbn code of book
        mem_email: member email id
        fee: rent fee of book

    Returns:
        bool: True if book issue successful
    """
    if mem_exists(path, mem_email):
        if book_available(path,isbn):
            if check_debt( path, mem_email) == False:

                cur_date = date.today().strftime("%d-%m-%Y")
                bdata = (isbn,cur_date, fee, mem_email)

                update_mem(path, isbn, mem_email, fee)
                update_issue(path, bdata)

                return True
            else:
                return False
        else:
            return False
    else:
        if book_available(path, isbn):
            uid = generate_uid(path)
            cur_date = date.today().strftime("%d-%m-%Y")

            mdata = (uid, mem_email, fee, isbn)
            bdata = (isbn, cur_date, fee, mem_email)

            new_mem(path, mdata)
            update_issue(path, bdata)

            return True


def return_book( path: str, isbn: str, mem_email: str, fee: int) -> bool:
    """
    Returns book from a member
    Args:
        path: path to database
        isbn: isbn code of book
        mem_email: member email id
        fee: rent fee of book
    Returns:
        bool: True if return successful
    """
    if mem_exists(path, mem_email):
        fres = update_return( path, isbn, mem_email, fee)
        return fres
    else:
        return False
