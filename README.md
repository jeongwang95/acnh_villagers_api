# ACNH: My Villagers

### Decide which villagers you want to have in your island before you start your jounrey in Animal Crossing New Horizons

With ACNH: My Villagers, user will be given their unique user token. 
With tokens, users can make HTTP reqests to the server to Get, Add, Edit, Remove villagers.
Users can go to the browse page to view all of the available villagers in Animal Crossing. 
User can also add villagers from the browse page, and the added villagers will show up in the user's profile page.
<br />
Animal Crossings Villager's data is pulled from a third party API called [ACNH API](https://acnhapi.com/).
<br />
***
Full-stack of the project was created with Flask, a Python Frame work.
<br />
***
Blueprints:
* api: used to make CRUD operations to our server hosted on ElephantSQL
* auth: handles user authentication (signin/signup/signout)
* site: renders the browse and profile pages of application
***
Models:
- User: holds id, first/last name, email, password, and date created
- Villager: holds id, name, species, villager statistics, and the user id that is associated with the villager
***
<br />
Check out the application [HERE](https://strengthened-silver-caper.glitch.me/signin)
