#!/bin/bash 
set -e 
# environment variables 
if [ "$ENV" = 'DEV' ]; then 
  echo "Running Development Server" 
  flask run --host=0.0.0.0 --reload
elif [ "$ENV" = 'UNIT' ]; then 
  echo "Running Unit Tests" 
  flask test 
else 
  echo "Running Production Server" 
  gunicorn --bind=0.0.0.0:8888 index:app --reload 
fi
