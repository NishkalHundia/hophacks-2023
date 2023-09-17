# hophacks-2023 - Medi Mingle

This is the backend

Please visit the frontend here
https://github.com/dappon4/HopHacks2023

## Inspiration
Moved by the alarming news of thousands of patients suffering from drug interactions annually, we felt compelled to create this app for the safety and well-being of patients worldwide. Many of us have had close encounters with the dangers of drug interactions, making us realize the need for a simple, user-friendly solution. This app is our inspired response to a global health concern.

## What it does
Our app is designed to help patients check for potential drug interactions. It’s connected to a comprehensive database of medicine interactions, allowing users to quickly and accurately assess the compatibility of their medications. Users can input their medication information through various methods, such as scanning the medicine or typing it manually. The app also stores the list of medicines the user is currently taking, making it easier to manage and review their medication regimen. It’s a simple, user-friendly solution for a critical health concern.

## How we built it
Our application was built using a combination of robust technologies and resources. On the backend, we used Flask, a lightweight and flexible Python web framework. For storing patients’ medicine data, we utilized PostgreSQL, a powerful, open-source object-relational database system.

We sourced our interaction database from rxnav.nlm.nih.gov, a reliable resource for medication information. This allowed us to provide accurate and up-to-date drug interaction data to our users.

On the frontend, we used ReactJS, a popular JavaScript library for building user interfaces. To facilitate the app building process, we used Expo, a framework and a platform for universal React applications.

We also incorporated artificial intelligence into our app. We used a text recognition AI to recognize text from images and an NLP (Natural Language Processing) AI to accurately extract the medicine name from the recognized text.

Finally, we hosted our application on DigitalOcean using free student credit. This provided us with a cost-effective solution for deploying and managing our app.

In summary, our application is a blend of advanced technologies and high-quality resources, all aimed at ensuring patient safety and convenience.

## Challenges we ran into
We faced several challenges during the development of our application.

One of the main challenges was ensuring good performance while hosting the application. Initially, we hosted the application on our laptops, but we soon realized that this was not a sustainable or efficient solution. We then transitioned to hosting on DigitalOcean, which presented its own set of challenges but ultimately provided a more robust hosting solution.

Setting up PostgreSQL was another hurdle we had to overcome. As none of us were familiar with this database system, it took some time and effort to get it up and running smoothly.

Additionally, none of our team members had prior experience with frontend development, including working with ReactJS. This meant that we had to learn as we went along, picking up new skills and knowledge throughout the development process.

Accomplishments that we're proud of
One of our proudest accomplishments is the rapid mastery of ReactJS during the hackathon. Despite having no prior experience with this technology, we were able to learn and apply it effectively to complete our project. This not only showcases our adaptability and determination but also our passion for continuous learning and growth.

## What we learned
Throughout the course of this project, we gained valuable knowledge and experience in several key areas. We learned ReactJS, a popular JavaScript library for building user interfaces, which was a new skill for all of us. Some team members also learned PostgreSQL, a powerful open-source relational database system, while others familiarized themselves with Flask, a micro web framework written in Python. This project served as a great learning platform for us, enhancing our technical skills and understanding of these technologies.

## What's next for Medi Mingle
Looking ahead, we have exciting plans for Medi Mingle. We aim to expand its functionality to include features for nurses, enabling them to manage their patients’ medications and communicate effectively about the right medication. This will further enhance the app’s utility in healthcare settings, promoting better patient care and medication management.

Additionally, we plan to integrate notifications into the app. These reminders will alert users when it’s time to take their medication, ensuring adherence to their medication regimen. This feature will make it even easier for users to manage their health and stay on top of their medication schedules.

In essence, our future plans for Medi Mingle revolve around making it an even more comprehensive and user-friendly tool for medication management and patient care.
