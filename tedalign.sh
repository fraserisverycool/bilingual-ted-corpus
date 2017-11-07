for i in $( ls ../outputcorpus/ ); do
	echo $i
	src/hunalign/hunalign data/hu-en.dic ../outputcorpus/$i/tedcorpus."$i".de ../outputcorpus/$i/tedcorpus."$i".ko -text >../outputcorpus/$i/tedcorpus."$i".align
done
