def merge_the_tools(string, k):
    # your code goes here
    while (len(string)>=k):
        elems = string[:k]
        print("".join(sorted(set(elems), key = elems.index)))
        string = string[k:]
  
  
"""
input:
   merge_the_tools('AABCAAADA', 3)
output:
  AB
  CA
  AD
"""
