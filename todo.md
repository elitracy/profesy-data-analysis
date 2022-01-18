# TODO LIST

## User Accounts

#### Backend:

- [x] encrypt passwords right when they submit them
  - they should not leave the front end without being encrypted
  - js-sha256 library already imported

---

## Sign Up

#### Frontend:

<sup>./components/Signup.tsx

- [x] link parameters in RootStackParams.ts
- [x] add component to App.tsx
- [x] navigate from login (LandinPage.tsx)
- [x] send fetch (PUT) request to backend

#### Backend:

<sup> localhost:8080/signup

- [x] parse arguments (req.query.x)
- [x] check for other users with same username or email
  - [x] send back fail message and tell user to pick another username/ email upon fail
- [x] on sign up succeed
  - [x] update database (insertOne) -> params are listed out in function in Signup.tsx (username, pass, email, name, favProfs[])
  - [x] insert empty favorite profs list
- [x] AsyncStorage.setItem("name", name that was entered)

---

## Favorite Professors

#### Frontend

<sup>(Needs to be made) ./components/Favorites.tsx

- [ ] add heart button by proffesor both on search (Home.tsx) and on their "professor" page (Professor.tsx)
  - [ ] make heart togglable which adds and removes from the users favoriteProfessors list
- [ ] on the home search, make the list of defaults the professor list if there is nothing in the search bar
- [ ] add favorite professors page and link to nav (see other pages for example)
- [ ]

### Backend

<sup> localhost:8080/favorites

- [ ] update corresponding user list (PUT)
  - Only store professor name, we can do a query for that professor later if need be
