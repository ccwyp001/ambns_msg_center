# -*- coding: utf-8 -*-

from .base import BaseProApi
import cx_Oracle


class ZIT_MIS_SYS_PKG(BaseProApi):
    PKG_NAME = 'ZIT_MIS_SYS_PKG'

    def check_user_info(self, user_id, password):
        pro_name = 'SP_CHECK_USERINFO'
        in_args = [user_id, password]
        out_args = [cx_Oracle.CURSOR]
        return self._call_proc(pro_name,
                               in_args=in_args,
                               out_args=out_args
                               )
