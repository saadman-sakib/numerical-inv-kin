import sympy as sp

l1, l2 = 1, 1

def inv_kin(x1f, x2f, theta1f, theta2f):
    e1, e2, theta1, theta2= sp.symbols('e1 e2 theta1 theta2')
    theta1f = sp.rad(theta1f+0.1)
    theta2f = sp.rad(theta2f+0.2)

    eq1 = sp.Eq(e1, l1 * sp.cos(theta1) + l2 * sp.cos(theta1 + theta2) - x1f)
    eq2 = sp.Eq(e2, l1 * sp.sin(theta1) + l2 * sp.sin(theta1 + theta2) - x2f)
    J = sp.Matrix([eq1.rhs, eq2.rhs]).jacobian([theta1, theta2])
    
    print('Jacobian:', J)
    for i in range(20):
        Jval = J.subs({theta1: theta1f, theta2: theta2f})
        Jinv = Jval.inv().evalf()
        e1f = eq1.rhs.subs({theta1: theta1f, theta2: theta2f}).evalf()
        e2f = eq2.rhs.subs({theta1: theta1f, theta2: theta2f}).evalf()
        e = sp.Matrix([e1f, e2f]).evalf()
        delta = Jinv * e
        delta = delta.evalf()
        theta1f = theta1f - delta[0]
        theta2f = theta2f - delta[1]
        theta1f = theta1f.evalf()
        theta2f = theta2f.evalf()
        
    theta1f = sp.deg(theta1f).evalf()
    theta2f = sp.deg(theta2f).evalf()
    return [theta1f, theta2f]