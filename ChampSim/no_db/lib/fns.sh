#!/bin/bash
#
# Help functions
#

###############################################################################
#                               Main functions                                #
###############################################################################
fn_correctness()
{
    if [[ "$TEST" == "N" ]]; then return; fi

    for i in $1/*; do
        if [ -d $i ]; then 
            fn_correctness $i; 
        else 
            fn_aux_correctness $i; 
        fi
    done
}

fn_csv()
{

    files=1
    for i in $2/*; do
        if [ -d $i ]; then $1 $i ${@:3}
        else files=0; fi
    done

    if [ $files -eq 0 ]; then $1 $2 ${@:3}; fi
}

fn_cli()
{
    files=1
    first=0
    for i in $2/*; do
        if [ -d $i ]; then
            name=$(echo $i | rev | cut -d'/' -f1 | rev)

            if [ $first -eq 1 ]; then 
                fn_print_cli_press_key "$name"; 
                echo ""
            fi

            aux=$($1 $i ${@:3})
            aux=$(echo "$aux" | fn_awk_column $(echo "$aux" | fn_lenght))
            fn_print_cli $(echo $name | tr '[:lower:]' '[:upper:]') "$aux"
            first=1
        else files=0; fi
    done

    if [ $files -eq 0 ]; then 
        if [ $first -eq 1 ]; then 
            fn_print_cli_press_key "Base"; 
            echo ""
        fi

        aux=$($1 $2 ${@:3})
        aux=$(echo "$aux" | fn_awk_column $(echo "$aux" | fn_lenght))
        fn_print_cli "Base" "$aux"
    fi
}

fn_best()
{
    # Copy to move all the benchmarks
    mkdir $2/all
    cp $2/gap/* $2/all/
    cp $2/spec2k17/* $2/all/

    if [[ "$3" == "max" ]]; then
        gap=$(fn_get_best_max "$1 $2/gap")
        spec=$(fn_get_best_max "$1 $2/spec2k17")
        all=$(fn_get_best_max "$1 $2/all")
    elif [[ "$3" == "min" ]]; then
        gap=$(fn_get_best_min "$1 $2/gap")
        spec=$(fn_get_best_min "$1 $2/spec2k17")
        all=$(fn_get_best_min "$1 $2/all")
    fi

    fn_print_cli "GAP" "$gap"
    fn_print_cli_press_key "$spec"
    fn_print_cli "SPEC" "$spec"
    fn_print_cli_press_key "$all"
    fn_print_cli "ALL" "$all"

    rm -r $2/all
}

###############################################################################
#                                Aux functions                                #
###############################################################################

fn_lenght()
{
    # Get max word length
    sed 's/,/\n/g' | sort | uniq | awk '{print length, $0}' | sort -nr | head -n 1 | cut -d' ' -f1 | tr -d '\n'
}

fn_awk_column()
{
    # Convert text to columns using awk
    awk -v var="$1" -F',' '{for (i=1;i<=NF;i++) { if (length($i) != 0) printf("%"var"s|", $i)}; printf("\n"); }'
}

fn_print_cli()
{
    # Parameters
    #   $1: Name
    #   $2: Info
    if [ ! -z "$2" ]; then
        echo -e "\033[1m$1\033[0m"
        echo -e "\033[1m-------------------------------------------------------\033[0m"
        echo "$2"
        echo -e "\033[1m-------------------------------------------------------\033[0m"
    fi
 
}

fn_print_cli_press_key()
{
    # Parameters
    #   $1: should I show info?
    if [ ! -z "$1" ]; then
        echo ""
        echo -n -e "\033[3mPress key to continue\033[0m"
        read -p ""
        return 1
    fi
    return 0
 
}

fn_get_best_max()
{
    $1 | tail -n 2 | tr -d ' ' | python -c "\
import sys
import numpy as np
foo = [float(i) for i in sys.stdin.readline().split('\n')[0].split(',')[1:]]
bar = sys.stdin.readline().split('\n')[0].split(',')[1:]
dx = np.argmax(foo)
print(\"{}: {}\".format(bar[dx], foo[dx]))
        "
}

fn_get_best_min()
{
    $1 | tail -n 2 | tr -d ' ' | python -c "\
import sys
import numpy as np
foo = [float(i) for i in sys.stdin.readline().split('\n')[0].split(',')[1:]]
bar = sys.stdin.readline().split('\n')[0].split(',')[1:]
dx = np.argmin(foo)
print(\"{}: {}\".format(bar[dx], foo[dx]))
        "
}

fn_aux_correctness()
{
    # Test if simulation outputs are correct
    $(dirname "$0")/test_correcteness.sh $1 || exit 1
}
