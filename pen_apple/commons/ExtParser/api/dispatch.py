# -*- coding: utf-8 -*-



from .base import BaseDispatchApi
import datetime

class DispatchApi(BaseDispatchApi):
    def ambulance_outed(self, start_time='', end_time='', xzbm=''):
        _ = datetime.date.today()
        if not start_time:
            start_time = _.strftime('%Y-%m-%d %H:%M:%S')
        if not end_time:
            end_time = (_ + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        return self._get(
            'Get_AMBUL_INFO_BY_DATE',
            params={
                'starttime': start_time,
                'endtime': end_time,
                'xzbm': xzbm
            }
        )
