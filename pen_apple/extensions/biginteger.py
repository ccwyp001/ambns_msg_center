from sqlalchemy import BigInteger
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.compiler import compiles


# SQLAlchemy does not map BigInt to Int by default on the sqlite dialect.
# It should, but it doesnt.
class SLBigInteger(BigInteger):
    pass


@compiles(SLBigInteger, 'sqlite')
def bi_c1(element, compiler, **kw):
    return "INTEGER"


@compiles(SLBigInteger)
def bi_c2(element, compiler, **kw):
    return compiler.visit_BIGINT(element, **kw)


class LongText(LONGTEXT):
    pass


@compiles(LongText, 'mysql')
def bi_c3(element, compiler, **kw):
    return compiler.visit_LONGTEXT(element, **kw)


@compiles(LongText)
def bi_c4(element, compiler, **kw):
    return "TEXT"
