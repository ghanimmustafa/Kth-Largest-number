#include "TestBed.h"
#include <iostream>
#include <ctime>
using namespace std;

TestBed::TestBed()
{
}

 void TestBed::execute(){



    // Time stamp before the computations

    clock_t start = clock();
    algorithm->select();

    // Computations to be measured //
    // Time stamp after the computations
    clock_t end = clock();
   double cpu_time = static_cast<double>( end - start ) /CLOCKS_PER_SEC;
    cout<<"Duration(sec):"<< cpu_time<<endl;


 }
 void TestBed::setAlgorithm(int al,int k){

     if(al==1)
        algorithm = new AlgorithmSortAll(k);
     else if(al==2)
        algorithm= new AlgorithmSortK(k);
     else if(al==3)
        algorithm = new AlgorithmSortHeap(k);
     else if(al==4)
         algorithm = new AlgorithmSortQuick(k);
      else
     cout<<"No Valid Algorithm type"<<endl;

 };

TestBed::~TestBed(){
    delete algorithm;
}
