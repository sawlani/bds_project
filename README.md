# BDS Project:

In this project, we developed a tool which enables potential restaurant proprietors to draw inspiration from existing restaurants and their features. The users provide their requirements like cuisine, timings and city of interest using our tool. We fetch and display images of best food items, indoor designs and outdoor designs of restaurants based on the inputs.

# Installation Instructions:

The code package consists of an environment.yml file for Linux based OS and environment_mac.yml file for MacOS. Use the following command for installation:

```
conda env create -f environment.yml
```

Install MongoDB using the instruction here: https://docs.mongodb.com/v3.2/administration/install-community/

Activate the environment and install pymongo using:

```
pip install pymongo
```

Download yelp photos dataset using the URL: https://www.yelp.com/dataset

Place the yelp photos folder in code/static/data and name the folder “photos”

Run app.py to use the tool.

# Datasets

Food-101:
The dataset can be found here: https://www.kaggle.com/kmader/food41 . 
This datasets consists of images of 101 classes of food, 1000 images per each class. We use this dataset to build a classification model for predicting the category of yelp food images.

Yelp Dataset:
The dataset can be found here: https://www.yelp.com/dataset. We use this dataset to retrieve the images of food, indoor designs and outdoor designs based on user query.

