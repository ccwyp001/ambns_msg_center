# -*- coding: utf-8 -*-


from .base import BaseDispatchApi


class DispatchMember(BaseDispatchApi):
    def on_duty(self, is_on_duty=0, org_id='', xzbm=''):
        return self._get(
            'GET_V_STAFF_ONDUTY',
            params={
                'sfsb': is_on_duty,
                'orgid': org_id,
                'xzbm': xzbm
            }
        )

    def org_info(self, xzbm=''):
        return self._get(
            'Get_All_V_ORG_INFO',
            params={
                'xzbm': xzbm
            }
        )

    def mem_info(self):
        return self._get(
            'Get_V_MEMBER_INFO',
            params={

            }
        )
