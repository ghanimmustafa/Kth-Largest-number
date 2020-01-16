#include "AlgorithmSortK.h"

AlgorithmSortK::AlgorithmSortK(int k) : SelectionAlgorithm(k)
{
    this->k = k;

}

int AlgorithmSortK::select()

{
    int N = 0;
    int x=0;
    int *pNums = 0;
    cin>>N;
    int tmp;
    pNums = new int[k];
     int key, j,i,shift;

    for ( i=0; i<k; i++)
    {
        cin>>x;
        pNums[i] = x;
    }



    for ( i = 1; i <k; i++)
    {
            key = pNums[i];
            j = i - 1;
            while (j >= 0 && pNums[j] <key)
            {
                pNums[j + 1] = pNums[j];
                j = j - 1;
            }
            pNums[j + 1] = key;
    }
    for( i=k; i<N; i++)
    {
        cin >> x;


        if(x>pNums[k-1]) {

            pNums[k-1] = x;
            shift = k - 1;
            while(shift > 0 && pNums[shift] > pNums[shift-1]  )
             {
                        tmp = pNums[shift];
                     pNums[shift]=pNums[shift-1];
                     pNums[shift-1]=tmp;
                     shift--;


             }

        }

    }

        cout<<"Result: "<<pNums[k-1]<<endl;
        int result=pNums[k-1];


        delete [] pNums;
        pNums = 0;
        return result;




    }


/*


            pNums[k-1] = x;

            for(int shift=k-1;shift>0;shift--)
             {

                 if (pNums[shift] > pNums[shift-1]) {
                      tmp = pNums[shift];
                     pNums[shift]=pNums[shift-1];
                     pNums[shift-1]=tmp;
                 }

             }

*/



