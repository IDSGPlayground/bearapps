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

Welcome to BearApps! BearApps is an Django based application that provides
an easy and centralized way for UC Berkeley students to download software, 
specifically MatLab.

1. Make sure your python version is up to date. This project is based on python 
2.7. To check, run the command:

    python -V

If your python version is less then 2.7, we reccommend updating to 2.7.

    how do I update python?
    
2. You will need pip for some of the installs:

    sudo apt-get install python-pip

3. If needed, install git, the revision control system used for this project:

    sudo apt-get install git
    
Make a git repository in your home directory, to house ALL your git repositories:

    mkdir ~/GITREPONAME
 
4. Django is necessary to run the application as it's based on the Django
framework. To install Django enter in the command:

    pip install django
        
5. Fially, to download the files necessary to run BearApps, use github. Browse to:

    https://github.com/IDSGPlayground/bearapps

and either fork the repository to your own account for downloading OR clone
the repository directly onto your system using the command:

    git clone https://github.com/IDSGPlayground/bearapps.git

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
Matlab and Matlab + Toolbox. You can click on any of the tiles to bring down
a dropdown menu that contains the information about the app and the button to
request it. After you click the request button, it will be grayed out.

If you entered in the credentials of a professor or RSO, you should be 
redirected to:
	
    localhost:8000/manage

Here, you will see the current licenses owned and the requests made by 
members of your group. You can revoke licenses, deny licenses, and approve 
licenses by clicking the respective buttons. If you approve a license, 
you must also select a chartstring. If you do not have a chartstring, 
you can click the "Chartstrings" tab under "Manage Licenses". Once there, 
you have the option of adding a new chartstring by clicking the "Add New 
Chartstring" button. The "Groups" tab shows all the groups that the user
belongs to and the member in each group.

If you entered the credentials of an admin, you should be redirected to:

    localhost:8000/admin

Here, you will see a table of all the purchases made by all the users. 
You can sort by chartstring, username, group, description, date approved,
price, or RSO. There is also a separate table for the chartstrings, which 
contains the name and chartstring for each. You can also sort this be name 
and chartstring.

==========================================================================
SECTION IV. BROWSING AND FEATURES

BearApps features a notification tab on the upper right-hand corner of the 
screen. Undergradute and Graduate users will recieve message regarding the 
state of their requested app. If the manager approves the user's requested 
app, the user will receive a notification indicating so. Managers also receive 
notifications about requests for software made by members in their groups. 
Moreover, these notifications also remain with the user until he or she has 
clicked the "CLEAR ALL NOTIFICATIONS" button in the norifications box.

Another useful feature is the "My Apps" tab the to top of the page for 
Undergraduates and Gradutes. Here, the user will be able to see all the approved
and downloadable apps.

Also, we included dropdown box in the manage page that displays the past history 
for each user and chartstring when clicked. The history includes the software 
name, date approved, and the cost of the software. 

We also implemented a registration sheet that is displayed if you enter in 
a user name that does not exist in the database (or if you do not enter in 
any user name and password combination), you will be redirected to a registration 
page, where you can register a new user. Also, note that if you enter in a user 
name and password combination that is incorrect, you will not be directed to the
registration page.

Finally, we also a table into the admin page that can sort itself based on 
software name, user name, date, price, RSO, and date approved. The table can 
be sorted by pressing the arrow icon to the right of each column. This makes 
for a compact interface that does not need extra buttons of tabs to sort the table.

==========================================================================
SECTION V. USER TYPES AND USER SETTINGS

Undergradute and Gradute: Have the ability to request and, once approved,
download software. They belong to one or more groups that are managed by an
RSO or professor. They may belong to several groups.

RSO and Professor: Approve, deny, or revoke the licenses of the users within
their groups. As with Graduates and Undergraduates, they may belong to several
groups. RSOs and Professors also have the ability to enter in new chartstrings
that are used to charge for software requested by the Graduates and Undergraduates

Admin: Access to a complete table of purchases made by any user in BearApps. 
He or she can organize and keep track of activity within the application.


