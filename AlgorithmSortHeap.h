#ifndef ALGORITHMSORTHEAP_H
#define ALGORITHMSORTHEAP_H
#include "SelectionAlgorithm.h"
#include <iostream>
using namespace std;

class AlgorithmSortHeap:public SelectionAlgorithm
{
     public:
        AlgorithmSortHeap(int k);
        virtual int select();
};

#endif // ALGORITHMSORTHEAP_H
