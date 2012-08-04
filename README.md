BearApps Documentation
==========================================================================
Table of Contents:
    i. Downloading the server application
   ii. Setting up the application
  iii. Getting started with BearApps
   iv. Browsing and Features
    v. User types and user settings

==========================================================================
SECTION I. DOWNLOADING THE APPLICATION

To download the files necessary to run BearApps, use github. Browse to:

	https://github.com/IDSGPlayground/bearapps

and either fork the repository to your own account for downloading OR clone
the repository directly onto your system using the command:

	git clone https://github.com/IDSGPlayground/bearapps.git

This will retrieve the files in the current directory. You may need to
install some additional packages to your system before you can proceed to
set-up. These packages include:
	git
	virtualenvwrapper
	virtualenv
	django

Use virtualenvwrapper to create a virtual environment for python execution
if you haven't already (see documentation online.) Django is necessary
to run the application as it's based on the Django framework.

==========================================================================
SECTION II. SETTING UP THE APPLICATION

To begin set-up, cd into the directory where you cloned the git repository.
If you're not already working on a virtual environment to protect system
dependencies, do so.
Next, begin by preparing the BearApps database by running this command:

	python manage.py syncdb

This creates db.sqlite in the bear_apps directory, which is where the
application will store the database (based on SQLITE). It will ask you
to create a super user to manage the database -- go ahead and do this.
Now, the database needs to be initialized with actual data. BearApps
has a browser-based facility to add this. Run the server with this command:

	python manage.py runserver

Django will run the server on the local host. Open a browser of your
choice and browse to:

	localhost:8000/backend

You should see a log-in prompt. Use the credentials you input when you
created the super user account during the syncdb process. If you enter the
correct credentials, you'll be taken to the Django Administration pane.

BearApps currently supports two applications: Matlab and Matlab with
Toolboxes. Let's add them. Under 'store', click 'Apps' and you'll be taken
to a blank list. click 'Add app' at the top right. Input the following:

	App name:	Matlab
	Href name:	matlab
	Price:		200
	*just type gibberish for the remaining fields.

And then press 'Save' at the bottom right of the list.
Repeat this process once more with the following information:

	App name:	Matlab + Toolboxes
	Href name:	matlab-toolboxes
	Price:		300
	*again, fill in gibberish for the remaining fields.

Now return to the main Django administration pane. Under Store, select
'Groups'. On the new page, click 'Add group' at the top right. Input
any name for the group you please. You may add multiple groups. Click
'Save' at the bottom right of the list after adding each group.
Return to the main Django administration pane again. This completes the
set-up process for the administration pane. You may leave this page or
logout of it if you want.

Now you can add users to the database. Browse to the following:

	localhost:8000/register

and create as many users as you want by inputting a name, a unique
id number, and password. For each of these users, type the name of ONE
of the groups (the only one, if you only created one in the previous step)
and choose that. Select the 'Graduate' radio button for ALL of these users.
Next, create a manager. Using localhost:8000/register, input another set
of user credentials (including the same group), but this time select the
'RSO' radio button. Finally, create an administrator. Use the same page and
process again but select the 'Admin' radio button. After you've created
these accounts, your BearApps application should be prepared for use.

==========================================================================
SECTION III. GETTING STARTED WITH BEARAPPS

To enter BearApps, return to the log-in page of the application by typing:
    
        localhost:8000

Input the username and password of one of the users created in the register
page.

If you entered in the credentials of a Graduate or Undergraduate, you
should be redirected to:

        localhost:8000/browse

Here, you will see the apps available for you to download, which should be
Matlab and Matlab + Toolbox. 


