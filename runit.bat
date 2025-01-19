rem ## python script_name.py <URL> <Depth> <Output_Directory>
if not exist %3 mkdir %3
python url2html.py %1 %2 %3 