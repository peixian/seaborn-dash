#!/bin/bash

echo "Pulling Seaborn";
git clone "https://github.com/mwaskom/seaborn/";
cd seaborn/doc;
cd tutorial;
make;
cd ..;
make html;
doc2dash -n Seaborn _build/html;
mv Seaborn.docset ../../Seaborn.docset;
cd ../../;
rm -rf seaborn;
