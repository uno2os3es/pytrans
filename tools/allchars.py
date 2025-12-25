#!/usr/bin/env python3

import sys
from math import remainder

def main():
    with open('allchars.txt','w') as f1:
        with open('all_chars.txt','w') as f2:
            with open('chars.txt','w') as f3:
                for i in range(1,55296):
                
                    try:
                       f1.write(f'{chr(i)}\n')
                       if i<10000:
                           f2.write(f'{i} : {chr(i)}\n')
                       if int(remainder(i,50))==0:
                           f3.write(f'{chr(i)}\n')
                       else:
                           f3.write(f'{chr(i)} ')
                
                    except:
                        print(i)
                        pass
        
if __name__ == "__main__":
    sys.exit(main())
