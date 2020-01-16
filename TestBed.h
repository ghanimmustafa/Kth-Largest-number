#ifndef TESTBED_H
#define TESTBED_H
#include "SelectionAlgorithm.h"
#include "AlgorithmSortAll.h"
#include "AlgorithmSortK.h"
#include "AlgorithmSortHeap.h"
#include "AlgorithmSortQuick.h"
class TestBed
{
    private:
        SelectionAlgorithm* algorithm;

    public:
        void execute();
        void setAlgorithm(int,int);
        TestBed();
        ~TestBed();
};

#endif // TESTBED_H
