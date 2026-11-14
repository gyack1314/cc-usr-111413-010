"""来源读取、修订与发布摘要。"""
from pathlib import Path
from decimal import Decimal,InvalidOperation
from copy import deepcopy
import json,hashlib

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def number(value):
    if isinstance(value,bool):raise ValueError('布尔值不是计量')
    try:x=float(value)
    except (ValueError,TypeError):raise ValueError('计量非法')
    import math
    if not math.isfinite(x):raise ValueError('非有限计量')
    return x

def money(value):
    if isinstance(value,(float,bool)):raise ValueError('金额须用十进制字符串或整数')
    try:x=Decimal(value)
    except (InvalidOperation,TypeError):raise ValueError('金额非法')
    if not x.is_finite():raise ValueError('金额非有限')
    return x

def read(path='data/source.json'):return json.loads(Path(path).read_text(encoding='utf-8'))

def latest(rows,key,asof):
    versions={}
    for row in rows:
        if row['known']>asof:continue
        rev=row.get('revision',1)
        if type(rev) is not int or rev<1:raise ValueError('修订号非法')
        k=(row[key],rev)
        if k in versions and versions[k]!=row:raise ValueError('来源修订冲突')
        versions[k]=deepcopy(row)
    selected={}
    for (ident,rev),r in versions.items():
        if ident not in selected or rev>selected[ident].get('revision',1):selected[ident]=r
    return [selected[k] for k in sorted(selected)]

def release(folder,payload):
    path=Path(folder);path.mkdir(parents=True,exist_ok=True);key=digest(payload);target=path/(key+'.json')
    if target.exists():
        if digest(json.loads(target.read_text(encoding='utf-8')))!=key:raise ValueError('发布版本损坏')
        return key
    with target.open('x',encoding='utf-8') as f:json.dump(payload,f,ensure_ascii=False,allow_nan=False)
    return key
