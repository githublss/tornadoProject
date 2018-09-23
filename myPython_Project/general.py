#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by lss on 2018/9/12
class A(object):
    bar = 1

    def foo(self):
        print 'foo'

    @staticmethod
    def static_foo():
        print 'static_foo'
        print A.bar

    @classmethod
    def class_foo(cls):     #这里用了cls参数，即A这个类本身，后面要使用类.属性或类.方法时就可以用cls.属性或cls.方法，避免硬编码
        print 'class_foo'
        print cls.bar
        cls().foo()     #类.方法的调用，没有使用类的名字(A)，避免硬编码

A.static_foo()
A.class_foo()