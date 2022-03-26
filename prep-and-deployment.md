# **Wax Crate Deployment Documentation**
When deploying this application, I deployed very early on in the development stages to ensure that I had a solid platform to work on and to ensure that I didn’t run in to any problems towards the project submission. I also wanted to get set up on my production database as soon as possible so that I could begin to fill it with entries. If you wish to use this code as a starting point for your own project, I recommend adopting the same philosophy. The way I developed this application might seem a little backwards. I'm going to break this down into a few significant sections.

* ### [Project Set Up](#project-set-up)
* ### [AWS Set Up](#aws-set-up)
* ### [Deployment](#deploying-to-heroku)
* ### [Production Email Set Up](#production-email-set-up)


# **<a id="project-set-up"></a>Project Set Up**

I used the Code Institute GitPod full template to start this project which came with a Git repository already initialised so you will need to account for that. 

Also, rather than having to go and install the dependencies yourself manually, you should ensure that you have a copy of my requirements.txt file as then you can just issue the following command in the terminal "pip3 install -r requirements.txt" which will install all the dependencies you need to get started. Once all the project packages and dependencies have been installed you will be able to follow my processes outlined below.

Also, if you do add to this project in terms of the dependencies and libraries used, you will need to freeze those libraries into the requirements.txt file by issuing the following command to the terminal "pip3 freeze --local > requirements.txt". Failure to do this will mean that when the app is deployed to Heroku, it wont be able to download and install the dependencies the app needs to run.

Once I had all my dependencies installed, I started the development of my app by issuing the following command to in the terminal "django-admin startproject wax_crate". This created my project level directory, off which the rest of the app is supported.

Now that I had the project started, I created the first app within the project (this being the "home" app) by issuing the following command to the terminal "python3 manage.py startapp home". This step was followed for each of the additional apps I created for the project. Every time that this step is completed, I had to return to the project settings.py file and add the newly created app to the list of installed apps. You can see this demonstrated in the screenshot below:

![installed apps list](deployment-md-images/installed_apps.PNG)

Any time that a new app is added or any time that a data model is changed there are few commands that you will need to issue. As a genreal rule of thumb, I like to run a few extra commands just to make sure anything I'm migrating to the database is correct. Just before I detail the commands, if you switch databases and you haven't made the migrations on the new database, you will have to run the migrations again. The commands are:

1. python3 manage.py makemigrations --dry-run - This shows a dry run of the creation of the migrations script without actually making the migrations, this allows you to check that the migrations are within the scope that you require. 

2. python3 manage.py makemigrations - This creates a migrations script.

3. python3 manage.py migrate --plan - This plans all of the migrations scripts that have been created and allows you to check the scope before the migration scripts are pushed to the database.

4. python3 manage.py migrate - This command pushes the scripts to the database.

To check that Django is installed correctly, type python3 manage.py runserver into the terminal, and you should see the Django success message.

