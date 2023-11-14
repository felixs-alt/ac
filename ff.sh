cd ./files
wget https://cloud.oscie.net/acdp/acnh/$1/$2.mp3
cd ..
mv ./files/$2.mp3 ./main.mp3
rm ./files/*
ffmpeg -i ./main.mp3 -listen 1 -method GET -c copy -f MP3 http://0.0.0.0:5000/main.mp3