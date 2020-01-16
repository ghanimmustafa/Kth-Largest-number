#include "AlgorithmSortQuick.h"

AlgorithmSortQuick::AlgorithmSortQuick(int k): SelectionAlgorithm(k){
       this->k = k;
}

int AlgorithmSortQuick::select()
{
    int N = 0;
     cin>>N;
     int x=0;
     int *pNums = 0;
    pNums = new int[N];
    int left =0;
    int right = N-1;
    for (int i=0; i< N; i++)
    {
             cin>>x;
            pNums[i] = x;
    }
   quickselect( pNums, left, right, k);
    int result = pNums[k];
    cout<<"Result: "<<result<<endl;
    pNums = 0;
    delete [] pNums;
    return result;
}

int AlgorithmSortQuick::quickselect(int* pNums,int left, int right,int k)

{
    int array_size = right - left + 1 ;
    if(array_size>10)
    {
        // Partition, Quick sort, and quick select:
       int pivot=median3(pNums,left,right);
        int i=left,j=right-1;
        for(;;)
        {
            while(pNums[++i]>pivot){}
            while(pNums[--j]<pivot){}
            if(i<j)
                swap(pNums,i,j);
            else
                break;

        }
        swap(pNums,i,right-1);

        if (k == i) {
            return pivot;
        } else if (k <=  i - 1) {
            return quickselect(pNums, left, i - 1, k);
        } else {
            return quickselect(pNums, i + 1, right, k);
        }

    }
    else
    {
            // Do insertion sort for N<=10
           for(int i=0; i<=array_size; i++)
        {
            int  temp = pNums[i];
            int j= i-1;
            while(j>=0 && temp >= pNums[j])
            {
                pNums[j+1] = pNums[j];
                j = j-1;
            }
            pNums[j+1] = temp;
        }
        return pNums[k-1];
    }
}

int AlgorithmSortQuick::median3(int* pNums,int left, int right)
{
    int center = (left + right ) / 2 ;

   if(pNums[center]>pNums[left])
   {
        swap(pNums,left,center);
   }
   if(pNums[right]>pNums[left])
   {
        swap(pNums,left,right);
   }
   if(pNums[right]>pNums[center])
   {
        swap(pNums,right,center);
   }
   swap(pNums,center,right-1);
   return pNums[right-1];
}


void AlgorithmSortQuick::swap(int* pNums,int i, int j) {
	int t = pNums[i];
	pNums[i] = pNums[j];
	pNums[j] = t;
}
