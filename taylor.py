import numpy as np
import matplotlib.pyplot as plt

P = 10  # nombre d'itérations
x1, x2, x3, y1, y2, y3 = 1, -1, 0, -1, -1, 1
x0 = int(input('estimation initiale x0: '))
y0 = int(input('estimation initiale y0: '))
X = 0.5  #T
Y = 0.5  #L vrai position de la source
xk = x0  #T
yk = y0  #L position estimée de la source à la k-ième itération
n = 3  # nombre de microphones
x = [x1, x2, x3]  #T
y = [y1, y2, y3]  #L positions respectives des microphones 1, 2 et 3
m = [1, 1, 1]  # ['input(TOA) (range estimation)' for _ in range(n)]  # len(m) = 3 (= len(n))
d, Q, D, e, Xapprox, Yapprox = [[] for _ in range(6)]
A = []

# TOA method 2D
# x=xk+d 2 formules pour trouver d: 
# 1) Ad=D+e
# 2) d=(A^{T}Q^{-1}A)^{-1}A^{T}Q^{-1}D
for _ in range(P):
    for i in range(n):
        r = np.sqrt((xk-x[i])**2 + (yk-y[i])**2) # len(r) = 1 ;  r = fv 
        A.append([[(xk - x[I])/r, (yk - y[I])/r] for I in range(n)])
        D.append(m[i] - r)
        e.append(1)  # vecteur colonne de l'erreur à chaque itération voir Q
    print(len(np.size(A)))
    Ainv = np.linalg.inv(np.array(A))
    d.append(Ainv.dot(D+e))  # c'est ce qu'on cherche ;  len(d) = i

    Q = 1  # ??? covariance matrix, range estimation error ??? voir avec e

    xk += d[0]
    yk += d[1]
    Xapprox.append(xk)
    Yapprox.append(yk)
    # fin de la première itération mettre le tout dans une boucle 

plt.figure()
plt.plot(x0, y0, 'O')
plt.plot(Xapprox, Yapprox, 'o')
plt.plot(x, y, 's')
plt.plot(X, Y, '*')
plt.show()
