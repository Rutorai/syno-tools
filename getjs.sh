#!/bin/bash

HOST_USER=${HOST_USER:-admin}
HOST_NAME=${HOST_NAME:-192.168.1.46}
HOST_PORT=${HOST_PORT:-522}

#ssh -p $HOST_PORT $HOST_USER@$HOST_NAME << __EOS__
#if [ -e ~/javascript_files.tar ]
#then
#    rm -f ~/javascript_files.tar
#fi
#
#find /usr/syno/synoman -name *.js -exec tar -rf ~/javascript_files.tar {} \; 2> /dev/null
#__EOS__

#mkdir -p ./js/beautified

#sftp $HOST_USER@$HOST_NAME:/homes/$HOST_USER/javascript_files.tar ./js/
#(cd ./js; tar xf javascript_files.tar)

#(
#cd ./js
#find ./ \( -path "./beautified" \) -prune -o -name *.js 2> /dev/null | while read -r i;
#do
#    if [ ! -d $i ];
#    then
#        target=${i#"./"}
#        basedir=$(dirname "$target")
#        mkdir -p "beautified/$basedir"
#        js-beautify $i > beautified/$target
#    fi
#done
#)

find ./packages -name *.js | while read -r i;
do
    echo "Beautifying $i"
    js-beautify $i > $i.beautifyed.js
    rm $i
    mv $i.beautifyed.js $i
done

echo "Finished"
