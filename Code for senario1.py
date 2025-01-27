import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from tqdm import tqdm

# Dummy file_tools module for testing
class file_tools:
    @staticmethod
    def get_dataset(dataset_id, fs):
        # Dummy dataset for testing
        num_samples = 100
        dfs = [np.random.rand(num_samples, 2) for _ in range(3)]  # 3 robots
        landmark_gt = np.random.rand(10, 2)  # 10 landmarks
        return dfs, landmark_gt

# Dummy Robot class for testing
class robot:
    class Robot:
        def __init__(self, df, fs, landmark_gt, gt_initialization, my_idx):
            self.df = df
            self.fs = fs
            self.landmark_gt = landmark_gt
            self.gt_initialization = gt_initialization
            self.my_idx = my_idx
            self.tot_time = len(df)  # total time based on the data length

        def next(self):
            # Simulate the robot's next step (this is just a placeholder)
            pass

# Dummy SceneAnimation class for testing
class SceneAnimation:
    def __init__(self, robots, landmark_gt, title="", plot_est_pos=False, plot_est_landmarks=False, plot_measurements=False, run_time=None, undersample=20, speedup=20, fs=10):
        self.robots = robots
        self.landmark_gt = landmark_gt
        self.title = title

    def write(self, filename):
        print(f"Writing animation to {filename}")
        # Add your animation saving logic here

# Parameters
fs = 10  # Frame rate
dfs, landmark_gt = file_tools.get_dataset(1, fs=fs)

# All Robots #########################################################
robots = [robot.Robot(df,    
                      fs=fs, landmark_gt=landmark_gt,
                      gt_initialization=False,
                      my_idx=i+1)
          for i, df in enumerate(dfs)]

for t in tqdm(range(robots[0].tot_time - 1)):
    for r in robots:
        r.next()

s = SceneAnimation(robots, landmark_gt, title="Scenario 1, Dataset 1, 10Hz",
                   plot_est_pos=True, plot_est_landmarks=True,
                   plot_measurements=True, run_time=None,
                   undersample=20, speedup=20, fs=fs)

s.write("../output/scenario_1_all_robots.mp4")

# All Robots, Gt initialization #####################################
robots = [robot.Robot(df,
                      fs=fs, landmark_gt=landmark_gt,
                      gt_initialization=True,
                      my_idx=i+1)
          for i, df in enumerate(dfs)]

for t in tqdm(range(robots[0].tot_time - 1)):
    for r in robots:
        r.next()

s = SceneAnimation(robots, landmark_gt, title="Scenario 1, Dataset 1, 10Hz",
                   plot_est_pos=True, plot_est_landmarks=True,
                   plot_measurements=True, run_time=None,
                   undersample=20, speedup=20, fs=fs)

s.write("../output/scenario_1_all_robots_gt.mp4")

# Robot 2 ###########################################################
robots = [robot.Robot(dfs[1], fs=fs,
                      landmark_gt=landmark_gt,
                      gt_initialization=False, my_idx=2)]

for t in tqdm(range(robots[0].tot_time - 1)):
    for r in robots:
        r.next()

s = SceneAnimation(robots, landmark_gt, title="Scenario 1, Dataset 1, 10Hz",
                   plot_est_pos=True, plot_est_landmarks=True,
                   plot_measurements=True, run_time=None,
                   undersample=20, speedup=20, fs=fs)
s.write("../output/scenario_1_robot_2.mp4")

# Generate example data for the robot and landmarks
robot_position = np.array([1, 0])  # Robot position (x, y)
landmarks = np.array([[1, 1], [2, 3], [3, 1], [0, -2], [2, -1], 
                      [5, 4], [0, 4], [1, -4], [4, -3], [3, 3]])
landmark_ids = range(1, len(landmarks) + 1)
robot_path = np.array([[1, 0], [1.5, 1.5], [2, 3]])

# Create plot
fig, ax = plt.subplots(figsize=(6, 8))
ax.set_title("Scenario 1, Dataset 1, 10Hz\n2.00/1484.50 s")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_xlim(-1, 6)
ax.set_ylim(-5, 5)

# Plot landmarks with ids
for idx, landmark in zip(landmark_ids, landmarks):
    ax.plot(landmark[0], landmark[1], 'ko')  # Black dots for landmarks
    ax.text(landmark[0] + 0.1, landmark[1] + 0.1, f'{idx}', color='black', fontsize=9)

# Plot robot's path
ax.plot(robot_path[:, 0], robot_path[:, 1], 'o-', color='orange', label="Robot 2")
ax.plot(robot_position[0], robot_position[1], 'ro', markersize=8)  # Current robot position

# Draw error ellipses (example ellipses)
for i, position in enumerate(robot_path):
    ellipse = Ellipse(xy=position, width=1.5, height=0.8, angle=30,
                      edgecolor='orange', facecolor='orange', alpha=0.2)
    ax.add_patch(ellipse)

# Add a legend
ax.legend(loc="upper left")

# Show plot
plt.show()
