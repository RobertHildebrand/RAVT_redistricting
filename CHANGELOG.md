## 0.2.1 (2020-05-13)

### Features

- Added the ability to abort a run via Ctrl+C.  Doing so will skip that iteration and move on to the next one; it's intended to use when a run simply isn't completing.  

## 0.2.0 (2020-04-30)

### Features

- Added the ability to write summary to CSV file

### Bugs

- Timeout function never quite seems to find a new better seed after timing out
- Needed to drop initial partition by 0.001 population tolearance to make sure it generates starts that are solidly within the criteria

## 0.1.0 (2020-04-23)

Initial commit.  This is the basic functionality, but needs a lot of work

### Features

- Accepts json or shapefile geometries
- Accepts additional data fields via CSV file
- Has polsby popper, black representattives, and mixed optimization functions
- Has controls for setting steps, runs, and other basic control information

