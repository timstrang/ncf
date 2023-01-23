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
    return L_fn(x, xdot).sum()

def minimize_action(path, steps, step_size, L_fn, dt, opt='sgd', print_every=15):
    t = np.linspace(0, len(path.x)-1, len(path.x)) * dt
    optimizer = torch.optim.SGD(path.parameters(), lr=step_size, momentum=0) if opt=='sgd' else \
                torch.optim.Adam(path.parameters(), lr=step_size)
    xs = [path.x.clone().data]
    t0 = time.time()
    for i in range(steps):
        S = action(path.x, L_fn, dt)
        S.backward() ; path.x.grad.data[[0,-1]] *= 0
        optimizer.step() ; path.zero_grad()

        if i % (steps//print_every) == 0:
            xs.append(path.x.clone().data)
            print('step={:04d}, S={:.3e} J*s, dt={:.1f}s'.format(i, S.item(), time.time()-t0))
            t0 = time.time()
    return t, path, xs

class PerturbedPath(torch.nn.Module):
    def __init__(self, x_true, N, sigma=0, shift=False, zero_basepath=False, coords=2, is_ephemeris=False):
        super(PerturbedPath, self).__init__()
        np.random.seed(0)
        self.x_true = x_true
        x_noise = sigma*np.random.randn(*x_true.shape).clip(-1,1)
        x_noise[:1] = x_noise[-1:] = 0
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
    args = get_args()
    logging_loop(args)
