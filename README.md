# kukaGrasp_pybullet
HKU 2018-2019 RoboticArmGrasping
By Lance, Paul, Alex

This project is still undergoing and the source codes will be updated for imporvements.

This project aims to train a DCNN to guide the simulated robot arm's grasping movement. Agents will learn while trying in the environment based on PyBullet-gym. Q-learning strategy is used. The platform used for network is Tensorflow Keras.

In this project, vision-based and data-driven approach was realized to enable robot grasping. CNN architecture combined with HER algorithm was used.

A simulation environment based on the Pybullet platform was built for virtual training.

For the real-world implementation, refer to the hardware controller at the following address:
  https://github.com/lycpaul/rr_interface_v2.git
  
To train a new network, either configure the training parameters in "config.py" and then run "train.py"; or run the Learner modules inside /agents directly.
