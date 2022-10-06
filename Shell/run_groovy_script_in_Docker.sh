# Run Groovy script in Docker

#!/usr/bin/env bash
docker run --rm -v "${pwd}:/home/groovy/scripts" -w /home/groovy/scripts groovy:latest groovy your_script.groovy