"""试点企业的已知随机分配与单位结果。"""
from common import number,digest

def trial(data):
    rows={}
    for r in data['trial']:
        if r['firm'] in rows or r['assigned'] not in (0,1) or not 0<number(r['p_treatment'])<1:raise ValueError('试点分配身份或概率非法')
        if r['saving_kwh'] is not None:number(r['saving_kwh'])
        rows[r['firm']]=r
    return {'rows':rows,'design_digest':digest([{k:r[k] for k in ('firm','block','p_treatment','assigned')} for r in data['trial']])}

def descriptive(data):
    rows=trial(data)['rows'];out={}
    for z in (0,1):
        rs=[r for r in rows.values() if r['assigned']==z and r['saving_kwh'] is not None]
        out[str(z)]={'n':len(rs),'observed_mean':sum(r['saving_kwh'] for r in rs)/len(rs) if rs else None}
    return out
