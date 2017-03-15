export MARY_BASE=/home/murtraja/Downloads/marytts_downloads/releases/marytts-5.2

java -showversion -Xms40m -Xmx1g -cp "$MARY_BASE/lib/*" -Dmary.base="$MARY_BASE" -Dsocket.port=59126 $* marytts.server.Mary