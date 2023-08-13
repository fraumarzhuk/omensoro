#!/bin/bash

URL="https://db5xszokwvv76.cloudfront.net/uploads/mobile_file/content/88366/Omens.dmg"

DMGName=`basename $URL`;

cd ~/Downloads/

echo -e "Starting installer for DMG from $URL \n";

http_code="$(curl -w '%{http_code}\n' -o "$DMGName" $URL)"

if [ ! "$http_code" = 200 ]; then
	echo "Failed to download file. Failed with error: $http_code";
	exit 1;
fi

echo "Starting installation"

VOLUME=`hdiutil attach -nobrowse "$DMGName" | grep Volumes | sed 's/.*\/Volumes\//\/Volumes\//'`
echo -e "\nVolume found : $VOLUME"
cd "$VOLUME"
\cp -rf *.app /Applications
INSTALLED=$?
cd ..
hdiutil detach "$VOLUME"

cd ~/Downloads/

if [ $INSTALLED -ne 0 ]; then
    echo -e "\nFailed to install"
    rm "$DMGName"
    exit 1
fi

echo -e "\nSuccessfully installed"
rm "$FILEPATH"
exit 0