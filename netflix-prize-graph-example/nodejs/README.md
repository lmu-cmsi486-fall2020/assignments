# A Node.js DAL Using the [Official Neo4j JavaScript Driver](https://neo4j.com/developer/javascript/)

## Installation and Setup
Due to its relative simplicity—and to make the library dependencies more explicit—the Node.js DAL example doesn’t come with a _package.json_. Instead, you can install the needed libraries directly within [this folder](.):

    cd nodejs # Within this repository
    npm install neo4j-driver

In order to use the more modern [`import`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/import) syntax for ECMAscript modules without relying on _package.json_, the provided source code [ends in _.mjs_ and not plain _.js_](https://nodejs.org/api/esm.html#esm_enabling). When “graduating” this sample code to a bona fide DAL package, feel free to include the requisite `type` property in _package.json_ [as documented here](https://nodejs.org/api/packages.html#packages_type).

The sample DAL programs here also use a feature called _top-level `await`_. This is the ability to `await` promise results at the top scope of a program, outside of an `async` function. It’s supported by Node.js versions 14.8 and above.

## Running the Examples
The reusable DAL code itself is in _netflix-dal.mjs_. The general pattern for invoking the accompanying programs is:

    DB_URL=<database URL> DB_PASSWORD=<Neo4j user password> node <program name> <arguments>

So, running _add-movie.mjs_ for a database server on your local machine would look like this:

    DB_URL=neo4j://localhost DB_PASSWORD=thisfeelsweird node add-movie.mjs "Bill & Ted Face the Music" 2020

As noted in the overall [README](../README.md), if supplying the password on the command line like this is unnerving, you can set the `DB_PASSWORD` environment variable through other common mechanisms.

Note the use of double-quotes to delimit the first title argument so that the title’s spaces don’t break that argument into multiple ones. Double-quotes also help with symbols that have other meanings on the command line, such as the `&`. The I/O redirection symbols `<`, `>`, `|`, etc. also belong to this category.

For fun, I tried to make the output of the Python and Node.js programs indistinguishable, to drive home the point that the underlying language shouldn’t necessarily limit the visible interface of the end-user program.
