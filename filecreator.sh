#!/bin/bash
x=1
while [ $x -le 17 ]
do
  touch Charlse_Darwin/"module$x.txt"
  x=$(( $x + 1 ))
done