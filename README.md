# p1data-parser

Parser to convert raw P1 data (from a logfile source) into readable CSV files

### Usage
The script can convert a single logfile:
```
$ ./smart_raw.py -f input_file
```
But it can also convert all files in a folder
```
$ ./smart_raw.py -d input_dir
```
**Note:** when analysing a directory, the script will try to parse all files found with `os.listdir`. For some files, the script might produce empty CSV files. This 'bug' might be removed in a future update. 

### Required input data
The script uses data of the following form (written in some text file):
```
/KFM5KAIFA-METER

1-3:0.2.8(42)
0-0:1.0.0(160826110040S)
0-0:96.1.1(XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX)
1-0:1.8.1(000753.455*kWh)
1-0:1.8.2(000678.858*kWh)
1-0:2.8.1(000000.000*kWh)
1-0:2.8.2(000000.000*kWh)
0-0:96.14.0(0002)
1-0:1.7.0(00.132*kW)
1-0:2.7.0(00.000*kW)
0-0:96.7.21(00011)
0-0:96.7.9(00008)
1-0:99.97.0(1)(0-0:96.7.19)(000101000001W)(2147483647*s)
1-0:32.32.0(00000)
1-0:32.36.0(00000)
0-0:96.13.1()
0-0:96.13.0()
1-0:31.7.0(000*A)
1-0:21.7.0(00.132*kW)
1-0:22.7.0(00.000*kW)
0-1:24.1.0(003)
0-1:96.1.0(XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX)
0-1:24.2.1(160826100000S)(00417.124*m3)
!
```

### Parser options
If you want to add/remove/sort columns, modify the `parser.json` file which specifies all columns of the CSV file. 
