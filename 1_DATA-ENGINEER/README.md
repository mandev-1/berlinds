## BEING A DATA ENGINEER

(wrangle and cleanse)

For this exercise, you can use PostgreSQL directly if it is installed on your campus
machine or on a VM. Otherwise, you must use Docker Compose.
• The username must be your student login.
• The name of the database must be piscineds.
• The password must be mysecretpassword.

We must be able to connect to your PostgreSQL database with the following command:
psql -U your_login -d piscineds -h localhost -W
mysecretpasswor

If you choose to use Docker, your setup must follow the same
standards and good practices as required in the Inception project.

-------------------

> INCEPITON PROJECT STANDARDS:
Each Docker image must have the same name as its corresponding service.
Each service has to run in a dedicated container.
For performance reasons, the containers must be built from either the penultimate stable
version of Alpine or Debian. The choice is yours.
You also have to write your own Dockerfiles, one per service. The Dockerfiles must
be called in your docker-compose.yml by your Makefile.
This means you must build the Docker images for your project yourself. It is then forbidden to pull ready-made Docker images or use services such as DockerHub (Alpine/Debian
being excluded from this rule).

This project must be completed on a Virtual Machine.
• All the files required for the configuration of your project must be placed in a srcs
folder.

• A Makefile is also required and must be located at the root of your directory. It
must set up your entire application (i.e., it has to build the Docker images using
docker-compose.yml).


###### RUNNING LOCAL TESTS ON MACOS

1. start the app with:
brew services start postgresql

1b. access it with
psql postgres

2. create the DB named piscineds
CREATE DATABASE piscineds;

3. setup user (create and give privileges)

x...x..
GRANT ALL PRIVILEGES ON DATABASE piscineds TO mman;


4. login to the db
psql -U mman -d piscineds -h localhost -W mysecretpassword


###### VISUALIZATION ON MACOS / WINDOWS / LINUX

TO visualize the data, I chose DBeaver software, available at:
https://dbeaver.com/docs/dbeaver/Basic-operations/#database-navigator

