# WELF Log Parser

## Log format

~~~
date=2020-02-24 time=13:53:08 logid=0000000013 type=traffic subtype=forward level=notice vd=root srcip=192.168.5.7 srcport=47613 srcintf="port1" dstip=94.75.204.214 dstport=80 dstintf="port2" sessionid=9551 status=close user="John" group="John" policyid=4 dstcountry="Netherlands" srccountry="Reserved" trandisp=noop service=HTTP proto=6 applist="default" duration=11 sentbyte=1140 rcvdbyte=32376 sentpkt=25 rcvdpkt=44 identidx=1 utmaction=passthrough utmevent=webfilter utmsubtype=ftgd-cat urlcnt=1 hostname="www.simpledomain.local" catdesc="File Sharing and Storage"
~~~

## Usage

Extract specific fields:

~~~
$ welf.py output.log date,srcip,dstip,hostname,catdesc
date=2020-02-24 srcip=192.168.5.7 dstip=94.75.204.214 hostname="www.simpledomain.local" catdesc="File Sharing and Storage"
~~~

Pass data from stdin:

~~~
$ cat output.log | welf.py --format=csv date,srcip,dstip,hostname,catdesc
2020-02-24,192.168.5.7,94.75.204.214,"www.simpledomain.local","File Sharing and Storage"
~~~

Output as CSV :

~~~
$ welf.py --format=csv output.log date,srcip,dstip,hostname,catdesc
2020-02-24,192.168.5.7,94.75.204.214,"www.simpledomain.local","File Sharing and Storage"
~~~