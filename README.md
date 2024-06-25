# Sports Classification using CNN, Xception, and ResNet

This repository contains code for classifying sports images using Convolutional Neural Networks (CNN), Xception, and ResNet architectures. The project demonstrates how to preprocess image data, build and train deep learning models, and evaluate their performance.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Dataset](#dataset)
- [Usage](#usage)
- [Models](#models)
- [Results](#results)
- [License](#license)

## Introduction

The goal of this project is to classify images into different sports categories using deep learning. We explore and compare three architectures:
- A custom Convolutional Neural Network (CNN)
- Xception
- ResNet (Residual Networks)


## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/your-username/sports-classification.git
    cd sports-classification
    ```

2. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Dataset

The dataset should be organized into `train`, `val`, and `test` directories, with subdirectories for each sport category. Each subdirectory contains the images belonging to that category.
https://www.kaggle.com/datasets/gpiosenka/sports-classification/data


## Usage

1. **Data Preprocessing**:
    To preprocess the images and prepare the dataset.

2. **Model Training**:
     We can choose between the CNN, Xception, and ResNet models by specifying the appropriate script from the `models` directory.

3. **Evaluation**:
    This will generate metrics and visualizations to compare the performance of the different models.

## Models

### CNN

A custom CNN architecture designed for sports image classification.
- Simple and fast to train

### Xception

An implementation of the Xception architecture, known for its depthwise separable convolutions and high accuracy.
- Requires more computational resources

### ResNet

An implementation of the ResNet architecture, which introduces residual learning to ease the training of deep networks.
- Robust and widely used in various image classification tasks

## Results

The results of the trained models, including accuracy, precision, recall, and F1-score, are documented in the `notebooks/evaluation.ipynb` notebook. We can also find visualizations of the model performances and confusion matrices.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---
