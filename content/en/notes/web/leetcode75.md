---
title: LeetCode75
category: Web
description: Given an integer array nums, return true if any value appears at least
  twice in the array, and return false if every element is distinct.
tags:
- web
---

<!-- imported from ObsidianVault/webdev/LeetCode75.md. Edit the source, then run sync.py. -->

# LeetCode75

`web`

## Problem #1 - LC217

### Problem Statement

Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

```
Example 1:

Input: nums = [1,2,3,1]
Output: true

Example 2:

Input: nums = [1,2,3,4]
Output: false

Example 3:

Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
```

### My Solution

- Time Complexity: `O(n)`

- Space Complexity: `O(n)`

Code:

```python
def hasDuplicate(nums: list[int]) -> bool:
	seen = set()
	for n in nums:
		if n in seen:
			return True # Duplicate found
		else:
			seen.add(n)
	return False
```

### My Explanation?

Creating a set, which allows for O(1) search, then iterating over the list and checking if each number in the list is already in the set. If it is, return True as that's a duplicate. If not, add it to the set. Return false outside the loop.

## Problem #2 - LC 242

### Problem Statement

Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

```
Example 1:

Input: s = "anagram", t = "nagaram"
Output: true
Example 2:

Input: s = "rat", t = "car"
Output: false
```

### My Solution

- Time Complexity: O(len(s) + len(t))

- Space Complexity: O(len(s) + len(t))

Code:

```python
def isAnagram(s,t):
	if len(s) != len(t): return False
	s_map, t_map = {}, {}
	for i in range(len(s)):
		s_map[s[i]] = s_map.get(s[i],0) +
		t_map[t[i]] = t_map.get(t[i],0) +
	for key in s_map:
		if key noy in t_map or s_map[key] != t_map[key]:
			return False
	return True

```

### My Explanation?

Count each occurance in two maps. iterate through one map's keys and return false if either the key isnt in the other map or the two key values dont match. return true at the end of the loop.

## Problem #3 - LC 1

### Problem Statement

Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.

Example:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

### My Solution

- Time Complexity: O(n)

- Space Complexity: O(n)

Code:

```python
def twoSum(nums: List[int], target: int) -> List[int]:
	num_to_idx = {}
	for i in range(len(nums)):
		if nums[i] in num_to_idx:
			return [num_to_idx[nums[i]], i]
		num_to_idx[target - nums[i]] = i

	return None
```

### My Explanation?

Start out with a map that will contain target's complement and its index. loop through the list, if the current number is in the map, return a list
containing map[curr_num] (the index of the complement of number) and `i` (the current index). Else add the `target - curr_num` to the map with its index.

```
nums = [4,5,6], t = 10
i = 0
t - nums[0] = 6
map[6] = 0
i = 1
t - nums[1] = 5
map[5] = 1
i = 2
t - nums[2] = 4
map[4] = 2

```

## Problem #4 - LC 49

### Problem Statement

Given an array of strings strs, group all anagrams together into sublists. You may return the output in any order.

An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.

```
Example 1:

Input: strs = ["act","pots","tops","cat","stop","hat"]

Output: [["hat"],["act", "cat"],["stop", "pots", "tops"]]
```

### My Solution

- Time Complexity: O(n \* m) - `n = avg. length of word, m = number of words in strs`

- Space Complexity:

Code:

```python
def groupAnagrams(strs: List[str]) -> List[List[str]]:
	# defaultdict -> for when the value doesnt exist, the function passed will be invoked on the value
	res = defaultdict(list)

	for word in strs:
		# A count for each letter
		count = [0] * 26

		for char in word:
			count[ord(char) - ord('a')] += 1
		# lists arent hashable, so tuple them (immutable therefore hashable)
		# for each count add the word for it
		res[tuple(count)].append(word)
	# return the values, we dont care about the keys
	return res.values()
```

### My Explanation?

start with a map: list (letter counts) -> list (words with those letter counts). Loop through each word in strs, initializing a letter count array of 26 (a-z). count each letter occurance.
add the count as a tuple to the initial map (lists arent hashable, so tuple them (immutable therefore hashable)) and append the current word as a value.
because of default dict all elements of the dict are lists. return map's values().

## Problem #5 - LC 347

### Problem Statement

Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.

```
Example:

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

### My Solution

- Time Complexity: O(k \* n)

- Space Complexity: O(n)

Code:

```python
def topKFrequent(nums: list[int], k: int) -> list[int]:
    if len(nums) == 1: return [nums[0]]
    counter = {}
    res = []
	# SC - O(n)
	# TC - O(n)
    for i in range(len(nums)):
        counter[nums[i]] = counter.get(nums[i],0) + 1
	# TC - O(k)
    for _ in range(k):
		# O(k * n)
        max_v = max(counter.values())
        for key in counter:
			# O(n)
            if counter[key] == max_v and key not in res:
                res.append(key)
                counter[key] = -1
                if len(res) == k:
                    return res
```

### My Explanation?

count each occurance in a map. loop k times, each time getting max_value in the map. loop over each map key and see if it's equal
to the current max_v. if equal, add it to result and reset it's value to -1, so as to not show up as a max. stop when res length is equal to k

### Optimal Solution

- Time Complexity: O(n)
- Space Complexity:

Code:

```python
def topKFrequent(nums: list[int], k: int) -> list[int]:
	counter = {}
	freq = [[] for i in range(len(nums) + 1)]
	res = []

    for i in range(len(nums)):
        counter[nums[i]] = counter.get(nums[i],0) + 1

	for num, count in counter.items():
		for f in freq:
			f[count].append(num)

	for i in range(len(freq) - 1, 0, -1):
		for num in freq[i]:
			res.append(num)
			if len(res) == k:
				return res

```

### Solution Explanation

set up frequencies arr with (n+1) empty lists. count each occurance in a map. loop over k,v in counter items, loop for each freq[v] append k.
now start from i = len(nums) - 1, loop for each number in freq[i], append num to res. stop when len(res) == k.

## Problem #6

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #7

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #8

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #9

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #10

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #11

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #12

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #13

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #14

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #15

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #16

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #17

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #18

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #19

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #20

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #21

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #22

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #23

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #24

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #25

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #26

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #27

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #28

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #29

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #30

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #31

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #32

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #33

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #34

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #35

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #36

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #37

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #38

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #39

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #40

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #41

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #42

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #43

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #44

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #45

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #46

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #47

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #48

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #49

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #50

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #51

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #52

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #53

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #54

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #55

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #56

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #57

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #58

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #59

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #60

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #61

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #62

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #63

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #64

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #65

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #66

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #67

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #68

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #69

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #70

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #71

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #72

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #73

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #74

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here

## Problem #75

### Problem Statement

Statement here

### My Solution

- Time Complexity:

- Space Complexity:

Code:

```python
def solution():
	# code
```

### My Explanation?

Explanation Here

### Optimal Solution

- Time Complexity:
- Space Complexity:

Code:

```python
def solution():
	# code
```

### Solution Explanation

Solution here
