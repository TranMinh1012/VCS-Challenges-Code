def binary_search(arr, value, left, right):
    while left <= right:
        middle = (left + right) // 2
        if(arr[middle] == value):
            return middle
        elif(arr[middle] > value):
            right = middle - 1
        else:
            left = middle + 1
    return -1

print("Nhap so luong phan tu: ")
n = int(input())
arr = []
for i in range(n):
    arr.append(int(input()))
print("Nhap phan tu can tim:")
value = int(input())
res = binary_search(arr, value, 0, len(arr)-1)
if res != 1:
    print("Index cua phan tu can tim", str(res))
else:
    print("Khong co phan tu trong mang")