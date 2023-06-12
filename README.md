# csv visualization tool
## functionality
* assumes csv files with data in timesteps as columns
    * one header line which describes every field
* buttons to internally delete all opened data or open a new additional csv file

<img src="https://i.ibb.co/nrbvr1H/screenshot-csvviz.png" width="580" height="324" />

## features in config.py
* usage: copy *config_boilerplate.py* or *config_intelligent_energy.py* as *config.py* and set desired values
* *path*: possibility to set path (will be also written automatically if you choose one), which always will be opened.
    * make sure to use raw strings or single qotes `'`
* *lineno_header_data*: set linenumber from which the header data is read
* *no_headerlines_ignore*: number of header lines that will be ignored (>0, has to include the header itself)
* *x_axis_field*: specify which field to use as x-axis values (most likely time)
* *delimiter*: delimiter used in csv
* *unwanted_keys*: specify an array of keys, that will not be selectable in the gui (for non-numeric fields, etc)
* *lineskipper*: give generator to `np.genfromtxt()`
    * basic: `lambda file: (line for line in file)`
    * be aware: all lines filtered here have to be subtracted from *lineno_header_data* and *no_headerlines_ignore*

* *lambdadict*: if the key is matches, will apply the function to all the data
    * used to invert etc

## example configs:
### basic boilerplate (to be used with files in *example/*)
```python
path = ''

lineno_header_data = 0
no_headerlines_ignore = 1
x_axis_field="time"
delimiter=","
unwanted_keys=[]
lineskipper = lambda file: (line for line in file)

lambdadict={
    'key1': lambda x: -x
}
```

### intelligent energy fuelcell logs (to be used with files in *example_ie/*)
```python
path=''

lineno_header_data=0
no_headerlines_ignore=1
x_axis_field="Time [s]"
delimiter=","
unwanted_keys=["D Type", "Stack Temperature #2 (mean) [degC]", "OVOC Fault DI High [-]","DCDC Fault DI High [-]","Fault Code (word1)","Button #1 + #2","Safety Circuit Safety #1 + #2"]

def lineskipper(file):
    for line in file:
        if line[0] == 'E' or line[0] == 'N':
            continue
        yield line

lambdadict={}
```