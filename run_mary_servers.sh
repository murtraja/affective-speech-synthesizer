if [ "$#" -eq 0 ];then
	echo "please enter the MARY_BASE as a command line argument"
else
	export MARY_BASE=$1
	gnome-terminal -e "bash mary-server/p59125.sh"
	gnome-terminal -e "bash mary-server/p59126.sh"
	gnome-terminal -e "bash mary-server/p59127.sh"
	gnome-terminal -e "bash mary-server/p59128.sh"
fi
