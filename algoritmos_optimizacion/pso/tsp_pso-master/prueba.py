

import itertools
import numpy as np

#nxm_random_num=list(np.random.permutation(100))
job_order=list(range(0,99))#nxm_random_num

for j in job_order:
    job_order[j]=job_order[j]%10
#print(job_order)

my_list=list(itertools.permutations(job_order))

with open('your_file.txt', 'w') as f:
    for item in my_list:
        f.write("%s\n" % item)