## **Setting up the Heroku App & Database
1. Go to [Heroku](https://id.heroku.com/login) and signup for an account if you don’t already have one. If you do, sign in so that you can see the Heroku dashboard. 
5. Click the new button in the top right hand section and select “Create New App”
6. Give the application a name and select the region. When selecting a region, select the option that is closest to you. 
7. Click the “Create App” button at the bottom of the form.
8. Once the app is created, select it by clicking the application name.
### **Application Dashboard**
At this stage, I installed some add ons into the application to serve as the database. 
### **Resources Tab**
1. In the application dashboard, select the resources tab.
2. In the resources tab, in the search bar type “Heroku Postgres”. When it appears as an option in the drop down, select it.
3. Following the above step will open an order form. For the purposes of this project, I left the “Plan Name” field as “Hobby Dev – Free”. If you deploy this application yourself, depending on the scope of the application and its use, you may need to select something different. 
4. Click “Submit order form”.
5. You will now see that the “Heroku Postgres” add on is included in the “add-ons” section of the Heroku application. This will serve as our database whilst the application is deployed. I used this database from very early on the project

### **Settings Tab**
We have completed the necessary steps in the “Resources” tab now. Once the above has been completed, click the “Settings” tab and follow the steps below.

1. In the settings tab, click the “Reveal Config Vars” button. Contained within this section, we will detail our environment variables such as database URL, secret keys and other environment variables. These variables allow the project to function once deployed (Note: Some of the details within this section will be redacted for security purposes but I will explain the processes that need to be followed. 

2. Upon revealing the config vars, you will see text fields. One of the fields will already be populated with the “DATABASE_URL” variable. You must copy the value assigned to this variable as you will need to use it in your project to serve as the connection to the Heroku Postgres database add on we added in the previous section.

3. Once the string of text assigned to the “DATABASE_URL” variable has been copied, return to the workspace.

## **Creating an env.py file**

Now that the Heroku app is set up and the PostgreSQL database has been added, I created an env.py file within my workspace. I will show a screenshot of my env.py file below but I've redacted the variable values so as to keep my application secure. The env.py file is an untracked file so it wont appear in the GitHub repository. In my case, it was included in my gitignore file so you would need to consider doing something similar. I'm going to show you the completed env.py file from my project but just to be super clear, I built these variables up over the course of a few weeks of development.

![wax-crate-env-file](deployment-md-images/env-1.PNG)

I've imported the os module at the top of the file to set the variables in the environment. Using the module allows for the values of my environment variables to be passed through the operating systems between tracked and non tracked files and hidden by the variable name as opposed to hard coding them.

1. DEBUG & DEVELOPMENT - These two variables are responsible for switching key settings such as switching DEBUG to False in production and changing the email back end from the Gmail account in production to the console version in development.
2. I've created a DATABASE_URL variable and given it the value I copied from Heroku. I then access this variable in the settings.py file and using dj_database_url, connect to the external database. Theres a conditional check involved in this to see whether the DATABASE_URL is True in the environment. If true, I'm using my external database and if false, Im using the SQL lite database that comes with django. 
3. SECRET_KEY - I set this myself as an alpha numeric string and pulled it into the settings.py file to set the SECRET_KEY setting via the environment variable using the os.environ.get() method.
4. STRIPE KEYS - To access these values, you need to go and sign up for a Stripe account and then in the developer dashboard you will be able to access your "publishable key" which you should assign to the STRIPE_PUBLIC_KEY variable, the secret key, which you should assign to the STRIPE_SECRET_KEY environment variable and finally the two webhook signing secrets. You can only access these by setting up a webhook endpoint in the stripe developer dashboard. You will notice that I have two that was becuase I set up two webhook endpoints, one for my development environment (which required its own webhook signing secret) and my deployed version. One tip I would give with this is watch the URL that your local development site is on as it will sometimes change slightly and as a result, if you try to process a payment via Stripe and the URL of the local running version of the server has changed, it will give you a 500 response on stripe. Fortunatley, the Heroku webhook endpoint is completley static and does not change. 

Once you have created your env.py file, you need to replicate it within the Heroku config vars as the env.py file will not be accessible when the site is deployed.

You can see from my example below, that I have duplicated the variables from my env.py file and their values (redacted) into the Heroku config vars (for the STRIPE_WH_SECRET i used the specific key generated when I set up my Heroku webhook endpoint). Just note, there are some environment variables for AWS and the production email client in there, just ignore them for the moment and focus on the database url, the secret key, and the stripe keys for now:

![heroku config vars](deployment-md-images/heroku-env-starting.png)

At this stage in the process, I left Heroku alone for the time being whilst I completed some additional steps towards setting up my AWS bucket and a very small piece of development in the home screen of the app prior to deploying. It was important at me to get all of the required functionality in Heroku and AWS set up to build on as a solid foundation. I'm going to talk you through the AWS set up process and then the final Heroku steps I took to get the fledgling version of the app up and running.

N.B. - You will probably need to add a DISABLE_COLLECTSTATIC environment variable set to 1 right at the start as there are no static files to collect at the moment but we will be removing later on in the deployment process.

# **<a id="aws-set-up"></a>AWS S3 Set Up**
As the site is being deployed to Heroku, I decided to use Amazon Web Services' S3 cloud hosting service to store my static and media files. I followed the following steps to set up an account and integrate it into my project.
## Registering and Setting Up A Bucket
1. Go to [aws.amazon.com](https://aws.amazon.com/) and register for an account.
2. Once registered, you will be at the management console. You need to find the S3 service in the search bar. 
3. Once you've accessed S3, you need click "Create Bucket" button. This bucket will be the place where the static and media files will be stored.
4. You will need to give your bucket a name, I named mine according the name of my application on Heroku.
5. You will now need to select a region, select the one that is closest to you.
6. Make sure that you select the radio button to enable "ACLs".
7. Make sure that you check the radio button "Bucket Ownership preferred".
8. Click "Create Bucket".
9. Scroll right down to the bottom of the page and find the properties section. 
10. In the properties section, select "Static Website Hosting" and fill in the index and error values as "index.html" and "error.html".
11. Now go to the permissions tab.
12. Find the CORS configuration section. Within this section, I set up the connection between the Heroku app I set up and the S3 bucket.
13. Within the code editor on the CORS configuration page, paste in the below code.
```python
[
  {
      "AllowedHeaders": [
          "Authorization"
      ],
      "AllowedMethods": [
          "GET"
      ],
      "AllowedOrigins": [
          "*"
      ],
      "ExposeHeaders": []
  }
]
```
14. Within the permission section, navigate to the bucket policy section and select the "policy generator". This is used to generate a security policy for the bucket open this in a new tab so that you can easily come back to the previous page without losing your progress.
15. In the security policy form enter the following details
16. Policy Type - Select 23 Bucket Policy
17. Principal - Enter a "*" to allow all principals.
18. Actions - Select "Get object".
19. In the ARN field, copy the ARN number from the previous page and paste it into the field.
20. Click "Add Statement".
21. Click "generate policy".
22. The security policy will be generated in object format. Copy the entire policy.
23. Return to the bucket policy screen and copy the object into the bucket policy code editor.
24. In the object editor, look for the "Resource". The value should be set to the ARN. At the end of the value, add a "/*" to allow full access to all resources the bucket.
25. In the permissions tab, locate the Access Control List. click edit and enable List for Everyone (public access) and accept the warning box. If the edit button is disabled you need to change the Object Ownership section to ACLs enabled.
At this point, the S3 bucket is set up but there are a few more steps that need to be followed.

## Creating a User to Access the Bucket
All of this functionality is handled by IAM, another AWS service. Follow the steps below to set this up:
1. Go back to the services menu on the AWS console and find IAM. 
2. In the sidebar, select "User Groups".
3. Click "Create a New Group".
4. Name your group, in my case I named it "manage-wax-crate-ms5" and click the next step button until you see the "Create Group" button. Click the "Create Group" button.
5. Navigate to the policies section in the side bar.
6. Click the create policy button. 
7. Navigate to the JSON tab and click the "import managed policy" link.
8. In the form that opens, search for the "S3 Full Access" policy adn import it. 
9. Get the ARN from the bucket policy and paste it into the resource key value field but add two values in a list format. In my case, I added the below:
```python
"Resource": [
    "arn:aws:s3:::wax-crate-ms5",
    "arn:aws:s3:::wax-crate-ms5/*"
]
```
10. Click "Review policy"
11. Give the policy a name and description, I called mine "jr-wax-crate-policy".
12. Click "Create Policy".
13. Navigate back to the groups section. We now need to attach the policy we just created to the group.
14. Locate the manage group you just set up, in my case it was called "manage-wax-crate-ms5".
15. Click attach policy.
16. Search for the policy that was just created, in my case it was "jr-wax-crate-policy".
17. Select the policy via the checkbox and click "Attach Policy".

To create a user to put into the group, follow the below steps:

1. Navigate to the users section and click "add user".
2. Create a user, in my case I named my user "wax-crate-staticfiles-user".
3. Ensure that the programmatic access checkbox is checked.
4. Click the next button.
5. Add the user to the "manage-wax-crate-ms5" group.
6. Click through to the end and click "Create User".
7. You will be asked to download a CSV file containing the access credentials. These are really important and can only be downloaded once so please keep them safe. They will also be required to set up the relevant AWS environment variables in Heroku.

## Connecting S3 to the Django App
If you've followed my previous steps and used my requirements.txt file to install all the required dependencies, you shouldn't need to follow steps X below. If you haven't used my requirements file, follow all the below steps.

1. Install boto3 with "pip3 install boto3" in the terminal.
2. Install Django Storages with "pip3 install django-storages".
3. Remember to freeze these into your own requirements.txt file. 
4. Add storages to the list of installed apps as you can see demonstrated below.
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_summernote',
    'home',
    'records',
    'cart',
    'checkout',
    'accounts',

    # Other apps
    'storages', # Hey! Over here!
    'crispy_forms',
]
```
5. At this point, I added some settings into my settings.py file to set up the connection between the bucket and the application. Look at the examples belowand just note that you would have to have your own bucket and keys to get all these settings to work for you:

```python
if 'USE_AWS' in os.environ:
    # File caching control settings
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }

    # Bucket configuration
    AWS_STORAGE_BUCKET_NAME = 'wax-crate-ms5'
    AWS_S3_REGION_NAME = 'eu-west-2'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID') # Declared in Heroku
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY') # Declared in Heroku.
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Static and media files locations when deployed and using S3 as storage.
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    # Creates a static folder in the s3 bucket just like in the workspace.
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    # Creates a media folder within the bucket just like in the workspace.
    MEDIAFILES_LOCATION = 'media'

    # Override staatic and media URLs in the production environment.
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
```
6. Now that those settings are in, we need to go to Heroku and add the environment variables in so that when the project is deployed, it will be using the settings we just specified. Just note here, that I'm not setting any AWS variables in the env.py file because I'm using my worspace to host static and media files in the development environment.

7. Go back to the settings tab in Heroku and reveal the config vars. Add the ones detailed in the screenshot below.  
<img src="deployment-md-images/aws-heroku-vars.png" width="700">

8. The two keys can be found in the CSV file you downloaded from AWS so set them accordingly and the USE_AWS variable should be set to "True" so that the above settings can be accessed when deployed to Heroku. Make sure you keep your keys safe.

9. Within the application, I have CRUD functionality that takes and image file. As a result of this, I needed to make sure that in the production environment, any images added as part of the apps CRUD functionality would be stored in the AWS bucket. To do this, I created a custom_storages.py file in the root directory of the project.

10. In the custom_storages.py file, I created a couple of classes to handle the static and media uploads to AWS. I've detailed the code within the file below and neccessary imports to make the file talk with the rest of the project.

```python
"""
1 - Importing settings file to access locations.
2 - Importing S3 storage class to access S3 on collect static.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """
    Setting static files storages to location
    specified in settings.
    """
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """
    Setting media files storages to location
    specified in settings.
    """
    location = settings.MEDIAFILES_LOCATION
```
11. With these settings prepared, when we deploy to Heroku, the terminal will run the Django collect static command, all the static files within the app will be collected and stored on AWS automatically. For media files that are not uploaded as part of the applications CRUD functionality, they need to be uploaded to the AWS media bucket. To do this, open the media folder on the bucket and click upload, then its just a matter of dragging and dropping the images. In my case, I had to do this with my Hero Images.

12. Add and commit these changes to your repository.

At this stage, I developed the base template and home app so that I had something concrete. I also uploaded the home page hero image to AWS once done so that when deployed, I would be able to ensure that my media files were being served correctly from S3. Once I had completed this small piece of development locally, I was ready to deploy the project which I will go over in the next part of the document.

## **<a id="deploying-to-heroku"></a>Deploying to Heroku**

### Creating a Procfile
This file is really important and will tell Heroku how to run our application.

1. In the top level of the project (the same level as the manage.py file), create a new file called “Procfile” (note that this file must be named with a capital p):
2. Open the newly created Procfile and input the following code.
```python
web: gunicorn wax_crate.wsgi:application
```

Please note that in the above code, I have referenced the name of my Django project wax_crate. When completing your own project, this code would need to change to reference the name of the Django project you set up.

At this stage, I saved all of my files, committed them and pushed them to GitHub ready for a first deployment attempt of the project.

### Deployment
Before attempting the deployment, if you have a DISABLE_COLLECTSTATIC environment variable within your Heroku config vars, delete it as it will prevent the application for deploying as expected as the static files wont be collected from the workspace.

1. Navigate back to your application dashboard on Heroku and click the “Deploy” tab.
2. In the deployment method section, click GitHub. If you haven’t already connected your account, you will need to connect it before you can follow the next steps.
3. Once your account is connected, you can perform a search in the search bar for the GitHub repository you are using to store the code for the application. In my case, I searched for my repository “wax_crate_MS5”. Once you have entered your repository name, click “Search” and provided a matching repository is found, an option will appear below providing you with the button to connect the
repository to Heroku. Click “Connect”.
4. Scroll down to the bottom of the page, and click “Deploy branch”
5. When deploying the application, it is good practice to view the build logs as this will allow you to identify any errors. You can do this by clicking the “View build logs” link. You can see from the build logs that the Django application has now been built in Heroku, once you see this, click the “Open app” button to open the application to check for a successful install.
6. Provided that all the previous steps have been followed, when you open the app, you will see the home page, only if you look at the URL bar, you will see that the application is not running on a local server but instead on our Heroku platform.
7. At this stage, I enabled automatic deployments on the deploy tab of Heroku which meant that everytime my code was pushed up to GitHub, Heroku would run the deployment again. This gave me a really stable platform to gradually develop the application. I developed the rest of the application from this point onwards. The only additional process to go over is how to get the email system working which I wil detail below.


## **<a id="production-email-set-up"></a>Production Email Set Up**
When running in my GitPod workspace, it isn't possible to set the application up to use a real mail server to send out emails. As mentioned previously, I developed my project fully after setting up AWS and getting the first parts deployed as doing all this work first meant I could pretty much develop the app worry free when it came to deployment as it was already done. Right at the end of the development process, prior to application testing, I set up the deployed version of the site to send emails via a free Gmail SMTP server. Let me guide you through the process I followed below:

1. Sign up for a Gmail account [here](https://www.google.com/intl/en_uk/gmail/about/) or if you already have one, just sign in.
2. Once registered or logged in, go to the account settings in the top right. 
3. Click the "Accounts & Import" tab.
4. Click "Other google account settings".
5. On the next screen, in the navigation, go to "Security".
6. Go to the "2-step Verification" setting and turn it on. Following this process will allow us to create credentials that our django application can use to send emails via the server.
7. Click the "Get Started" button and enter your password.
8. Then you will need to select a verification method, I chose to receive an authorisation code via text.
9. Enter the code and turn on two step verification then click the back button until you can see the highlighted security tab in the navigation.  
10. You will now see that under the "Signing into Google" section, there is an "app passwords" setting, click this.
11. Enter your credentials if prompted.
12. On the app passwords screen, select "mail" as the app. In the device type, select "Other" and then type in "Django".
13. Click the generate button which will give you the 16 character password, copy this. 
14. Go to the Heroku dashboard to the "settings" tab.
15. Open the config vars and enter the following additional variables into the config vars:  
<img src="deployment-md-images/email-heroku-vars.png" width="700" alt="Email heroku variables">

16. The EMAIL_HOST_PASS needs to be assigned the 16 character code from Gmail and the EMAIL_HOST_USER variable needs to be assigned your gmail email address.
17. Return to the settings.py file and add the following settings:
```python
# Deployed email settings
# Using console emails if in development environment.
if 'DEVELOPMENT' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'waxcrate_recordshop@example.co.uk'
else:
    # Using Gmail if in production.
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASS')
    DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
```

Once these settings have been entered, save the files, add and commit them to the repository and push them on to GitHub. Once the application has deployed, the best way to test the functionality is the register for a test account and see if you receive the confirmation email from all auth. You can use a temporary email at [temp-mail.org](https://temp-mail.org/en/) to do this multiple times if required.

With that, thats all the deployment steps completed.

Happy coding!