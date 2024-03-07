import sympy as sp
import numpy as np

l1, l2, l3 = 1, 1, 1

def inv_kin(x1f, x2f, theta1f, theta2f, theta3f):
    e1, e2, theta1, theta2, theta3= sp.symbols('e1 e2 theta1 theta2 theta3')
    theta1f = sp.rad(theta1f+0.01)
    theta2f = sp.rad(theta2f+0.02)
    theta3f = sp.rad(theta3f+0.015)

    eq1 = sp.Eq(e1, l1 * sp.cos(theta1) + l2 * sp.cos(theta1 + theta2) + l3 * sp.cos(theta1 + theta2 + theta3) - x1f)
    eq2 = sp.Eq(e2, l1 * sp.sin(theta1) + l2 * sp.sin(theta1 + theta2) + l3 * sp.sin(theta1 + theta2 + theta3) - x2f)
    J = sp.Matrix([eq1.rhs, eq2.rhs]).jacobian([theta1, theta2, theta3])
    
    for i in range(20):
        Jval = J.subs({theta1: theta1f, theta2: theta2f, theta3: theta3f}).evalf()
        Jval = sp.matrix2numpy(Jval)
        Jval = np.array(Jval).astype('float64')
        Jinv = np.linalg.pinv(Jval)
        e1f = eq1.rhs.subs({theta1: theta1f, theta2: theta2f, theta3: theta3f}).evalf()
        e2f = eq2.rhs.subs({theta1: theta1f, theta2: theta2f, theta3: theta3f}).evalf()
        e = sp.Matrix([e1f, e2f]).evalf()

        delta = Jinv * e
        delta = delta.evalf()
        theta1f = theta1f - delta[0]
        theta2f = theta2f - delta[1]
        theta3f = theta3f - delta[2]
        theta1f = theta1f.evalf()
        theta2f = theta2f.evalf()
        theta3f = theta3f.evalf()
        
    theta1f = sp.deg(theta1f).evalf()
    theta2f = sp.deg(theta2f).evalf()
    theta3f = sp.deg(theta3f).evalf()
    return [theta1f, theta2f, theta3f]