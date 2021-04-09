# task_project specification
Task project

# Tasks
## Environment
- `Dockerize` the project
- Should follow `microservice architecture`
- Use `postgresql` as database

## Pages
- `Home Page` - Shows list of quizzes. Implement pagination.
- `Detail Page` - Details of a quiz containing options with current vote count. User should be able to choose the option and submit. User will be able to add comments for the quiz.

## Admin
- Implement admin options to manage the quizzes by administrators

## Authentication
- Implement user authentication

## API
- An api to create a survey quiz
- Api to list quizzes
- Api to get quiz detail
- Api to edit a quiz
- Api to delete a quiz
- Api to create option for a particular quiz
- Api to see quiz detail along with available options
- Api to vote for a particular option of a quiz
- Api to see result for a particular quiz

## Celery
- Use celery to implement asynchronous tasks
- Send an email to the admins whenever a user makes a comment to a quiz

## Unittest
- Write unittests

## Instructions
- Check the existing code base and work from there
- Follow best practises
- Write clean code
- Update Readme
- Make a branch for each sub task. If done, then make a pull request and merge with `main` branch
- If you need any clarification, contact with us