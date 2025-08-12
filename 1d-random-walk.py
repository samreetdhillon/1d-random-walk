import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ===== USER INPUT =====
n_steps = int(input("Enter number of steps: "))
p_up = float(input("Enter probability of moving UP (0 to 1): "))
p_down = 1 - p_up

# Input validation for number of walkers
while True:
    try:
        n_walkers = int(input("Enter number of walkers (positive integer): "))
        if n_walkers > 0:
            break
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter a positive integer.")

# ===== STEP GENERATION =====
# ±1 now means UP/DOWN
steps = np.random.choice([1, -1], size=(n_walkers, n_steps), p=[p_up, p_down])
positions = np.zeros((n_walkers, n_steps + 1))
positions[:, 1:] = np.cumsum(steps, axis=1)

# ===== FIGURE SETUP =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: trajectories
lines = []
# Show up to 10 random walkers for clarity
import random
walker_indices = random.sample(range(n_walkers), min(10, n_walkers))
for i in walker_indices:
    line, = ax1.plot([], [], lw=1)
    lines.append(line)

ax1.set_xlim(0, n_steps)
ax1.set_ylim(-n_steps//2, n_steps//2)
ax1.set_title("1D Random Walk (Up/Down)")
ax1.set_xlabel("Step")
ax1.set_ylabel("Vertical Position")

# Right plot: MSD
msd_line, = ax2.plot([], [], label="Monte Carlo MSD")
theoretical_line, = ax2.plot([], [], 'r--', label="Theoretical MSD (∝ t)")
ax2.set_xlim(0, n_steps)
ax2.set_ylim(0, n_steps)
ax2.set_title("Mean Squared Displacement")
ax2.set_xlabel("Step")
ax2.set_ylabel("MSD")
ax2.legend()

# ===== ANIMATION UPDATE =====
def update(frame):
    # Update sample trajectories
    for i, line in enumerate(lines):
        line.set_data(range(frame+1), positions[i, :frame+1])

    # MSD calculation
    msd = np.mean(positions[:, :frame+1]**2, axis=0)
    msd_line.set_data(range(frame+1), msd)
    theoretical_line.set_data(range(frame+1), np.arange(frame+1) * (p_up + p_down - (p_up - p_down)**2))

    # Compute diffusion coefficient at final frame
    if frame == n_steps:
        D_measured = msd[-1] / (2 * n_steps)
        print(f"\nMeasured Diffusion Coefficient D ≈ {D_measured:.3f}")
        print(f"Theoretical Diffusion Coefficient D = {(1 - (p_up - p_down)**2) / 2:.3f}")

    return lines + [msd_line, theoretical_line]

# Animate
ani = animation.FuncAnimation(fig, update, frames=n_steps+1, interval=50, blit=True, repeat=False)
plt.tight_layout()
plt.show()
plt.close('all')

# Show histogram of final displacements
final_displacements = positions[:, -1]
plt.figure(figsize=(8, 5))
plt.hist(final_displacements, bins=30, edgecolor='black')
plt.title('Histogram of Final Displacements')
plt.xlabel('Displacement')
plt.ylabel('Number of Walkers')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
