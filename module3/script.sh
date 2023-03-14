#!usr/bin/bash

pylint decoder.py --output-format=json --output=pylint_result.json
pylint_res=$?

if [[ pylint_res -eq 0 ]]; then
	tests=`python3 -m unittest`
else
	echo "Error"
fi

exit 0