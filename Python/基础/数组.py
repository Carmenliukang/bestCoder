#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 底层存储

# 用于存储相关的数组结构
nums = [3, 2, 3, 7, 8, 1]

total = nums.count(3)
print(total)
# 2

place = nums.index(3)
print(place)
# 0


# 这里是在原数组的基础上直接反转，生成新的列表
nums.reverse()
print(nums)
# [1, 8, 7, 3, 2, 3]

# 原数组上进行修改
nums.sort()
print(nums)
# [1, 2, 3, 3, 7, 8]

nums = [1,2,3,4]
result = list(map(lambda x:x*2,nums))
print(result)

nums = [1,2,3,4]
result =filter(lambda x:x>2,nums)
print(list(result))
# result 是一个可迭代集合