# TODO LIST
- [ ] back arrow

## Search Professors
- [ ] crop seach results


## User Accounts

#### Backend:

---

## Sign Up/Login

#### Frontend:
./components/Signup.tsx


#### Backend:

 localhost:8080/signup
 - [ ] cleaner login time

---

## Favorite Professors

#### Frontend

(Needs to be made) ./components/Favorites.tsx

- [ ] highlight nav buttons for course first time 
- [ ] add heart button by proffesor both on search (Home.tsx) and on their "professor" page (Professor.tsx)
  - [ ] make heart togglable which adds and removes from the users favoriteProfessors list
- [ ] on the home search, make the list of defaults the professor list if there is nothing in the search bar
- [ ] add favorite professors page and link to nav (see other pages for example)

### Backend

localhost:8080/favorites

- [ ] update corresponding user list (PUT)
  - Only store professor name, we can do a query for that professor later if need be
- [ ] upgrade heroku once app is deployed
