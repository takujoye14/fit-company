## Context

To scale our application and handle CPU-intensive tasks we moved the **Workout of the Day (WOD)** logic into a separate microservice called **coach**.

## Steps

1. We extracted the WOD logic from the main fit application into a new Flask microservice (coach) that included:
    - an app.py with a basic flask model
    - routes/wod_routes.py that gets the user email from the main (fit) application
    - services/wod_service.py that has the generate_wod function that generates a WOD with some dummy data and a heavy_computation function that simulates a delay due to a time-consuming task.

    Also we initially used dummy data in the coach service to test the integration and to make sure that the communication worked.

2. We added the coach service in the docker-compose.yml and created a new separate Dockerfile.coach (configuring the run port on 5002)

3. We integrated the coach microservice with the main fit application:
    - Updated the request_wod function in fitness_coach_service.py to make a GET request to the coach service’s /wod endpoint.
    - We kept using dummy data and heavy computation to test the end-to-end communication.

4. We updated the coach service’s endpoint to from a GET to a POST request with user_email and excluded_ids (yesterday’s exercises). We updated the coach service to handle this POST request and to return a dummy WOD list, to ensure that we implemented correctly the exercise filtering logic.

5. We updated the main application service’s fitness_coach_service.py:
    - Removed the local heavy computation.
    - Implemented a POST request to the coach microservice with user_email and excluded_ids.
    - Logged today's exercise history in the local database after receiving the WOD.

6. After making sure the communication between both api's was working we updated the coach service to use real exercise data provided by the fit api:
    - The main fit service now sends all exercises excluding yesterday’s to the coach service.
    - The coach service uses the real data to generate a WOD and then returns it to the main service.
    - Suggested weights and reps are generated within the coach service.

7. We tested all endpoints and made sure the applications are working perfectly.

8. We wrote an OpenAPI specification (openapi.yml) for the coach service’s /wod endpoint.



4. We changed the request_wod() function in fitness_coach_service to:
    - Remove the heavy computation logic
    - Fetch yesterday’s exercise history from the local database.
    - Send a POST request to the coach microservice (instead of calling the logic internally).
    - The request body includes the user_email and excluded_ids.
    - Remove the exercise filtering and sampling because now we handle that in the coach service.
    - Added logic to:
        Log today’s exercise history using the local database.
        Fetch exercise details for today’s selected exercises from the local database.
        Retrieve muscle groups for each exercise.

3. We updated the /wod endpoint on the coach service (from GET to POST) to accept POST requests with user_email and excluded_ids from the fit application.

4. We updated the wod_service to exlude the exercises that were inlcuded in yesterdays workout (sent through the /wod endpoint body), create a list of 6 exercises and return them in JSON format to the fit api.

5. We updated the fit/services/fitness_coach_service.py to fetch yesterdays exercises ids from the database, send a POST request with them to the coach microservice and to save today's exercise history locally.

6. After testing and confirming everything works correctly with dummy data 

. We wrote an OpenAPI spec for the coach service’s endpoint.