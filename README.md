# HealthyOrNot

## 💡Inspiration

Small businesses and local entrepreneurs are an essential facet of our communities, with the COVID-19 Pandemic demonstrating how much we depend on them and vice versa. However, it can often be difficult for these businesses to know the best trajectory for their growth, with no streamlined method currently existing for gathering and analyzing their customers' feedback.

SentiView aims to change that.

## 🔍 What it does

Small businesses reply greatly on reviews; they tell them what they're doing right and what to improve. SentiView takes in a set of customer reviews and sorts positive reviews from neutral/negative reviews. Then, it finds the top five keywords that occur the most frequently in the review sets, helping business owners swiftly find the root of their problems.

SentiView takes in a set of customer reviews and uses the power of sentiment analysis in order to determine whether or not they are positive or negative. Then, each review is tokenized and cleaned based on a stoplist. The 5 most common positive and negative words are then displayed to the user; they can then select and scroll through the reviews containing the word, gathering a first-hand view of their business's needs and strengths.

⚙️ How we built it
We developed the application's front end using React, Bootstrap, and Tailwind. The backend used a Flask server that hosted the data generated from the Cohere API, which we used for sentiment analysis and tokenization purposes.

## 🚧 Challenges we ran into

There were a variety of challenges we ran into, primarily with regard to integrating our front and back end systems. We discovered that the Cohere API didn't play along the nicest with React, requiring us to spin up a Flask server to enable us to transfer data back and forth from the API. Setting up this server and enabling it to achieve the desired functionality was a challenge in and of itself, as none of us were particularly experienced with using it.

## ✔️ Accomplishments that we're proud of

The team's synergy was unmatched. We all shared a passion for this project and ferociously pursued its completion to the very end.
Successfully leveraging Cohere to perform NLP tasks and achieve our initial goals.
Our minimalistic, yet powerful home page.
The substantial code! It was our first time using sentiment analysis and flask, which launched some big obstacles along the way (that we powered through, of course).

## 📚 What we learned

How to work with the Cohere API and tailor it for our specific use case.
Some of us interacted with Tailwind for the first time at this hackathon, broadening our knowledge of relevant frameworks.
Flask. Powerful and challenging, we learned how to link the front end with the back end.
How to integrate a Python backend with a React frontend and send data between the layers.
How to use Figma to generate higher-quality and tailored graphics.

## 🔭 What's next for SentiView

SentiView would like to be able to produce graphs that display trends over time in customer satisfaction to give small businesses a way to assess their improvement.
Provide bespoke recommendations to businesses.

## Try Sentiview

Clone the repo

Go to https://dashboard.cohere.ai/register and get an API key

Copy the .env.display file and name it .env

Paste your API key in the .env file

Install Dependencies

    npm i --prefix front

Open terminal and go to the cloned directory

    npm start --prefix front

In a new terminal

    python3 main.py