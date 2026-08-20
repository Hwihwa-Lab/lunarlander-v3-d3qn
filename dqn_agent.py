"""
DQN Agent Implementation for LunarLander
Supports Dueling Q-Network, Double DQN, and Stylish Landing Reward Shaping.
"""

import os
import random
from collections import deque, namedtuple
from typing import Tuple, List, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Experience tuple
Experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])

# Device configuration (GPU if available, otherwise CPU)
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class DuelingQNetwork(nn.Module):
    """
    Dueling Q-Network architecture:
    Separates state-value V(s) and advantage A(s, a) streams.
    Q(s, a) = V(s) + (A(s, a) - mean(A(s, :)))
    """
    def __init__(self, state_size: int = 8, action_size: int = 4, seed: int = 42, hidden_size: int = 128):
        super(DuelingQNetwork, self).__init__()
        torch.manual_seed(seed)

        # Feature extractor layers
        self.feature_network = nn.Sequential(
            nn.Linear(state_size, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.ReLU(),
        )

        # Value stream: V(s)
        self.value_stream = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

        # Advantage stream: A(s, a)
        self.advantage_stream = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )

    def forward(self, state: torch.Tensor) -> torch.Tensor:
        features = self.feature_network(state)
        values = self.value_stream(features)
        advantages = self.advantage_stream(features)
        # Combine streams with zero-mean advantage constraint
        q_values = values + (advantages - advantages.mean(dim=-1, keepdim=True))
        return q_values


