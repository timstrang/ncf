# Simulation as Optimization | Tim Strang and Sam Greydanus | 2023 | MIT License

import numpy as np
import torch, time, argparse
from core_physics import *
from utils import *

def get_args():
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--logfile', default='paxg.csv', type=str, help='file where price data is written')
    parser.add_argument('--interval', default=10, type=int, help='logging interval (seconds)')
    parser.add_argument('--verbose', default=False, type=bool, help='print to terminal while running?')
    return parser.parse_args()


############################# MINIMIZING THE ACTION #############################

def action(x, L_fn, dt):
    xdot = (x[1:] - x[:-1]) / dt
    xdot = torch.cat([xdot, xdot[-1:]], axis=0)
    T, V = L_fn(x, xdot)
    return T-V, T, V

def calc_loss(S, T, V, loss_coeffs):
    S_coeff, E_coeff = loss_coeffs
    S_loss = S_coeff*S.sum()
    E = T + V
    E_loss = E_coeff*(torch.square(torch.diff(E, axis=0)).mean())
    return S_loss + E_loss, E_loss

def minimize_action(path, steps, step_size, L_fn, dt, opt='sgd', print_every=15, loss_coeffs=(1,0), unpert_till=0, verbose=True):
    t = np.linspace(0, len(path.x)-1, len(path.x)) * dt
    optimizer = torch.optim.SGD(path.parameters(), lr=step_size, momentum=0) if opt=='sgd' else \
                torch.optim.Adam(path.parameters(), lr=step_size)
    xs = [path.x.clone().data]
    info = {'S' : [], 'T' : [], 'V' : [], 'loss' : [], 'E_loss' : []}
    t0 = time.time()
    for i in range(steps):
        S, T, V = action(path.x, L_fn, dt)
        info['S'].append(S.sum().item()) ; info['T'].append(T.sum().item()) ; info['V'].append(V.sum().item())
        loss, E_loss = calc_loss(S, T, V, loss_coeffs)
        info['loss'].append(loss.item()) ; info['E_loss'].append(E_loss.item())
        loss.backward() ; path.x.grad.data[-1] *= 0 ; path.x.grad.data[:unpert_till+1] *= 0
        optimizer.step() ; path.zero_grad()

        if i % (steps//print_every) == 0:
            xs.append(path.x.clone().data)
            if verbose:
                print('step={:04d}, S={:.3e} J*s, loss={:.3e}, E_loss={:.3e}, dt={:.1f}s'
                      .format(i, S.sum().item(), loss.item(), E_loss.item(), time.time()-t0))
            t0 = time.time()
    return t, path, xs, info

class PerturbedPath(torch.nn.Module):
    def __init__(self, x_true, N, sigma=0, shift=False, zero_basepath=False, coords=2, is_ephemeris=False, unpert_till=0, clip_rng=1):
        super(PerturbedPath, self).__init__()
        np.random.seed(0)
        self.x_true = x_true
        x_noise = sigma*np.random.randn(*x_true.shape).clip(-clip_rng, clip_rng)
        x_noise[:unpert_till+1] = x_noise[-1:] = 0
        if is_ephemeris:
            x_noise[:,0,:] = 0 # don't perturb the Sun
        x_basepath = np.copy(x_true)
        x_basepath[1:-1] = x_basepath[1:-1]*0 if zero_basepath else x_basepath[1:-1]
        self.x_pert = x_pert = (x_basepath + x_noise).reshape(-1, N*coords)
        if shift:
            x_pert_shift = np.concatenate([x_pert[5:-5,2:], x_pert[5:-5,:2]], axis=-1)
            self.x_pert[5:-5] = x_pert[5:-5] = x_pert_shift
            print(self.x_pert.shape)
        self.x = torch.nn.Parameter(torch.tensor(x_pert)) # [time, N*2]


if __name__ == "__main__":
    print('TODO @sam @tim implement this function so all experiments can be reproduced from the command line')