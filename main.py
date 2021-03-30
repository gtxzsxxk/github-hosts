import requests

domain_set=['raw.githubusercontent.com','github.githubassets.com','github.com','avatars.githubusercontent.com','github.global.ssl.fastly.net']
hosts=[]

for i in domain_set:
    domain_arr=i.split('.')
    len=domain_arr.__len__()
    secfirstdomain=domain_arr[len-2]+"."+domain_arr[len-1]
    request_Url="https://%s.ipaddress.com/%s"%(secfirstdomain,i)
    if len==2:
        request_Url="https://%s.ipaddress.com/"%secfirstdomain
    print(request_Url)
    response=requests.get(request_Url)
    res_html=response.text
    ipaddr=""
    if "IPv4 addresses:" in res_html:
        basekey="<h2>Frequently Asked Questions (FAQ)</h2>"
        tostartindex=res_html.find(basekey)
        bgkey="IPv4 addresses:"
        endkey="</ul></div>"
        target_begin=res_html.find(bgkey,tostartindex)+bgkey.__len__()
        target_end=res_html.find(endkey,target_begin)
        tosearch=res_html[target_begin:target_end]
        while True:
            index=tosearch.find('/ipv4/')
            if index==-1:
                break
            end=tosearch.find("\">",index,index+30)
            ipaddr=tosearch[index+6:end]
            print(ipaddr)
            tosearch=tosearch[end:tosearch.__len__()]
            hosts.append((ipaddr,i))
            
    else:
        bgkey="<th>IP Address</th><td><ul class=\"comma-separated\"><li>"
        endkey="</li></ul></td></tr>"
        target_begin=res_html.find(bgkey)+bgkey.__len__()
        target_end=res_html.find(endkey,target_begin)
        ipaddr=res_html[target_begin:target_end]
        hosts.append((ipaddr,i))
        print(ipaddr)

print("开始写入HOST文件")
filename="C:\Windows\System32\drivers\etc\hosts"
hostsfile=open(filename,'a')
for i in hosts:
    hostsfile.write("%s %s\r\n"%(i[0],i[1]))
    print("%s %s"%(i[0],i[1]))
hostsfile.close()
