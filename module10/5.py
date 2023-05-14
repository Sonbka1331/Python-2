def find_insert_position(arr, x):
    if not arr:
        return 0
    for i, num in enumerate(arr):
        if num > x:
            return i
    return len(arr)


a = [1, 2, 3, 3, 3, 5]
x = 4

assert find_insert_position(a, x) == 5
