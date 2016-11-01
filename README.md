# Stochastic-Imaging
Producing, Analysing and Aggregating images:

- This repository will follow my final year project, the aim being to beat optical resolution with stochastic imaging
- Initially it will include basic code, subsequent additions will be more complex and complete
- The end result will be a labelled project which will allow someone to set up their own version of the experiment and use the code in this repository to recreate it

Initial Work:
- Create program to simulate blurry images
- Do this by selecting points on pixel map and fitting random Gaussian distributions around them
- Reverse engineer the images to find points of maximum intensity

Experimental Setup:
- Flashing LED array set up x distance from a camera such that the images appear blurry
- Capture multiple images and reduce intensity maxima to single point 
- Aggregate images to form a final, sharp image

Notes:
- The LED array and camera will be controlled using Raspberry Pis
