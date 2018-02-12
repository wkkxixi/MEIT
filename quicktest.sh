#!/bin/bash
mkdir -p test_data;
export TESTIMGZIP=./test_data/test.tif.zip;
export TESTIMG=./test_data/test.tif;
export TESTURL=https://s3-ap-southeast-2.amazonaws.com/rivulet/test.tif.zip;
export OUT=$TESTIMG.r2.swc;
if [ ! -f $TESTIMG ];
then
  rm -rf test_data/*;
  echo "Downloading test image from $TESTURL";
  wget -P ./test_data/ $TESTURL;
  unzip $TESTIMGZIP -d ./test_data;
fi

python3 meit_single.py --file $TESTIMG   -v;

echo "== Done =="