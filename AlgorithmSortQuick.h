#ifndef ALGORITHMSORTQUICK_H
#define ALGORITHMSORTQUICK_H
#include "SelectionAlgorithm.h"
#include <iostream>

using namespace std;
//+select() : int
//+quickselect(in numbers * : int, in left : int, in right : int, in k : int) : int
//+AlgorithmSortQuick(in k : int)
// numbers is an integer array
class AlgorithmSortQuick:public SelectionAlgorithm
{
    public:
        AlgorithmSortQuick(int k);
        virtual int select();
        int quickselect( int*, int, int, int);
        int median3(int*,int,int);
        void swap(int*,int , int );






};

#endif // ALGORITHMSORTQUICK_H
