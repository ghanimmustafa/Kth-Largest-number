#ifndef ALGORITHMSORTK_H
#define ALGORITHMSORTK_H
#include "SelectionAlgorithm.h"
#include <iostream>

using namespace std;

class AlgorithmSortK:public SelectionAlgorithm
{

    public:
        AlgorithmSortK(int k);

        virtual int select();

};

#endif // ALGORITHMSORTK_H
