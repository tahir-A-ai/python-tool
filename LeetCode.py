# 1. Two Sum
""" Given an array of integers nums and an integer target, 
    return indices of the two numbers such that they add up to target.

    You may assume that each input would have exactly one solution, 
    and you may not use the same element twice.

    You can return the answer in any order.

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
"""

class Solution(object):
    def twoSum(self, nums, target):
        for i in range(len(nums)):
            for j in range (i+1, len(nums)):
                if nums[i]+nums[j] == target:
                    return i,j

nums = [2,7,11,15]
target = 9
sol = Solution()
sol.twoSum(nums, target)

# ======================================================= #

# 2. Palindrome Numbers
""" 
Given an integer x, return true if x is a palindrome, and false otherwise.
Example 1:
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.
"""
class Solution(object):
    def isPalindrome(self, x):
        num_x = str(x)
        if num_x == num_x[::-1]:
            return True
        else:
            return False

x = 121
sol = Solution()
sol.isPalindrome(x)

# ==================================================================

# 3.valid Anagram
"""
Given two strings s and t, return true if t is an anagram of s, and false otherwise.

Example 1:
Input: s = "anagram", t = "nagaram"
Output: true

Example 2:
Input: s = "rat", t = "car"
Output: false 
"""
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s = s.lower()
        t = t.lower()
        if sorted(s) == sorted(t):
            return True
        else:
            return False
s = "anagram"
t = "nagaram"
sol = Solution()
print(sol.isAnagram(s, t))
        
# =============================================================

# 4. Move Zeroes
""" 
Given an integer array nums, move all 0's to the end of it while maintaining the relative order 
of the non-zero elements.
Note that you must do this in-place without making a copy of the array.
Example 1:
Input: nums = [0,1,0,3,12]
Output: [1,3,12,0,0] 
"""
class Solution:
    def moveZeroes(self, nums):
        
        indx = 0
        for i in nums:
            if i != 0:
                nums[indx] = i
                indx += 1
        for i in range(indx, len(nums)):
            nums[i] = 0
        return nums

nums = [0,1,0,3,12]
sol = Solution()
print(sol.moveZeroes(nums))

# =======================================================

# 5. Remove duplicates from sorted Array / List
"""
Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that 
each unique element appears only once. The relative order of the elements should be kept the same.
"""
class Solution:
    def removeDuplicates(self, nums):
        nums[:]=sorted(set(nums))
        return nums

nums = [3,5,4,3,1,5,6]
sol = Solution()
print(sol.removeDuplicates(nums))