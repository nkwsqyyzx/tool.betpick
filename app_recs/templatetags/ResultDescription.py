#!/usr/bin/env python
#coding:utf-8

from django import template
register = template.Library()

@register.filter(name='ResultDescription')
def ResultDescription(value):
    dc = ['等待', "输盘", "输半", "走水", "赢半", "赢盘"]
    return dc[value]
