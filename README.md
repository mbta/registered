# Registered

A set of scripts for working with TransitMaster. Reference the rating process documentation [here](https://github.com/mbta/wiki/blob/master/transit_tech/Procedures/TransitMaster/TM-03_Make_Updates.md). 

**Effect:**	Different steps throughout the rating process. Allows data validation before importing into TransitMaster.
**Circumstances:**	As needed. Generally once per quarterly rating.  
**Required Skills:**	None  
**Required Tools:**	VPN access, a text editor, access to TM databases 

## Setup

Reminder: Before the set-up process, clone the registered repository and direct to it. 

### Linux/MacOS
```
$ brew install proj freetds
$ asdf install
$ asdf reshim
$ pip install pipenv
$ pipenv install  # --dev if you want to do development on the scripts
```

### Windows
```
$ choco install pyenv-win
$ pyenv install
$ pyenv rehash
$ pip install pipenv
$ pipenv install  # --dev if you want to do development on the scripts
```

## Scripts 

For the scripts below, you will have to access the rating files, found on different TM servers, on your local machine to direct it to the right path. If you're working from a PC computer, you are all set. If you're working from a MAC, follow the instructions below. 

### Linux/MacOS
- From your MAC, open finder
- Click 'Go' 
- Click 'Connect to Server' 
- Type 'smb://HSTMTEST01/c$/Ratings' 
- Access the files at '/Volumes/Ratings/[Rating]' (i.e. /Volumes/Ratings/Winter12202020) 

## HASTUS sync_hastus

Sync a HASTUS export to the TransitMaster server, validating the data in the process.

- Writes the data to `support/ratings/*` for later processing if needed.
- Will prompt for your AD password, or you can put it in the `AD_PASSWORD` environment
  variable.

```
$ pipenv run hastus_sync (if testing, use "—no-push" to avoid actually updating the rating data on the TM server)
```

## Merge

Merge a set of rating files together in the Combine directory. This step is found under step 2 in [TM-03.05: Production Import, Merge, and Route Splitting](https://github.com/mbta/wiki/blob/master/transit_tech/Procedures/TransitMaster/TM-03_Make_Updates.md) 

Writes the merged files to `<rating>.pat`, `<rating>.nde`, &c.

```
$ pipenv run merge <path to Rating/Combine>
```

## Validate

Validate that the rating files are correct. This step is found under step 4 (Integrity Checker) in [TM-03.05: Production Import, Merge, and Route Splitting](https://github.com/mbta/wiki/blob/master/transit_tech/Procedures/TransitMaster/TM-03_Make_Updates.md) 

Exits with 1 if there were any errors.

```
$ pipenv run validate <path to Rating/Combine or Rating/Combine/HASTUS_export>
```

## Calendar

Print a CSV which has the service information for each garage, by date. This step is meant to help facilitate step 7 in [TM-03.05: Production Import, Merge, and Route Splitting](https://github.com/mbta/wiki/blob/master/transit_tech/Procedures/TransitMaster/TM-03_Make_Updates.md) 

```
$ pipenv run calendar <path to Rating/Combine or Rating/Combine/HASTUS_export>
```

## Stop Comparison

Print a CSV which shows new/changed stops between two ratings. This step is found under step 1 in [TM-03.06: Map Changes](https://github.com/mbta/wiki/blob/master/transit_tech/Procedures/TransitMaster/TM-03_Make_Updates.md) 

- Copy .env.template to .env and fill out at least the first three variables with the TransitMaster DB server information from 1Password.
```
$ pipenv run stop_comparison <path to current Rating/Combine> <path to next Rating/Combine>
```
