# tlsrpt_processor


## TLSRPT Processor

This is a small python script that is meant to be able to process TLSRPT reports.  The script currently only outputs to CSV and key/value pairs.

```
This script should process a TLSRPT JSON file pass as an argument
Options are as follows:
-h                              Show this help message
-i/-input                       Input file
-o/-output-style                Output Style (values: kv,csv)
```

As of July 2018, the script will not directly handle zipped reports, but I've created an issue to track that.
