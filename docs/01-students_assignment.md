# Students assignment

## Project description

“The Fit Company” is a stratup building cutting-edge AI-powered fitness coach.
The start-up is growing very fast and is having trouble scaling the team and its technology.
As part of the architecture team, your mission is to break down this application into microservices that can scale, evolve independently, and deliver a great user experience.
The AI Fitness Coach will allow users to:

- Set their fitness goals (e.g., weight loss, muscle gain, endurance)
- Receive personalized workout plans based on those goals
- Get dietary guidance tailored to their profile
- Manage their profile, physical metrics, and preferences
- Upgrade to premium plans and handle payments securely

## Application discovery

This is your first day on the job, before we start re-architecting the application, we need to understand the current state of the application.

- Play a bit with the application using Bruno, read the code and the docs.
- Run the tests. There is a failing test that you should fix.
- Use Flask Blueprints to separate the different API endpoints.
- Dockerize the app

## Add user exercices history

Users are complaining that the coach is repeating the same exercices every day.

The product team decided that we should store the user's exercices history and avoid repeating them the next day.

- Create a new table in the database to store the user's exercices history
- Update the WOD generation to not repeat the same exercices

## First microservice

### Estimate load

Our user base is growing rapidly, it seems that our bottleneck is the generate WOD API that takes up to 5 seconds to send a response to the user.

Your first task is to estimate up to how many users we can scale the service with the current infrastructure.

Use k6 to test the API and find the maximum number of users that can use the service.

### Create first microservice "coach"

In order to scale the application, we need to extract the WOD generation into a separate microservice.

Create a first microservice that will be responsible for generating the WOD.

We cannot afford to have downtime during the migration.

- The microservice should not store the user's exercices history since it's not part of the responsibility of this microservice.
- Implement a strangler fig pattern for the migration.
- Write a design document explaining the migration steps and the reasoning behind the choices. You'll be graded on how well you can explain the choices you made.
- Document should be placed in adr/02-coach-service-migration.md. Do not be overly verbose (i.e no LLM generated text), the document should be a good summary of the choices you made and why.
- Link to your group repository should be sent to my email address.
- Delivery should be on Monday 2025-05-26T20:00:00Z.
