import numpy as np
from numpy import polynomial as Pol

# Calculation of L,U and P matrices
def lu(A):
    n = len(A)
    U = np.copy(A)
    L = np.eye(n)
    P = np.eye(n)  
    
    for k in range(n - 1): 
        P_0 = np.eye(n)
        U_0 = np.eye(n)
        L_0 = np.eye(n)      
        max_elem = U[k][k].copy()
        i_max = k
        
        # Calculation of the max element in a column
        for i in range (k + 1, n):
            if abs(max_elem) < abs(U[i][k]):
                max_elem = U[i][k].copy()
                i_max = i
                
        # Permutation of strings in P matrix
        P_0[i_max], P_0[k] = P_0[k].copy(), P_0[i_max].copy() 
        
        # Permutation of the U matrix
        U = P_0.dot(U) 
        
        # Calculation of common factor 
        for i in range(k + 1, n): 
            c = U[i][k] / U[k][k]
            U_0[i][k] = -c
            L_0[i][k] = c
            
        # Zeroing the leading elements in rows
        U = U_0.dot(U) 
        
        # Permutation in the final matrix P
        P = P_0.dot(P)
        L = L.dot(P_0.dot(L_0))
        
    # Calculation the final L matrix    
    L = P.dot(L)    
    return L, U, P


# Solving a system of linear algebraic equations Ax=b
def solve(L, U, P, b): 
    n = len(L)
    x = np.zeros(n)
    
    # Variable for direct substitution y=Ux
    y = np.zeros(n)
    
    P = b.dot(P)
    
    # Direct substitution
    for i in range(n): 
        s = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (P[0][i]-s)/L[i][i]
        
    # Reverse substitution
    for i in reversed(range(n)): 
        s = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - s) / U[i][i]
    return x

# Calculation of 360 points with a step of 1 degree
def get_all_points (x):
    n = 360
    values = np.zeros(360)
    
    # Polinomial with certain coefficients
    p1 = Pol.Polynomial(x) 
    
    # Calculation of values of polinomial in 360 points
    for i in range(n): 
        values[i] = p1(i) 
    return values

# Marix A with angles of detectors          
# A = np.array([(1,2,3),(-1,2,6),(1,-2,3)])
# print (A)

# Matrix b with measured values
# b = np.array([(1,2,3)])
# print (b)

# L,U,P = lu(A)

# x = solve(L,U,P,b)

# print(x)
# values = get_all_points(x)
# print(values)