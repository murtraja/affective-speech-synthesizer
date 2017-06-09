#!/bin/bash

echo "Starting Mary servers..."
export MARY_BASE="/home/pranjal/marytts-5.2/target/marytts-5.2/"
export PROJECT_PATH="/home/pranjal/BE_PROJECT/affective-speech-synthesizer"
gnome-terminal -e "bash $PROJECT_PATH/mary-server/p59125.sh"
gnome-terminal -e "bash $PROJECT_PATH/mary-server/p59126.sh"
gnome-terminal -e "bash $PROJECT_PATH/mary-server/p59127.sh"
gnome-terminal -e "bash $PROJECT_PATH/mary-server/p59128.sh"
echo "Successfully spawned Mary servers"

echo "Starting LSTM server..."
sudo gnome-terminal -e "python $PROJECT_PATH/lstm.py"
echo "Successfully spawned LSTM server"

echo "Starting GUI..."
python $PROJECT_PATH/qtmain.py
echo "Good Bye"