class ReplayBuffer:
    """Fixed-size experience replay buffer."""
    def __init__(self, action_size: int, buffer_size: int = int(1e5), batch_size: int = 64, seed: int = 42):
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size
        random.seed(seed)

    def add(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        e = Experience(state, action, reward, next_state, done)
        self.memory.append(e)

    def sample(self) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(DEVICE)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(DEVICE)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(DEVICE)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(DEVICE)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(DEVICE)

        return (states, actions, rewards, next_states, dones)

    def __len__(self) -> int:
        return len(self.memory)


class DQNAgent:
    """Interacts with and learns from the environment using Dueling Double DQN."""

    def __init__(
        self,
        state_size: int = 8,
        action_size: int = 4,
        seed: int = 42,
        buffer_size: int = int(1e5),
        batch_size: int = 64,
        gamma: float = 0.99,
        tau: float = 1e-3,
        lr: float = 5e-4,
        update_every: int = 4,
        double_dqn: bool = True,
    ):
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)
        self.gamma = gamma
        self.tau = tau
        self.update_every = update_every
        self.batch_size = batch_size
        self.double_dqn = double_dqn

        # Q-Networks (Local & Target)
        self.qnetwork_local = DuelingQNetwork(state_size, action_size, seed).to(DEVICE)
        self.qnetwork_target = DuelingQNetwork(state_size, action_size, seed).to(DEVICE)
        self.optimizer = optim.AdamW(self.qnetwork_local.parameters(), lr=lr, weight_decay=1e-4)

        # Replay Memory
        self.memory = ReplayBuffer(action_size, buffer_size, batch_size, seed)
        self.t_step = 0
        self.last_loss = 0.0

        # Hard copy weights to target initially
        self.hard_update(self.qnetwork_local, self.qnetwork_target)

    def step(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool):
        # Save experience in replay memory
        self.memory.add(state, action, reward, next_state, done)

        # Learn every UPDATE_EVERY time steps
        self.t_step = (self.t_step + 1) % self.update_every
        if self.t_step == 0 and len(self.memory) >= self.batch_size:
            experiences = self.memory.sample()
            self.learn(experiences)

    def act(self, state: np.ndarray, eps: float = 0.0) -> Tuple[int, List[float]]:
        """Returns chosen action and computed Q-values for the state."""
        state_tensor = torch.from_numpy(state).float().unsqueeze(0).to(DEVICE)
        self.qnetwork_local.eval()
        with torch.no_grad():
            q_values_tensor = self.qnetwork_local(state_tensor)
        self.qnetwork_local.train()

        q_values = q_values_tensor.cpu().data.numpy()[0].tolist()

        # Epsilon-greedy action selection
        if random.random() > eps:
            action = int(np.argmax(q_values))
        else:
            action = random.choice(range(self.action_size))

        return action, q_values

    def learn(self, experiences: Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]):
        """Updates value parameters using given batch of experience tuples."""
        states, actions, rewards, next_states, dones = experiences

        if self.double_dqn:
            # Double DQN: local network chooses best action, target network evaluates Q-value
            best_actions = self.qnetwork_local(next_states).detach().argmax(dim=1, keepdim=True)
            q_targets_next = self.qnetwork_target(next_states).gather(1, best_actions)
        else:
            # Standard DQN
            q_targets_next = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1)

        # Compute Q targets for current states: R + gamma * Q_target(s', a*) * (1 - done)
        q_targets = rewards + (self.gamma * q_targets_next * (1 - dones))

        # Get expected Q values from local model
        q_expected = self.qnetwork_local(states).gather(1, actions)

        # Compute loss (Smooth L1 / Huber Loss for stability)
        loss = F.smooth_l1_loss(q_expected, q_targets)

        # Minimize loss
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping to prevent gradient explosion
        torch.nn.utils.clip_grad_norm_(self.qnetwork_local.parameters(), max_norm=1.0)
        self.optimizer.step()

        self.last_loss = float(loss.item())

        # Soft update target network: theta_target = tau * theta_local + (1 - tau) * theta_target
        self.soft_update(self.qnetwork_local, self.qnetwork_target, self.tau)

    def soft_update(self, local_model: nn.Module, target_model: nn.Module, tau: float):
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau * local_param.data + (1.0 - tau) * target_param.data)

    def hard_update(self, local_model: nn.Module, target_model: nn.Module):
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(local_param.data)

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        torch.save({
            'qnetwork_state_dict': self.qnetwork_local.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, filepath)

    def load(self, filepath: str) -> bool:
        if os.path.exists(filepath):
            checkpoint = torch.load(filepath, map_location=DEVICE)
            self.qnetwork_local.load_state_dict(checkpoint['qnetwork_state_dict'])
            self.hard_update(self.qnetwork_local, self.qnetwork_target)
            return True
        return False


def shape_stylish_reward(state: np.ndarray, original_reward: float, action: int, terminated: bool, truncated: bool) -> float:
    """
    Reward Shaping to encourage a 'Stylish', graceful, perfectly centered and balanced landing.
    State representation in LunarLander:
    state[0]: x position (-1 to 1, 0 is center)
    state[1]: y position (0 is ground level)
    state[2]: x velocity
    state[3]: y velocity
    state[4]: angle (tilt in radians, 0 is vertical)
    state[5]: angular velocity
    state[6]: left leg contact (1.0 or 0.0)
    state[7]: right leg contact (1.0 or 0.0)
    """
    x, y, vx, vy, angle, angular_vel, left_leg, right_leg = state

    bonus = 0.0

    # 1. Upright posture reward: reward for keeping upright (|angle| close to 0)
    if abs(angle) < 0.08:
        bonus += 0.2
    elif abs(angle) > 0.35:
        bonus -= 0.5 * abs(angle)

    # 2. Angular stability reward: discourage rapid spinning
    if abs(angular_vel) < 0.1:
        bonus += 0.1
    elif abs(angular_vel) > 0.5:
        bonus -= 0.3 * abs(angular_vel)

    # 3. Soft descent near ground: when altitude is low, reward gentle downward speed
    if y < 0.3:
        if -0.3 <= vy <= 0.0:
            bonus += 0.4  # smooth soft touchdown speed
        elif vy < -0.6:
            bonus -= 0.8 * abs(vy)  # too fast landing penalty

        # Center alignment bonus near landing pad
        if abs(x) < 0.1:
            bonus += 0.3

    # 4. Perfect Touchdown & Legs bonus
    if left_leg > 0.5 and right_leg > 0.5:
        if abs(angle) < 0.05 and abs(x) < 0.1:
            bonus += 5.0  # Perfect two-legged stylish touchdown

    # 5. Penalize excessive engine thrashing when stable
    if abs(angle) < 0.05 and abs(x) < 0.05 and action in [1, 3]:
        bonus -= 0.05

    return original_reward + bonus
