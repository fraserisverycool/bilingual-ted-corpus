#!/bin/bash
for i in ` cat ../koreanurls.txt `;
	do
		wget "https://www.ted.com$i/transcript?language=de" && wget "https://www.ted.com$i/transcript?language=ko"
	done