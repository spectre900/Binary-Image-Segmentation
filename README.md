# Analysis of Max-flow/Min-cut Algorithms for Binary Image Segmentation

## Overview
Max-Flow/ Min-Cut algorithms, an integral part of the greedy algorithmic paradigm, are widely used for solving a large number of significant real-life problems. These algorithms are mainly employed to solve the Max-Flow problem, which deals with finding a feasible flow through a single source and single sink graph, which maximizes the flow rate. However, the time complexity of these algorithms can not be used to judge their practical efficiency to solve a certain problem. So, this paper focuses on finding out the practical efficiency of Max-Flow Algorithms on the basis of Binary Image Segmentation. Image segmentation is the process of classifying each pixel of the source image into two or more categories. Binary image segmentation is a special case of image segmentation in which each pixel is classified as one of the two classes, foreground or background. In this paper, image segmentation is performed by visualizing images as graphs and then using Max-Flow algorithms to cut the image into two parts. Several Max-Flow algorithms such as Ford Fulkerson, Edmonds Karp, Capacity Scaling, and Dinic's algorithm are used, and finally, the practical efficiency of the algorithms is analyzed based on the results derived from the above experiments. 

## Instructions
--> Execute the file 'driver.py'
> python3 driver.py

--> Browse the target image using the GUI that pops up.  
--> Left click on a few foreground pixels to provide the foregroud seeds in the displayed image. Press 'Esc' button when done.  
--> Left click on a few background pixels to provide the background seeds in the displayed image. Press 'Esc' button when done.  
--> The output segmented image by each of the algorithms: Ford Fulkerson, Edmonds Karp, Capacity Scaling, and Dinic's algorithm will be shown one after another. To close each output window press 'Q' key.
--> After this, all details including plots will be displayed in a final GUI.

## Purpose  

The project 'Analysis of Max-flow/Min-cut Algorithms for Binary Image Segmentation' has been created as a mini project for the course IT300- Design and Analysis of Algorithms.  

## Contributors  

- Pratham Nayak (191IT241)  
- Aprameya Dash (191IT209)  
- Suyash Chintawar (191IT109) 