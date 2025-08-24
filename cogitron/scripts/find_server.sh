ip_prefix="Nmap scan report for "


if [[ -z $@ ]]; then
    echo "Missing input argument. Please insert ip addresses to scan. E.g: 10.22.20.94/22"
    exit 128
fi

ip_adresses=`nmap $@ -p 22 --open | grep "$ip_prefix" | grep "dhcp"`


ip_adresses=${ip_adresses//$ip_prefix/\\n}
ip_adresses=${ip_adresses/\\n}

ip_adresses=`echo -e $ip_adresses | sed 's/^.*(//' | sed 's/).*//'`

sudo nmap $ip_adresses -O

#nmap $ip_adresses --script ssh-hostkey --script-args ssh_hostkey='full' known_hosts='~/.ssh/known_hosts'

#ip_adresses=`$ip_adresses | sed -n -e 's/^.*stalled: //p'`