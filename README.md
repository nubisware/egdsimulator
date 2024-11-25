# EGD Simulator

## Introduction

Ethernet Global Data (EGD) is a mechanism that enables one CPU, referred to as a producer, to
share a portion of its internal reference memory with one or more other CPUs, referred to as
consumers, at a regularly scheduled periodic rate. Such a snapshot of internal reference
memory, mediated by an Ethernet interface, is referred to as an exchange. An exchange is
identified by a unique combination of three identifiers:
• The Producer ID (the producer's IP address)
• The Exchange ID (the exchange's identifier)
• The Adapter Name (the Ethernet interface identifier) 

The EGD protocol is used in many contexts of Industrial monitoring and control and is backed by GE. 

Please refer to http://geplc.com/downloads/Labs/GFS-384%20M09%20EGD.pdf for further information.
> **The offical link is no more available** you can refer to [the last version available](https://web.archive.org/web/20180219025736/http://geplc.com/downloads/Labs/GFS-384%20M09%20EGD.pdf) on the [Wayback Machine - Internet Archive](https://web.archive.org)

## EGD Simulator

Our EGD Simulator is an effort to create a software that simulates typical EGD producers that can be found as control hardware like for example [Mark VI e (C)](http://www.geautomation.com/products/mark-vie) created by GE Automation (R).

EGD Simulator is a Python 2.7 and 3.x program with a web frontend.

Once the software is installed it can be executed with the command from a command line prompt:

```
python egdsimulator_http.py
```
At that point, opening a browser and pointing to the address *http://localhost:8000* is sufficient to get to the configuration interface.

It is also possible to change the port of the configuration interface. In order to do so the simulator has to be started with the following command line:

```
python egdsimulator_http.py -p NEWPORT
```
From the configuration interface it's possible to upload a CSV representing the setup of the simulator. Currently the simulator supports the CSV format obtained from exporting a setup from the MARK VI e control software. In addition, a simplified CSV format that contains only the four relevant information fields for every tag can be uploaded.

Two example files for both formats are supplied in the _resource_ folder.

Separator and initial number of lines to be skipped for the CSV parser may be specified before uploading.

Example MARK VI export format is:

```
#(V05.02.04C) EGD Point List Report for example,,,,,,,,,,,,,,,,
Entry No,Variable,Point Name,Point Offset,Direction,Data Type,CIMPLICITY Resource,Units,Producer ID,Period(ms),Exchange Name,Destination,Description,Alias,Second Language Description,Path,Format Specification
617,FAKEBOOL1,EGD.ProducedPages.FastEGD.Exchange3.Point_23,03.0003.1,ReadOnly,BOOL,,nd,1701122220,10,Exchange3,172.16.111.255,fake bool 1,,,System:PTT_1609256_59|Device:T1|EGD:|EgdPageList:ProducedPages|EgdPage:FastEGD|EgdExchange:Exchange3|EgdVariable:a,N_D
618,FAKEBOOL2,EGD.ProducedPages.FastEGD.Exchange3.Point_23,03.0003.2,ReadOnly,BOOL,,nd,1701122220,10,Exchange3,172.16.111.255,fake bool 2,,,System:PTT_1609256_59|Device:T1|EGD:|EgdPageList:ProducedPages|EgdPage:FastEGD|EgdExchange:Exchange3|EgdVariable:b,N_D
619,FAKEREAL1,EGD.ProducedPages.FastEGD.Exchange3.Point_30,03.0032.0,ReadOnly,REAL,,lb/hr,1701122220,10,Exchange3,172.16.111.255,fake real 1,,,System:PTT_1609256_59|Device:T1|EGD:|EgdPageList:ProducedPages|EgdPage:FastEGD|EgdExchange:Exchange3|EgdVariable:c,PPH
620,FAKEREAL2,EGD.ProducedPages.FastEGD.Exchange3.Point_31,03.0036.0,ReadOnly,REAL,,,1701122220,10,Exchange3,172.16.111.255,fake real 2,,,System:PTT_1609256_59|Device:T1|EGD:|EgdPageList:ProducedPages|EgdPage:FastEGD|EgdExchange:Exchange3|EgdVariable:d,
627,FAKEDINT,EGD.ProducedPages.FastEGD.Exchange3.Point_40,03.0072.0,ReadOnly,DINT,,nd,1701122220,10,Exchange3,172.16.111.255,fake dint,,,System:PTT_1609256_59|Device:T1|EGD:|EgdPageList:ProducedPages|EgdPage:FastEGD|EgdExchange:Exchange3|EgdVariable:e,N_D
649,FAKEINT,EGD.ProducedPages.FastEGD.Exchange3.Point_23,03.0004.0,ReadOnly,INT,,nd,1701122220,10,Exchange3,172.16.111.255,fake int,,,System:PTT_1609256_59|Device:T1|EGD:|EgdPageList:ProducedPages|EgdPage:FastEGD|EgdExchange:Exchange3|EgdVariable:f,N_D
1334,FAKEUDINT,EGD.ProducedPages._Status.Exchange1.Point_464,01.0292.0,ReadOnly,UDINT,,,1701122220,250,Exchange1,172.16.111.255,fake udint,,,System:PTT_1609256_59|Device:T1|EGD:|EgdPageList:ProducedPages|EgdPage:_Status|EgdExchange:Exchange1|EgdVariable:g,
1498,FAKEUINT,EGD.ProducedPages._Status.Exchange1.Point_400,01.0060.0,ReadOnly,UINT,,,1701122220,250,Exchange1,172.16.111.255,fake uint,,,System:PTT_1609256_59|Device:T1|EGD:|EgdPageList:ProducedPages|EgdPage:_Status|EgdExchange:Exchange1|EgdVariable:h,

```

Example simplified CSV format is:

```
Producer,Exchange,Address,Type
1,01,0000.0,UINT
1,01,0002.0,UINT
1,01,0004.0,UINT
2,03,0000.1,BOOL
2,03,0000.2,BOOL
2,03,0010.0,UINT
```
Once the setup CSV has been uploaded the simulator can be started through the play button and paused through the pause button.

It is possible to upload a different CSV while the simulator is running. This just changes the layout of the tags but keeps the simulator going.

When the simulator is in paused mode, it's possible to change the value generation policy to _fixed_. This forces the simulator to generate always the same value for each tag. If _fixed_ is not set, random values will be generated according to the tag type.

It is also possible, in paused mode, to change the UDP address to which the simulator publishes the Exchange values.

In order to overview the EGD structure and the values produced by the simulator, the web page shows a table with all Producers, Exchanges, Tags and generated values.

In order to see the changes in the readings it's just sufficient to reload the webpage. 

## Version

Version 0.5
