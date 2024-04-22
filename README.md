# InnSight

## Table of Contents
- [Introduction](#introduction)
- [Data](#data)
  - [Source](#source)
  - [Data Analysis](#data-analysis)
  - [Preprocessing](#preprocessing)
- [Modeling](#modeling)
  - [Approach](#approach)
- [Conclusion](#conclusion)


## Introduction
InnSight - one place to get all details about the places you are going to stay when you are travelling, on vacation or any events. This app provides detailed analysis of all the places you can stay like Hotels. Analyze reviews given by previous customers, provide you with sentimental analysis of the reviews. Help to search places with your amenities. 

## Data
### Source
We have used Dataset from Datafinity which had around 20K hotel reviews along with the ratings. Along with that we extended our search using Google Places API to get realtime reviews of desired places. We have also used date from Kaggle (airbnb).

![image](Resources/Fig1.png)

### Data Analysis

Kept a few features from the dataset to analyze the reviews and ratings.

![image](Resources/Fig2.png)

In the initial dataset we found that the ratings and reviews text was a good features to provide users what they need. We analyzed the reviews text to see what we can extract and score based on the sentiments. This good help users to decide if any specific place is good for them or not. 

Below are some sample charts that helps to understand sentiment analysis and frequent words used in reviews, 

![image](https://github.com/arnabroy-osu/project3-group3-travel-assistant/assets/93089647/aa24be20-28ba-4bb9-b014-ac51cb192b46)  

![image](https://github.com/arnabroy-osu/project3-group3-travel-assistant/assets/93089647/30eb1009-0e5e-4833-aba8-70c2e88d2f5d)  


### Preprocessing
There were 27 features in the dataset, but as mentioned we were more focused on actual entity details like city, state, hotel name its ratings and reviews. Other unwanted features like categories, dates and others were cleaned up along with duplicates and nulls. Even though certain fields were kept for future we didnt use it for current project. 

Using the Google API to get realtime reviews, we specified the fields that needs to be extracted from API so we are not fed with huge data. 

## Modeling
### Approach
We started by using Tdifvectorizer to understand the words in the reviews, the frequency, scoring the words which helps to get the amenities of the hotel. This can be used to help user to select the desired place. 

Then we used sentiment analysis from NLTK and TextBlob to understand the scoring of the reviews itself and provide the details to user. 

Finally we used a Langchain OpenAI and Question and Answer models to analyze the reviews. Provide analysis based on user input. 

Here is the sample output of the app, 

![Screenshot 2024-04-21 at 10 03 57 AM](https://github.com/arnabroy-osu/project3-group3-travel-assistant/assets/93089647/a733bf02-22ff-4313-ac73-ac078fc39266)

### Additional Approach (exploration)
Use **Support Vecor Machine (SVM)** to predict the price based on the reviews. This can be used to provide user with a predicted rating of the hotel. In this example we tried to use 'linear' kernel to predict the price. 

```
  Train Accuracy: 0.445
  Test Accuracy: 0.016
```
**Saving the Model** 
- We saved the model using joblib so it can be used in future. 

```
  import joblib
  filename = '../Resources/svm_model.sav'
  joblib.dump(model, filename)
```

## Conclusion
The app is initial step towards building a larger Travel assistant and make it more interactive and effective so users can completely set their travel plan with just using their natural language. 

## Required Modules
- pip install pandas
- pip install flask
- pip install --user -U nltk
- pip install textblob
- pip install -U matplotlib
- pip install numpy
- pip install python-dotenv
- pip install requests
- pip install langchain
- pip install -U textblob
- python -m textblob.download_corpora