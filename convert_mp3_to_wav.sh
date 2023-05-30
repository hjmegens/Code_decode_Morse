MP3S=`ls Morse_cursus/Music/*.mp3`
i=0
for MP3 in $MP3S; do echo $MP3; ((i+=1)); ffmpeg -i $MP3 -ar 44100 Morse_cursus_wav/Morse_les_${i}.wav; done

