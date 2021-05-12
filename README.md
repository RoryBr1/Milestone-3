![Logo](/static/readme-assets/logo-readme.png)
# Data-Centric Project | Recipe Website

# Table of Contents

1. [Overview](#overview)
2. [UX](#ux)
    * [Developer Goals](#developer-goals)
    * [User Stories](#user-stories)
    * [Design](#design)
    * [Concept & Font Choice](#concept-and-font-choice)
    * [Colours](#colours)
3. [Features](#existing-features)
    * [Existing Features](#existing-features)
    * [Future Features](#future-features)
4. [Technologies Used](#technologies-used)
    * [Flask-MongoDB](#flask-mongodb)
    * [Coding Languages & Libraries](#coding-languages-and-libraries)
    * [Software](#software)
    * [Additional Tools](#additional-tools)
5. [Deployment](#deployment)
    * [GitPod Deployment](#gitpod-deployment)
    * [Heroku](#heroku)
6. [Testing](#testing)
7. [Credits](#credits)
    * [Acknowledgements](#acknowledgements)

<hr>
<hr>

## Overview

JunkFood Vegan is a data-centric web project built as part of the _[CodeInstitute](http://www.codeinstitute.net/) Full-Stack Software Development Course._
It is a dynamic recipe website built with two users in mind; the _end user_, and the site _administrator_.

The end user can browse, view and share recipes. 
The site administrator - once authenticated - can add, edit, delete and categorize recipes using an intuitive web interface.
Recipe entries include information such as preparation time, ingredients, instructions and an image.
Each recipe is assigned to a category; users can choose to view recipes by category, and the site administrator can add, rename, and delete categories.

The website is fully responsive, utilizing simple and colourful design language and an intuitive information structure.

[⇧ Back to Top](#table-of-contents)

<hr>
<hr>

# UX

## Developer Goals
* Create an easy-to-use website for the end-user to browse and view recipes.
* Allow the end-user to share recipes on social media sites.
* Create an intuitive interface for the site administrator to add, delete and edit recipes.
* Allow the site administrator to add, edit and delete categories.
* Allow the end user to search recipes by search term, and view recipes based on category.
* Provide links to social media pages run by the site administrator.

<hr> 

## User Stories
1. As a _site administrator_, I want to upload recipes to the site for the _end-user_ to view. I want to be able to edit and delete these recipes if needed.
2. As a _site administrator_, I want to sort the recipes into separate categories for ease of browsing. I want to be able to rename or delete these categories, and add new categories in future.
3. As a _site administrator_, I want to ensure that only I can alter the content of the website.
4. As an _end-user_, I want to browse recipes relevant to me; including searching through them using search terms, or view only Breakfast recipes.
5. As an _end-user_, I want to share a good recipe I found on the site with my friends on social media.
   
### How does the website function to meet the needs of the user, as described in the user stories?
1. The _Add New Recipe_, _Edit_ and _Delete_ functions enable the administrator to fulfill these Create, Update and Delete functions.
2. The _Manage Categories_ page allows the administrator to add, delete and rename recipe categories.
3. The site requires administrator _authentication_ to reveal the administrator features. This is done on the _"Admin Login"_ page.
4. The homepage displays all recipes on the site. The _search_ feature enables the user to view recipes matching their search query. The _category select_ function allows the user to view recipes belonging to a selected category. 
    A preview of the recipe is shown; when clicked, the user is directed to the full recipe page.
5. When a recipe has been clicked, _"Facebook Share"_ and _"Tweet"_ buttons are shown below the recipe image. The user can click either to share the URL of the recipe on the chosen social media site.

[⇧ Back to Top](#table-of-contents)

<hr>

## Design
![AmIResponsive Screenshot](/static/readme-assets/responsive-screens.png)

* [Click here to view wireframes.](/static/readme-assets/wireframes.md) <br>

### Concept and Font Choice
The site is designed to appear clean, professional, and uncomplicated while also appearing vibrant and welcoming.
The <a href="https://www.dafont.com/lemon-milk.font" target="_blank">Lemon Milk</a> font was used in the design of the logo, and the <a href="https://fonts.google.com/specimen/Titillium+Web" target="_blank">Titillum Web</a> font 
is used throughout the site in headers, body text and footer. 

- [Hover.CSS](https://ianlunn.github.io/Hover/) - CSS library used for hover effects on site buttons.
- [FontAwesome](https://fontawesome.com/) - Webfont library used for icons throughout the site.

### Colours
The recipe site's personality is fun vegan food. Playful colours were selected to be used in the site layout. 
All colours on the site are either directly from the <a href="https://materializecss.com/color.html" target="_blank">MaterializeCSS</a> Color page, or are RGBA variants of those colours.
Main colours used are: cyan darken-1, cyan accent-4, orange accent-3, orange darken-2 and  red lighten-2.

![Image scheme](/static/readme-assets/colours.png)

_Some examples of the colours as used throughout the site_

[⇧ Back to Top](#table-of-contents)

<hr>
<hr>

# Existing Features
The site's structure consists of
- **Homepage** which displays all recipes, as well as search and sort-by-category functionality. When logged in as admin, relevant control panel links are also displayed.
    This uses the *get_recipes* python function.
- **Admin Login** page which allows the user to authenticate themselves using a username and password, as well as **Logout** buttons.
    These utilize the *admin_login* and *logout* python functions.

    ![Admin Login](/static/readme-assets/admin.png)

    - _The admin-login page can be accessed by clicking the link at the bottom of each page._

    ![Admin features](/static/readme-assets/admin-features.png)
    - _Once logged in as an admin, links to the content-management features are displayed at the top of the recipe list._
- **Recipe Page** for each recipe which is loaded when a recipe link is clicked on the homepage.
    This utilizes the *show_recipe* python function.
- **Add New Recipe** - used to add a new recipe to the database.
    This utilizes the *add_recipe* python function.
- **Delete Recipe** allows the admin to delete the given recipe. This utilizes the *delete_recipe* python function.
- **Edit Recipe** allows the admin to edit the selected recipe. This utilizes the *edit_recipe* python function.
    ![Edit and delete buttons](/static/readme-assets/edit-delete.png)
    - _Edit and Delete buttons as displayed when logged in as admin_
- **Manage Categories** function; used to manage the recipe categories which are used by the end-user to sort recipes.
    This utilizes the *add_category*, *delete_category* and *rename_category* python functions.
- **Flash Messages** display a simple message to the user confirming actions such as searches, recipe deletions, login actions etc.
    ![Flash Message](/static/readme-assets/flash-message.png)
    - _Flash messages are displayed at the top of the page and disappear after several seconds_

<hr>

## Future Features
- Currently, when a category is deleted in the _Manage Categories_ section of the site, the recipes within that category are not deleted and have to be deleted manually if desired.
In future, a feature could be added giving the option of deleting all recipes within the category. 
- At present, there is no way for users to save recipes that they like aside from bookmarking them in their browser. A simple login system could be implemented which allows users 
to create an account and save recipes that they like to that account.

[⇧ Back to Top](#table-of-contents)

<hr>
<hr>

# Technologies Used

## Flask MongoDB
The website is built using the [Flask Web Framework](https://flask.palletsprojects.com/en/2.0.x/).


[MongoDB Atlas](https://www.mongodb.com/) is used for data storage. Documentation detailing setup can be found [here](https://docs.atlas.mongodb.com/getting-started/).


## Coding Languages and Libraries

* [HTML5](https://www.w3.org/standards/webdesign/htmlcss.html) - Used on all pages for page structure and content.
* [CSS](https://www.w3.org/standards/webdesign/htmlcss.html) - Used on all pages for content styling and placement.
* [MaterializeCSS](https://materializecss.com/) - Front end CSS framework.
* [jQuery](https://jquery.com/) - JavaScript library used for intilization of MaterializeCSS features.
* [Jinja Template Language](https://jinja.palletsprojects.com/en/3.0.x/) - used for page templating in Flask.
* [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) - enables Flask to interact with the MongoDB database.
* [Python](https://www.python.org/) - used throughout site alongside Flask-PyMongo.

## Software

* [GitPod](https://www.gitpod.io/) - Code editor used throughout development to write code.
* [GIMP Image Editor](https://www.gimp.org/) - Used throughout to crop and edit images.

## Additional Tools

* [Balsamiq](https://balsamiq.com/) - Used to create wireframes in the design process.
* [Responsively](https://responsively.app/) - Used to test site responsiveness throughout development.
* [Am I Responsive](http://ami.responsivedesign.is/) - Browser-based preview any website's responsiveness. Screenshot featured in readme.md 
* [Google Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools) - Used throughout development to view the website, test features, test JavaScript, and test responsiveness. 
* [ScreenToGif](https://www.screentogif.com/) - Used to create GIF screen-recordings for readme and testing purposes

[⇧ Back to Top](#table-of-contents)

<hr>
<hr>

# Deployment 

**Required:**

- Python3
- [GitHub](https://github.com/) account
- [GitPod](https://gitpod.io/workspaces) account (for local deployment)
- [GitPod browser extension](https://www.gitpod.io/docs/browser-extension/)
- [Heroku](https://id.heroku.com/login) account
- [MongoDB](https://www.mongodb.com/) account

## GitPod Deployment

1. Login to GitHub, and navigate to the [repository](https://github.com/RoryBr1/Milestone-3)
2. Click on the GitPod button at the top right.
3. Install all requirements; in the terminal of your GitPod workspace, type
   
   ``` pip3 install -r requirements.txt ```

4. Create the database in MongoDB.
    - Signup/login to MongoDB
    - Create a cluster
    - Within the cluster, create the following collections: _categories, recipes, prep_times, users._

5. Create the environment variables