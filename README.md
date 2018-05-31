[![Build Status](https://travis-ci.org/deadlock-delegate/arkdelegates.svg?branch=master)](https://travis-ci.org/deadlock-delegate/arkdelegates)

## ARK delegates

MVP for listing all ARK delegates. As soon as some of the basic functionality is proven to be useful
to both visitors and delegates I'll start working on a more proper version which will primarily
change the frontend code.

Visit project: https://arkdelegates.io

## How to run project locally?

You'll need Docker, node and npm install locally. To build the whole project you'll have to:
1. run `make build` which will build the docker image along with all the npm packages that you'll
need (might take a while for it all to complete ⏲)
2. run `make start` to start the project

After starting the project for the first time and visiting the website you won't have any
information available. To populate your database run:
1. `make syncdelegates` which will insert all registered delegates into db
2. `make updatestats` which will update all the stats for all delegates (current rank, voting power
etc.)


## Support this project

- By voting for `deadlock` delegate on ARK
- By donating to the following ARK address: APEJtGcYY7pbA5RdPn43A982Sw3cxr5Y7m
