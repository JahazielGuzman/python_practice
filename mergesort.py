def mergesort(a,p,r):
    if p < r:
        q = int((p+r)/2)
        mergesort(a,p,q)
        mergesort(a,q+1,r)
        merge(a,p,q,r)

def merge(a,p,q,r):
    n1 = q - p + 1
    n2 = r - q
    
    L = []
    R = []
    
    for i in range(0,n1):
        L.append(a[p+i])
    
    for j in range(0,n2):
        R.append(a[q+j+1])
    i = 0
    j = 0
    k = p
    while k <= r and i < n1 and j < n2:
        if L[i] <= R[j]:
            a[k] = L[i]
            i += 1
        else:
            a[k] = R[j]
            j += 1
        k += 1
    
    if (i < n1):
        for x in range(i,n1):
            a[k] = L[x]
            k += 1
    else:
        for x in range (j,n2):
            a[k] = R[x]
            k += 1

list = [2,1,4,6,5,12,7,2,0]
mergesort(list,0,len(list)-1)
print list
