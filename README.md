# Prerequisites

## Python 3
NLTK (and the german.pickle model)
lxml

## Hunalign: http://mokk.bme.hu/en/resources/hunalign/
Put the hunalign-1.1 folder into this directory, and move the "tedalign.sh" script into it.

# Usage

1. Download search URLs from TED website containing German-Korean TED talks

`cd htmls
./download_ted_urls.sh`

2. Extract TED talk URLs from these search files and compile a list

`python3 compile_url_list.py`

3. Download HTMLs of TED talks from list

`cd crawlhtmls
./download_htmls.sh`

4. Extract sentences from TED talks

`python3 tedcrawl.py`

5. Align the sentences with hunalign - remember to move "tedalign.sh" into the correct directory

`cd hunalign-1.1
./tedalign.sh`

6. Use the results of the alignment to generate the final corpus

`python3 tedaligned.py`