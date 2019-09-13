from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

def set_initial_state(N=1000, I_0=1, R_0=0, beta=0.01, gamma=0.01, t=np.linspace(0, 200, 200)):
    S_0 = N - I_0 - R_0
    return N, S_0, I_0, R_0, beta, gamma, t

def solve_diffential_equations(y, beta, gamma, t, N):
    S, I, R = y
    dSdt = - beta * S * I / N
    dIdt = beta * S * I/ N - gamma * I 
    dRdt = gamma * I 
    return dSdt, dIdt, dRdt

def main():
    N, S_0, I_0, R_0, beta, gamma, t = set_initial_state()
    y_0 = S_0, I_0, R_0
    result = odeint(solve_diffential_equations, y_0, t, args=(beta, gamma, N))
    S, I, R = result.T 

    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(111, axisbelow=True)
    ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered')
    ax.set_xlabel("time")
    ax.set_ylabel("Users")
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    main()