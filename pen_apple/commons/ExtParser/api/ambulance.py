# -*- coding: utf-8 -*-

from .base import BaseDispatchApi


class DispatchAmbulance(BaseDispatchApi):
    def ambulance_info(self, xzbm=''):
        return self._get(
            'Get_All_CLLB_INFO',
            params={
                'xzbm': xzbm
            }
        )

    def ambulance_info_by_lsh_clid(self, lsh='', clid=''):
        return self._get(
            'GET_CCXX_CLXQ_INFO_BY_LSH_CLID',
            params={
                'lsh': lsh,
                'clid': clid,
            }
        )

    def ambulance_info_by_lsh(self, lsh=''):
        return self._get(
            'GET_AMBUL_OUTD_INFO_BY_LSH',
            params={
                'strlsh': lsh,
            }
        )