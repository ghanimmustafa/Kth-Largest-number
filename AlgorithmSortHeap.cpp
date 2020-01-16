#include "AlgorithmSortHeap.h"
#include "BinaryHeap.h"

AlgorithmSortHeap::AlgorithmSortHeap(int k): SelectionAlgorithm(k){
       this->k = k;
}
int AlgorithmSortHeap::select()
{

 //   build a min heap with the first k numbers (i.e., k times insert)
 //then, compare the remaining N-k numbers with the root node (i.e., min. element)
 //if a number is smaller than the root, ignore the number
 //else, deleteMin (remove the root) and insert the new number
 //return the root element

    int N = 0;
    int x=0;

    BinaryHeap heap(k);
    cin>>N;

    for (int i=1; i<=k; i++)
    {
        cin>>x;
       	heap.insert(x);

    }
    int new_el;
   for(int j=k;j<N;j++)
    {
        cin>>new_el;
        if(new_el>heap.getMin())
        {
            heap.deleteMin();
            heap.insert(new_el);
        }
    }
    cout<<"Result: "<<heap.getMin()<<endl;
    return heap.getMin();

}

