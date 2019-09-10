# StudentAttendance
KPI student attendance 
```
1- git init
2- git add .
3- git commit -m "Add all my files"
4- git remote add origin https://github.com/USER_NAME/FOLDER_NAME
5- git pull origin master --allow-unrelated-histories
6- git push origin master
```
### Step 1
```
Add 'Procfile' with the following text:
web: python manage.py runserver 0.0.0.0:$PORT
```
### Step 2
1. Disable the collectstatic during a deploy <br>
 `heroku config:set DISABLE_COLLECTSTATIC=1`<br>
2. Deploy<br>
`git push heroku master`<br>
3. Run migrations (django 1.10 added at least one)<br>
`heroku run python manage.py migrate`<br>
4. Run collectstatic using bower<br>
` heroku run 'bower install --config.interactive=false;grunt prep;python manage.py collectstatic --noinput'`<br>
5. eEnable collecstatic for future deploys<br>
` heroku config:unset DISABLE_COLLECTSTATIC`<br>
6. Try it on your own (optional)<br>
`heroku run python manage.py collectstatic`<br>

## Step 3
```
$ git add .
$ git commit -m 'init'
$ git push heroku master
$ heroku ps:scale web=1
$ heroku run python manage.py migrate
```
