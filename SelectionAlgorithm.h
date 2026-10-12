#ifndef SELECTIONALGORITHM_H
#define SELECTIONALGORITHM_H


class SelectionAlgorithm
{
    protected:
        int k;

    public:
        virtual int select();
        virtual ~SelectionAlgorithm() = default;

         SelectionAlgorithm(int k);


};

#endif // SELECTIONALGORITHM_H
