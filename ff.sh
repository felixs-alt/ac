wget https://cloud.oscie.net/acdp/acnh/$1/$2.mp3
mv ./$2.mp3 ./main.mp3
ffmpeg -i ./main.mp3 -listen 1 -method GET -c copy -f MP3 http://0.0.0.0:5000/main.mp3