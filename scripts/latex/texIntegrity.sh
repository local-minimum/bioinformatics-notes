#!/usr/bin/env bash                                                                          

# Author: Martin Zackrisson                                                                  
# TODO:                                                                                      
#   * Could allow verbosity off (no echo)                                                    
#   * Could allow output file                                                                
#   * Could allow manual patterns                                                            
#                                                                                            

if [ "$#" -ne 1 ] || [[ $1 == -h ]] || [[ $1 == --help ]]; then                              
    echo "Makes a diff between ref and label usage in a tex-file"                            
    echo "USAGE: texIntegrity.sh PATH"                                                       
    exit                                                                                     
fi                                                                                           

if [ ! -e $1 ]; then                                                                         
    echo "File '$1' not found"                                                               
    exit                                                                                     
fi                                                                                           

REFS=$(grep -E -o -e'\ref(fig|){[^}]+' $1 | grep -o -E -e'[^{}]*.$' | sort | uniq)           
LABELS=$(grep -E -o -e'\label{[^}]+' $1 | grep -o -E -e'[^{}]*.$' | sort | uniq)             

echo "#Showing difference in refernces and labels for $1"                                    
diff <(echo "$REFS") <(echo "$LABELS")
