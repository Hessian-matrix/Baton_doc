# Viobot2 Semantic Segmentation

Semantic segmentation is a core computer vision technique that assigns a semantic class label (e.g., person, grass, sky) to **every pixel** in an image, enabling pixel-level scene understanding. Its key idea is to use deep learning models to extract image features and classify each pixel, producing a full-image segmentation mask. Unlike object detection, semantic segmentation does not distinguish different instances of the same class; it focuses on the semantic category of each pixel. It is widely used in autonomous driving and mobile robotics.

![](image/image_grass_split.png)
<center style="font-size:14px;color:#C0C0C0;">Figure 1. Grass segmentation on Viobot2</center>

Semantic segmentation is compute-intensive. To run with low latency and high resolution on embedded low-power devices, dedicated hardware acceleration is usually required (e.g. NPU). Viobot2 achieves this via NPU acceleration as well.

<!-- ![](image/gif_grass.gif) -->
<center style="font-size:14px;color:#C0C0C0;">Figure 2. Grass segmentation on continuous frames</center>

