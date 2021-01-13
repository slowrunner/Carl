# plib EasyGoPiGo3 and GoPiGo3 develoment folder

1) ./make_locals.sh  to create local copy of _plib.py files and .bak files  
2) ./diff_plib_w_local.sh  to be sure no changes applied in plib/ files  
3) ./get_di_versions.sh  to bring latest DI version local
4) edit locals  
5) ./test_new_easygopigo3.py  to test using local files  
6) ./test_plib_easygopigo3.py to test using files in plib
7) ./diff_local_to_bak.sh to see changes made so far  
8) When ready to release locals to plib/  
   ./release_to_plib.sh   to copy locals to plib/ and to _plib.py  
9) When satisfied rm *.bak  
10) git status
11) git add easygopigo3_plib.py gopigo3_plib.py ~/Carl/plib/easygopigo3.py ~/Carl/plib/gopigo3.py
12) commit and push

