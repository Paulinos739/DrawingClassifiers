# Automated Architectural Drawing Classification

This docker image builds an API to categorize architectural drawings with
Convolutional Neural Networks through an HTTP Port.
The goal was to develop a framework to automatically create relevant metadata of drawings
for long-term archiving.
The API takes a user input parsed via the HTTP interface in server.py, runs predictions on n number of  images
and stores the predictions in either a json string or a csv-file. 

This is an ongoing research from the [FID BAUdigital](https://kickoff.fid-bau.de/en/), conducted at the TU Darmstadt.

<img src="C:\Users\PAUL\PycharmProjects\DrawingClassifiers\content\FlowChartPrototype.png"/>

**PredictDrawingCategory**

This script predicts if an architectural drawing either belongs to the category floor plan, section or elevation
through a Multi-Class Classification Model. Accepted drawing types are: floor plan, elevation and section.


**PredictDesignPattern**

This script estimates the presence of certain architectural design patterns in floor plan drawings.
Categories/Patterns include the following shapes: Rectangle, Circle, Composite-rectangular, Organic, Longitudinal, Polygonal.
It furthermore includes the following interior Patterns: Atrium, Column Grid and Staircase.
Accepted drawing types are only floor plans.


**Usage**

Run API with:

1. `git clone`
2. `docker build -t test -f build/package/Dockerfile`
3. `docker -p 8080:8080 run test`
4. `http://localhost:8080/pattern or http://localhost:8080/category`