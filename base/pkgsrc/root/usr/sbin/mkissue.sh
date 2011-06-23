#!/bin/sh
#Build BrazilFW Wellcome Screen
#by: Gustavo Lago - Feb/2008 fix: Washington Rodrigues Mar/2008

. /etc/coyote/coyote.conf

[ -z "$SSH_PORT" ] && SSH_PORT=22
[ -z "$WEBADMIN_PORT" ] && WEBADMIN_PORT=8180
[ -z "$ADMIN_AUTH" ] && MESSAGE="password not set yet, press [ENTER]"
BFW_INFO=`echo CPU:[1m\`grep "model name" /proc/cpuinfo | cut -d: -f2\` \`grep "MHz" /proc/cpuinfo |cut -d: -f2 |cut -d. -f1\`MHz [0m/ Memory:[1m\`grep "MemTotal" /proc/meminfo |cut -d: -f2\`[1m'`
echo -ne "

           [0;34m,-----. [1;36m                      [1;37m ,--.,-[0;37m-.,----[0;36m--.,--. [1;36m  ,--. 
           [0;34m\174  \174) /[1;36m_ ,--.-[0;36m-. ,--,[0;37m--.,----[1;37m-.\140--'\174[0;37m  \174\174  .[0;36m---'\174  \174[1;36m   \174  \174 
          [0;34m \174  .-.[1;36m  \134\134\134\174  .[0;36m--'' ,-[0;37m.  \174\140-. [1;37m / ,--.[0;37m\174  \174\174  [0;36m\140--, \174  [1;36m\174.'.\174  [0;34m\174 
	 [0;34m  \174  '-[1;36m-' /\174  [0;36m\174   \134\134\134 '[0;37m-'  \174 / [1;37m \140-.\174  [0;37m\174\174  \174\174 [0;36m \174\140   \174 [1;36m  ,'.  [0;34m \174 
        [0;34m   \140---[1;36m---' \140-[0;36m-'    \140[0;37m--\140--'\140-[1;37m----'\140-[0;37m-'\140--'\140[0;36m--'    '[1;36m--'   '[0;34m--' 
   [0;34m ___[0;34m _     [1;36m       [0;36m       [0;37m  _ _   [1;37m       [0;37m      _ [0;36m  ___  [1;36m       [0;34m _           
   [0;34m\174 _[0;34m_(_)_ _[1;36m _____ [0;36m__ ____[0;37m _\174 \174 \174 [1;37m __ _ _[0;37m _  __\174 [0;36m\174 \174 _ \134\134\134[1;36m___ _  [0;34m_\174 \174_ __[0;34m_ _ _ 
   [0;34m\174 [0;34m_\174\174 \174 '[1;36m_/ -_) [0;36mV  V / [0;37m_\140 \174 \174 \174[1;37m / _\140 \174[0;37m ' \134\134\134/ _\140[0;36m \174 \174   [1;36m/ _ \134\134\134 \174[0;34m\174 \174  _/ [0;34m-_) '_\174
   [0;34m\174[0;34m_\174 \174_\174_[1;36m\174 \134\134\134___\174[0;36m\134\134\134_/\134\134\134_/\134\134\134[0;37m__,_\174_\174_[1;37m\174 \134\134\134__,_[0;37m\174_\174\174_\134\134\134_[0;36m_,_\174 \174_\174[1;36m_\134\134\134___/\134\134\134[0;34m_,_\174\134\134\134__\134\134\134[0;34m___\174_\174  [0m


Version: [1m`cat /var/lib/lrpkg/root.version`[0m  
Local IP Address: [1m$LOCAL_IPADDR[0m  
`echo $BFW_INFO | sed 's/[ ]\+/ /g'`

[0mTo remotely access this router use an SSH client to connect on port [1m$SSH_PORT[0m
Access the BrazilFW Web Admin by using the URL: [1mhttp://$LOCAL_IPADDR:$WEBADMIN_PORT

            [0;34mBrazilFW Official Website: [1;34mhttp://www.brazilfw.com.br[0m
                           [0mBrazilFW login is: [0;32mroot 
                    [0;31m $MESSAGE  [0m

" > /etc/issue