# A Node.js DAL Using [Sequelize](https://sequelize.org/master)

## Installation and Setup
Due to its relative simplicity—and to make the library dependencies more explicit—the Node.js DAL example doesn’t come with a _package.json_. Instead, you can install the needed libraries directly within [this folder](.):

    cd nodejs # Within this repository
    npm install sequelize
    npm install pg pg-hstore

In order to use the more modern [`import`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) syntax for ECMAscript modules without relying on _package.json_, the provided source code [ends in _.mjs_ and not plain _.js_](https://nodejs.org/api/esm.html#esm_enabling). When “graduating” this sample code to a bona fide DAL package, feel free to include the requisite `type` property in _package.json_ [as documented here](https://nodejs.org/api/packages.html#packages_type).

## Running the Examples
The reusable DAL code itself is in _netflix-dal.mjs_. Similarly to the Python example, it has four functions, also implemented using the range of styles available in Sequelize. For comparison purposes, ORM examples from the Python DAL are implemented in the opposite manner here, and vice versa for raw SQL. The general pattern for invoking these programs is:

    DB_URL=<database URL> node <program name> <arguments>

So, running _add-movie.mjs_ for a database server on your local machine would look like this:

    DB_URL=postgres://localhost/postgres node add-movie.mjs "Bill & Ted Face the Music" 2020

Note the use of double-quotes to delimit the first title argument so that the title’s spaces don’t break that argument into multiple ones. Double-quotes also help with symbols that have other meanings on the command line, such as the `&`. The I/O redirection symbols `<`, `>`, `|`, etc. also belong to this category.

For fun, I tried to make the output of the Python and Node.js programs indistinguishable, to drive home the point that the underlying language shouldn’t necessarily limit the visible interface of the end-user program.
