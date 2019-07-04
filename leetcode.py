



'''
def main(self, nums: List[int]) -> int:
    target = list(range(1, len(nums)+2))
    for i in target:
        if (i <= len(nums)+1) & (i > 0):
            if i not in nums:
                return i

print(main())
'''