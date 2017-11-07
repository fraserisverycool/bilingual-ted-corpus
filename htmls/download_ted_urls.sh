#!/bin/bash
for i in `seq 1 67`;
	do
		wget "https://www.ted.com/talks?language=ko&page=$i&sort=newest"
	done 
