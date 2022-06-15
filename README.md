# Instructions
## Docker commands

* ``` docker build -t log-analyzer . ```
* ``` docker run --rm -it log-analyzer bash ```

## Docker container

Once in the container the ``` workdir``` has been defined as ```/app``` (See ```Dockerfile```), in which the tool can be triggered.

* ``` python3 analyzer.py -p access.log -m -l -e -b -o json_output ```

    * ``` -p ``` Path to log file
    * ``` -m ``` Most frequent IP
    * ``` -l ``` Least frequent IP
    * ``` -e ``` Events per second
    * ``` -b ``` Total amount of bytes exchanged
    * ``` -o ``` file name to save output in JSON format