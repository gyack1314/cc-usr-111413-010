"""当前来源连接，不拟合迁移效果。"""
import json
from common import read
from selection import joined,categorical_support
from trial import descriptive
from population import margins
def prepare_sources():
    data=read()
    return {"population_margins":margins(data),"trial_descriptive":descriptive(data),"joined":joined(data),"category_support":categorical_support(data)}
if __name__=="__main__":print(json.dumps(prepare_sources(),ensure_ascii=False,indent=2))
