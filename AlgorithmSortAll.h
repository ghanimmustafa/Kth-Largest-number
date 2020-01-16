#ifndef ALGORITHMSORTALL_H
#define ALGORITHMSORTALL_H
#include "SelectionAlgorithm.h"
#include <iostream>
using namespace std;
class AlgorithmSortAll:public SelectionAlgorithm
{
    public:
        AlgorithmSortAll(int k);
        virtual int select();

};


#endif // ALGORITHMSORTALL_H
