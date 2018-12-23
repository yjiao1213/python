from pykalman import KalmanFilter
import numpy as np

# kf = KalmanFilter(transition_matrices = [1], observation_matrices = [0.1])
# measurements = np.asarray([1, 0, 3])  # 3 observations
# kf = kf.em(measurements, n_iter=5)
# (filtered_state_means, filtered_state_covariances) = kf.filter(measurements)
# (smoothed_state_means, smoothed_state_covariances) = kf.smooth(measurements)
# print(kf.n_dim_state)
