# csv visualization tool
## functionality
* assumes csv files with data in timesteps as columns
    * one header line which describes every field, first one being the time step, named time
* buttons to internally delete all opened data or open a new additional csv file

## features in config.py
* usage: copy __config_boilerplate.py__ as __config.py__ and set desired values
* possibility to set path (will be also written automatically if you choose one), which always will be opened
* give a __lambdadict__ which if the key is equal, will apply the function to all the data, to invert etc
