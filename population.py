"""调查前冻结的全市目标企业总体框。"""
from common import number,digest

def population(data):
    out={}
    for r in data['population']:
        if r['firm'] in out or number(r['baseline_energy'])<0 or r['size'] not in ('small','medium','large'):raise ValueError('目标企业框非法')
        out[r['firm']]=r
    if not out:raise ValueError('目标总体为空')
    return {'rows':out,'digest':digest(data['population']),'sampling_error':False}

def margins(data):
    out={}
    for r in population(data)['rows'].values():
        k=(r['industry'],r['size']);out[k]=out.get(k,0)+1
    return [{'industry':i,'size':s,'firms':n} for (i,s),n in sorted(out.items())]
