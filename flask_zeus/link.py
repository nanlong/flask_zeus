# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
"""
link = Link('/a', '/a', 'hehe', method='POST', data=(
    LinkData(name='123', data_type='string'),
    LinkData(name='123', data_type='integer'),
    LinkData(name='123', data_type='float'),
    LinkData(name='123', data_type='array'),
    LinkData(name='123', data_type='object'),
))
"""

class Link(dict):

    def __init__(self, rel, href, name, method='GET', data=None):
        """
        :param rel: (必填) 关系
        :param href: (必填) 资源地址
        :param name: (必填) 名称
        :param method: (可选) 请求方法
        :param data: (可选) 在method为post活着put的时候, 必填, 字段
        :return: dict
        """
        kwargs = dict()

        kwargs['rel'] = rel
        kwargs['href'] = href
        kwargs['name'] = name
        kwargs['method'] = method

        if method in ('POST', 'PUT') \
                and isinstance(data, (list, tuple)) \
                and all(map(lambda x: isinstance(x, LinkData), data)):
            kwargs['data'] = data

        super(Link, self).__init__(**kwargs)


class LinkData(dict):

    DATA_TYPE = {
        'integer': (int,),
        'float': (float,),
        'string': (str, unicode,),
        'boolean': (bool,),
        'array': (list, tuple),
        'object': (dict,),
    }

    def __init__(self, name, data_type, label=None, description=None, default=None, validator=None, options=None, data=None):
        """
        :param name: (必填) 字段名称
        :param data_type: (必填) 字段类型 [integer, float, string, boolean, array, object]
        :param label: (可选) 字段标签
        :param description: (可选) 字段描述
        :param default: (可选) 默认值
        :param validator: (可选) 字段验证 一段正则表达式
        :param options: (可选) 提供字段的选项
        :param data: (可选) 当data_type为object时, 定义object内的字段
        :return: dict
        """
        kwargs = dict()
        kwargs['name'] = name
        kwargs['data_type'] = data_type

        if isinstance(label, (str, unicode)):
            kwargs['label'] = label

        if isinstance(description, (str, unicode)):
            kwargs['description'] = description

        if isinstance(default, self.DATA_TYPE.get(data_type, [])):
            kwargs['default'] = default

        if isinstance(validator, (str, unicode)):
            kwargs['validator'] = validator

        if isinstance(options, (list, tuple)):
            kwargs['options'] = options

        if isinstance(data, (list, tuple)) and all(map(lambda x: isinstance(x, LinkData), data)):
            kwargs['data'] = data

        super(LinkData, self).__init__(**kwargs)
