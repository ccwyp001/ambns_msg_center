# -*- coding: utf-8 -*-

from .base import BaseProApi
import cx_Oracle


class ZIT_MIS_MEDICAL_PKG(BaseProApi):
    PKG_NAME = 'ZIT_MIS_MEDICAL_PKG'

    def get_ambul_outd_info(self, unitid='', datauserid='', begintime='', endtime='',
                            lsh='', userid='', tsqk='', flag='', sfqxpc='', sortfield='',
                            sortorder=''):
        pro_name = 'SP_GET_AMBUL_OUTD_INFO'
        in_args = [unitid, datauserid, begintime, endtime,
                   lsh, userid, tsqk, flag, sfqxpc, sortfield, sortorder]
        out_args = [cx_Oracle.CURSOR]
        return self._call_proc(pro_name,
                               in_args=in_args,
                               out_args=out_args
                               )
