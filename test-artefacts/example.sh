#!bin/bash
URL=https://totosan-studious-computing-machine-ggvpvqpxq2v597-3500.preview.app.github.dev/resize
FILENAME=GlobalAzurePic.jpeg
curl -F "image=@${FILENAME}" -F "size=400" $URL -o outputFile.png
