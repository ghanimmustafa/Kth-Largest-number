#include "AlgorithmSortAll.h"

AlgorithmSortAll::AlgorithmSortAll(int k): SelectionAlgorithm(k){
       this->k = k;
}

int AlgorithmSortAll::select(){

    int N = 0;
    int x=0;
    int *pNums = 0; // Define pNums as a pointer to int, initialize to null
     // Define n for keeping the size needed for the array
    cin>>N;
    //cout<<"N:"<<N<<endl;
    // Read in the size
    pNums = new int[N];// Allocate n ints and save the pointer in pNums
for (int i=0; i<N; i++) {

    cin>>x;
    pNums[i] = x;

    }
    int *temp=0;
    //sorting - Descending ORDER

     int  i,key, j;
        for (i = 1; i <N; i++)
        {
            key = pNums[i];
            j = i - 1;
            while (j >= 0 && pNums[j] < key)
            {
                pNums[j + 1] = pNums[j];
                j = j - 1;
            }
            pNums[j + 1] = key;
        }
    cout<<"Result: "<<pNums[k-1]<<endl;
    int result=pNums[k-1];
    delete [] pNums; // When done, free the memory pointed to by pNums
    pNums = 0;

    return result;


}



