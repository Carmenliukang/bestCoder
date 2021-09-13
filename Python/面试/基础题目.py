#!/usr/bin/env python
# -*- coding: utf-8 -*-
def test():
    nums = [1, 2, 3]
    b = []

    b.append(nums)

    print(nums, b)
    nums = "1111"

    print(nums, b)


def test_1():
    a = [1, 2, 3]
    b = []

    b.append(a)

    print(a, b)

    a[2] = 4
    print(a, b)


def test_2():
    a = [1, 2, 3]
    b = []

    b.append(a)

    print(a, b)

    a.append(3)
    print(a, b)

test_1()
test_2()
