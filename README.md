# Cluster and Cloud Computing Assignment 2 Group 1
# Melbourne the Most Liveable City...?

## Introduction:

This is a scalable distributed system that gathers data from Twitter API or CSV file, processes the data through MapReduce and presents the visualised data in a graph/map through a web interface.

## Members:

Qianjun Ding

Zhiyuan Gao

Jiachen Li

Yanting Mu

Chi Zhang


## System Repositories

Ansible: Contains files for deploying the whole system onto Melbourne Research Cloud and start / end the system

Data: Contains json / csv files which are downloaded from Aurin Portal / Dropbox, is need for future data analysis

frontend: Contain codes for building up the frontend of this system

node_modules: required packages for building up the frontend

Gateway: Include codes for setting up the Gateway node for managing the whole system and direct response to the frontend request

Worker: Include codes for creating database with the harvested data based on the requirement got from the Gateway node’s task list
