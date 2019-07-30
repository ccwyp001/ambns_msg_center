# -*- coding: utf-8 -*-

import hashlib
from math import ceil


def md5_code(text):
    md = hashlib.md5()
    md.update(text.encode())
    return md.hexdigest().upper()


def paginate(items, page=None, per_page=None, error_out=True, max_per_page=None):
    """Returns ``per_page`` items from page ``page``.

    If ``page`` or ``per_page`` are ``None``, they will be retrieved from
    the request query. If ``max_per_page`` is specified, ``per_page`` will
    be limited to that value. If there is no request or they aren't in the
    query, they default to 1 and 20 respectively.

    When ``error_out`` is ``True`` (default), the following rules will
    cause a 404 response:

    * No items are found and ``page`` is not 1.
    * ``page`` is less than 1, or ``per_page`` is negative.
    * ``page`` or ``per_page`` are not ints.

    When ``error_out`` is ``False``, ``page`` and ``per_page`` default to
    1 and 20 respectively.

    Returns a :class:`Pagination` object.
    """

    if page is None:
        page = 1

    if not per_page:
        per_page = 10

    if max_per_page is not None:
        per_page = min(per_page, max_per_page)

    if page < 1:
        page = 1

    if per_page < 0:
        per_page = 10

    total = len(items)

    items = items[(page - 1) * per_page:page * per_page]

    if not items and page != 1 and error_out:
        raise

    # No need to count if we're on the first page and there are fewer
    # items than we expected.

    # if page == 1 and len(items) < per_page:
    #     total = len(items)
    # else:
    #     total = self.order_by(None).count()

    return Pagination(page, per_page, total, items)


class Pagination(object):
    """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, page, per_page, total, items):
        #: the unlimited query object that was used to create this
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def prev_num(self):
        """Number of the previous page."""
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        if not self.has_next:
            return None
        return self.page + 1
