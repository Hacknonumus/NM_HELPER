#!/usr/bin/python3.9

import os,argparse,sys,colorama

red=colorama.Fore.RED
reset=colorama.Fore.RESET
blue=colorama.Fore.BLUE
cyne=colorama.Fore.CYAN
ylo=colorama.Fore.YELLOW
            
def  main():
    if os.geteuid() != 0:
        print(red,"you need root permission! exiting",reset)
        sys.exit()

    parser = argparse.ArgumentParser(description=red+"....SIMPLE SCRIPT TO RECON...."+reset)
    
    parser.add_argument("-n","--nmap",action="store_true",help="running nmap")
    parser.add_argument("-sC","--nmap_script",action="store_true",help="running nmap script scan ")
    parser.add_argument("-s","--subdomain_enum",action="store_true",help="runing subdomain tools")
    parser.add_argument("-go","--gobuster",action="store_true",help="running gobuster")

    parser.add_argument("ip",type=str,help="enter ip ")
    parser.add_argument("-p","--port",type=str,help="port")
    parser.add_argument("-x","--add_command",type=str,help="add custom command for each tool..")
    
    args = parser.parse_args()
    
    cmd=args.add_command
    ip = args.ip
    prt=args.port 
    
    for i in (args.nmap,args.port,args.gobuster):
            
        if args.nmap and args.port :
            print("Hi:",ip,prt)
            x=("curl -s -I -v "+ip)
            y=("nmap -sS -sV -sC -f -A --append-output "+ip)
            for x in (x,) :
                print(cyne),os.system(x+':'+prt)
                for y in (y,):
                    print(red),os.system(y+' -p'+prt),print(reset)
        
        elif args.nmap  :
            print("Hi:",ip)
            
            for i in ("nmap -v -T5 -n -oN "+ip+" "+ip,):
                print(blue),os.system(i +' --reason | grep -e "Discovered open port" ')
                print("[~]OPEN PORTS FOUND..",reset )
                if "80/tcp" or "443/tcp" in open(ip,"r") :
                    os.system('nmap -sS -sV -sC -f -A '" "+ip+" "+' -oX .searchsploit.xml')
                    print( "Finding Searchsploit ....")
                    os.system('searchsploit -v --nmap .searchsploit.xml;rm -rf .searchsploit.xml'+" "+ip) 
                elif "80/tcp" or "443/tcp" not in open(ip,"r"):
                    print("[~]OPEN PORTS NOT FOUND..")
                    os.system(i) 
        
        elif args.gobuster:
            print(red,"Gobuster Running.....",reset)
            os.system("zenity --file-selection --filename=/usr/share/wordlists/ >> sav")
            for i in open("sav","r"):                                                                                                           
                print(i)
                os.system("gobuster dir --wildcard -t 20 -z -q "+" "+'-u '+ip+" "+'-w '+" "+i)
                os.remove('sav')
            
                
        elif args.subdomain_enum:
            print(red,"[~] Subdomain Enumration...",reset)
            for ip in ("amass enum --passive -d "+ip,"assetfinder -subs-only "+ip,"subfinder -silent -d "+ip):
                for i in ("amass","assetfinder","subfinder"):
                    print(blue,"[!]Running:~ ",i,reset)
                    os.system(ip+'>> subdomain.txt')   
                    os.system('sleep 1') 
                break
            print(cyne),os.system('sort subdomain.txt | uniq -u subdomain.txt'),print(reset)
        
        break 

    if args.nmap_script:
        try:
            print(red,"[~] NMAP SCRIPT ...",reset)
            print("[~]vulners \n[~]vuln")
            x = input(ylo + "enter script type \n:~"+reset)
            line = "nmap -sS -sV -A -f --script vulners"
            line = line.replace("vulners",x)
            print(line,ip)
            os.system(line + " "+ ip) 
        
        except KeyboardInterrupt as key:    
            print(red,"Exited",reset)
            

                  
if __name__ == "__main__" :    
    main()
    
