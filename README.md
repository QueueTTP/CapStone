# Authors
- **Peter Van Beever:** [GitHub](https://github.com/PeterVanBeever)
- **Teddy Archibald:** [GitHub](https://github.com/teddyvere)
- **Qian Wang:** [GitHub](https://github.com/CITATS928)
- **Tim Linkous:** [GitHub](https://github.com/TimLinkous)


# Starmeter
Starmeter is a dynamic web application designed for agents, promoters, and managers to track and analyze the impact of various events on a celebrity's public image in real-time. By inputting data related to a celebrity's social media posts, news mentions, and public appearances, users can monitor how these events affect popularity metrics and public sentiment through an intuitive dashboard.

![Real-Time chart](images/Real-time_chart.png)

# Overview
Managing a celebrity's public image is crucial, and Starmeter provides real-time insights into events that influence public sentiment. Whether it's a new release, a public controversy, or a major appearance, Starmeter tracks these events and displays their impact through real-time visualizations.

![StarMeter Future](images/StarMeter_Future.png)

With this information, you can:

Adjust publicity strategies based on real-time data.
Respond quickly to negative press or controversies.
Make informed decisions to boost a celebrity’s public image.
Monitor key performance indicators (KPIs) and event logs to understand the trajectory of a celebrity’s popularity.
Features
Real-Time Data Tracking: Continuously processes data related to celebrity events such as social media activity, news articles, and public appearances.
Sentiment Analysis: Analyzes public sentiment surrounding the celebrity, identifying positive or negative trends.
Interactive Dashboard: Visualizes KPIs and event logs, offering a comprehensive view of the celebrity's current standing.
Event Impact Analysis: Tracks how specific events affect the celebrity's popularity and sentiment over time.
Publicity Strategy Optimization: Provides real-time feedback, enabling you to adjust strategies to maintain or improve the celebrity's public image.
Minimum Viable Product (MVP)
Data Pipeline: Integrate and process data from various sources (social media, news, etc.) in real time.
Dashboard: Display key performance indicators and event logs with visualizations to track popularity trends.
Event Tracking: Monitor how different events impact public sentiment and popularity metrics.

![Website](images/Website.png)

Technologies Used
Python: The core programming language used for the application.
Flask: A lightweight web framework for building the Starmeter web application.
Flask-SocketIO: Enables real-time event updates to the dashboard.
SQLite: A lightweight database for storing processed data.
SQLAlchemy: ORM (Object-Relational Mapping) to interact with the SQLite database.
JavaScript & Plotly.js: For real-time, interactive data visualizations in the dashboard.
Jupyter Notebook: Used for prototyping and exploring data insights.

![Pipeline](images/Pipeline.png)



For this project, we designed and implemented two main database tables: one for storing user default settings and another for tracking changes in user preferences with dynamic probability. These tables are connected to the Amazon Relational Database Service.

We used Python and MySQL-connector to develop the Event Sim module, which simulates real-world events that affect user preferences in real-time, dynamically modeling changes in public opinion.

We used Apache Kafka to build data pipelines, allowing producers to send data and consumers to process it, enabling real-time event processing. Kafka facilitates the flow of event data into the system, where user preferences are updated based on these events. 
