# Run Groovy script in Docker
docker run --rm -v "${pwd}:/home/groovy/scripts" -w /home/groovy/scripts groovy:latest groovy your_script.groovy