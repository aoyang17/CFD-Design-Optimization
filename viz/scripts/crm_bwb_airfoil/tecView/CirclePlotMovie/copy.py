import os
folder='../CNN0.0'
it = 1
for i in range(90):
    orindx = '{0:03}'.format(i)
    if os.path.isfile(folder+'/fc_'+orindx+'_surf.cgns') and os.path.isfile(folder+'/FFD'+str(i)+'.xyz'):
        os.system('cp {0}/fc_{1}_surf.cgns input/surf{2}.cgns'.format(folder,orindx,it))
        os.system('cp {0}/FFD{1}.xyz input/FFD{2}.xyz'.format(folder,i,it))
        it +=1
    else:
        pass    
    
folder='../CNN0.0_restart'
for i in range(90,235):
    orindx = '{0:03}'.format(i-90)
    if os.path.isfile(folder+'/fc_'+orindx+'_surf.cgns') and os.path.isfile(folder+'/FFD'+str(i)+'.xyz'):
        os.system('cp {0}/fc_{1}_surf.cgns input/surf{2}.cgns'.format(folder,orindx,it))
        os.system('cp {0}/FFD{1}.xyz input/FFD{2}.xyz'.format(folder,i,it))
        it +=1
    else:
        pass    
    
    
    
