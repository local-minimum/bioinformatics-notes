#!/usr/bin/env python                                                                                                  
                                                                                                                       
import os                                                                                                              
import sys                                                                                                             
import fnmatch                                                                                                         
import re                                                                                                              
from subprocess import call, PIPE                                                                                      
                                                                                                                       
                                                                                                                       
def get_recursive_files(base, pattern="*"):                                                                            
                                                                                                                       
    for root, _, filenames in os.walk(base):                                                                           
        for filename in fnmatch.filter(filenames, pattern):                                                            
            yield os.path.join(root, filename)                                                                         
                                     
                                                                                                                       
def smart_diff(base_a, base_b, pattern, ignore_expression):                                                            
                                                                                                                       
    files_a = tuple(get_recursive_files(base_a, pattern))                                                              
    files_b = tuple(get_recursive_files(base_b, pattern))                                                              
    if ignore_expression:                                                                                              
        files_b_renamed = tuple(                                                                                       
                re.sub("{0}/?".format(ignore_expression), '', f) for f in files_b)                                     
    else:                                                                                                              
        files_b_renamed = files_b                                                                                      
    files_b_renamed = {f2[len(base_b):]:f1 for f1, f2 in                                                               
            zip(files_b, files_b_renamed)}                                                                             
    files_a_renamed = {f2[len(base_a):]:f1 for f1, f2 in                                                               
            zip(files_a, files_a)}                                                                                     
                                                                                                                       
    print "\n *** {0} : {1} files, {2} : {3} files".format(                                                            
            base_a, len(files_a_renamed), base_b, len(files_b_renamed))                                                
                                                                                                                       
    common = report_uniques_and_get_common(files_a_renamed, files_b_renamed)                                           
                                                                                                                       
    print "\n *** Comparable files {0}".format(len(common))                                                            
                                                                                                                       
    sed_diff_common_files(files_a_renamed, files_b_renamed, common,                                                    
            ignore_expression)                   
            
            
def sed_diff_common_files(files1, files2, common, ignore_expression):                                                  
                                                                                                                       
    sed_expression = "'s/{0}//g'".format(ignore_expression)                                                            
                                                                                                                       
    for f in common:                                                                                                   
                                                                                                                       
        print "\n*** diff {0} {1}:\n".format(files1[f], files2[f])                                                     
                                                                                                                       
        expression = " ".join(                                                                                         
            ['sed', '-E', sed_expression, files2[f], '|', 'diff', files1[f], '-'])                                     
                                                                                                                       
        #print expression                                                                                              
                                                                                                                       
        call(expression, shell=True)                                                                                   
                                                                                                                       
                                                                                                                       
def report_uniques_and_get_common(files1, files2):                                                                     
                                                                                                                       
    common = []                                                                                                        
    for f in files1:                                                                                                   
        if f not in files2:                                                                                            
            print "\n*** Unique file {0}".format(files1[f])                                                            
        else:                                                                                                          
            common.append(f)                                                                                           
                                                                                                                       
    for f in files2:                                                                                                   
        if f not in files1:                                                                                            
            print "\n*** Unique file {0}".format(files2[f])                                                            
    return common                                                                                                      
                                                                                                                       
if __name__ == "__main__":                                                                                             
                                                                                                                       
    base_a = sys.argv[1]                                                                                               
    base_b = sys.argv[2]                                                                                               
    pattern = sys.argv[3] if len(sys.argv) > 3 else "*"                                                                
    ignore_expression = sys.argv[4] if len(sys.argv) > 4 else None                                                     
    smart_diff(base_a, base_b, pattern, ignore_expression)                                                             
