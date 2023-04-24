#!/bin/bash

file=${1##*/}

filter=/home/arinov/projects/rnnoise-models/marathon-prescription-2018-08-29/mp.rnnn

echo "$(date +%T.%3N) Copy source video to temporary working directory."
mkdir -p $1.rnn
cp $1 $1.rnn/${file}

echo "$(date +%T.%3N) Extracting AAC from source video." \
&& ffmpeg \
  -y \
  -i $1.rnn/${file} \
  -vn \
  -acodec copy $1.rnn/${file}.aac \
  2> $1.rnn/1-extract-aac.log \
&& echo "$(date +%T.%3N) Processing RNN filter to extracted AAC data." \
&& ffmpeg \
  -y \
  -i $1.rnn/${file}.aac \
  -af arnndn=m=${filter} \
  $1.rnn/${file}-rnn.aac \
  2> $1.rnn/2-processing-rnn-aac.log \
&& echo "$(date +%T.%3N) Replacing original AAC with RNN-processed audio." \
&& ffmpeg \
  -y \
  -i $1.rnn/${file} \
  -i $1.rnn/${file}-rnn.aac \
  -c:v copy \
  -map 0:v:0 \
  -map 1:a:0 \
  $1.rnn/rnn-${file} \
  2> $1.rnn/3-insert-rnn.log \
&& echo "$(date +%T.%3N) Processing complete. Log files are in working directory." \
&& mpv $1.rnn/rnn-${file} &
wait

echo "You can close this window now."
