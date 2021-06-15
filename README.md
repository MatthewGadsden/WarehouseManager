# Warehouse Managment System

A Warehouse Management System tool used to automate the creation of custom work orders for warehousing staff, as well as reports on the 
current state of the warehouse and product lines in it. 

This app was made to be used with a [WISE Warehouse System](http://www.wisesystems.com.au/index.htm) and uses files exported directly from this system.

## Setup and Use

### Setup (with demo warehouse)
1) Locate the most recent stable tag (non pre-release version)
2) Download and extract zip
3) Run the .exe

### Use (with own WISE warehouse)
1) Run the .exe (see setup)
2) File -> New Warehouse 
3) Add four report files (Downloaded from WISE export)
4) Click create
5) Your warehouse reports will be imported and saved

![NewWarehouse Popup Picture](https://i.imgur.com/6agSXxd.png)

## Control Panel (Main Screen)
Here users are given a customisable display of useful warehouse information (displayed in a widget style).

> Widget Examples:
> - Warehouse Capacity Display
> - Aisle Capacity Display
> - Best Items List
> - Best Aisle Display
>
> ![Warehouse Capacity Display](https://i.imgur.com/Q96NQDh.png) ![Aisle Capacity Display](https://i.imgur.com/v4APKPj.png)  
> ![Best Items List](https://i.imgur.com/9aD0Z0S.png) ![Best Aisle Display](https://i.imgur.com/4SelfEq.png)

Users can also access the Apps located in the bar above the control panel widgets, and tools via the toolbar options.

Apps Available:
- Distro App
- Consolidation App
- Warehouse Relay App
- Slot Allocation App

## Distro App

The Distro App is for setting up a custom distro picking area for the picking of very large orders of product. These types of orders are 
ones that wouldn't be able to be picked with the normal picking setup that the warehouse uses.

How to use:

1) Upload a file containing items and the quantity to be picked in the order(s)
2) Select an Area (These can be edited in the `Edit -> Warehouse Areas` option of the toolbar).<br/>
  This is where the distro will be laid out.
3) Select where to export the output.
4) Run the distro

![Distro App](https://i.imgur.com/C7aLFYS.png)

## Consolidation App

The Consolidation App is for consolidating reserve slot pallets, this is to free up space for new stock. It determines which pallets in an aisle can be consolidated together (in groupings of 2's and 3's) and then exports a work order into an excel sheet (split by grouping #)

How to use:

1) Select aisle to consolidate
2) Run consolidation
3) Open the exported work order file

![Consolidation App](https://i.imgur.com/llgtuTA.png)

> #### Extra Functions:
> Print Report: This prints a report of how many consolidations there are per aisle in the warehouse

## Warehouse Relay App

The Warehouse Relay App is for relaying a specific category of items into a selected area. It will export a work order to move items in a category into a efficient position within the area (the efficient position calculation can be changed within the code to fit specific needs).

How to use:

1) Select a category of items to relay
2) Select the area you want to relay the items into
3) Select the overflow area (this doesn't matter so much, just can't be the same as first area)
4) Enter / Select where to export the work order file
5) Open work order file

![Warehouse Relay App](https://i.imgur.com/Sl6cT1d.png)

## Slot Allocation App

The Slot Allocation App is used to create a word order for swapping slots, so then all items are on their ideal level (high hitting products should be on levels 2 or 3, waist height).

How to use:

1) Select which area you want to create the slot swap work order for
2) Hit 'Sort' to run the swapping process
3) Open the created work order

![Slot Allocation App](https://i.imgur.com/Xgm15rV.png)

> #### Extra Functions
> Print Report: Report of how many slots each area has
