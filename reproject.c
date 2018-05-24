/**
 * reproject.cpp
 * Authors: Yizhao Gao <ygao29@illinois.edu>
 * Date: {12/06/2017}
 */


#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <omp.h>

void clipping(double * val, double * mask, int nPixels)
{
	for(int i = 0; i < nPixels; i++)
	{
		if(mask[i] == -999)
		{
			val[i] = -999;
		}
	}
}

void nnInterpolate(double * souVal, double * tarVal,
                   int * tarNNSouID, int nTar)
{

	int nnSouID;
	int i;

#pragma omp parallel for private(nnSouID)
	for(i = 0; i < nTar; i++) {
		nnSouID = tarNNSouID[i];
		if(nnSouID < 0) {
			tarVal[i] = -999;
		}
		else {
			tarVal[i] = souVal[nnSouID];
		}
	}
}


