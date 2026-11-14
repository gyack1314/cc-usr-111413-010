"""入选状态和可观察类别支持；不推断迁移因果效应。"""
from trial import trial
from population import population

def joined(data):
    pop=population(data)['rows'];experiment=trial(data)['rows']
    if set(experiment)-set(pop):raise ValueError('试点企业不在冻结目标框中')
    out=[]
    for ident,r in pop.items():out.append(dict(r,in_trial=ident in experiment,experiment=experiment.get(ident)))
    return out

def categorical_support(data):
    rows=joined(data);observed={(r['industry'],r['size']) for r in rows if r['in_trial']};out=[]
    for r in rows:out.append({'firm':r['firm'],'observed_category_support':(r['industry'],r['size']) in observed})
    return out
