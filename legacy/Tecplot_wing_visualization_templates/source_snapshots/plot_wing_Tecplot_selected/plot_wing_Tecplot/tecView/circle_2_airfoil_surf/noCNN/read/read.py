from sqlitedict import SqliteDict

db = SqliteDict('../slsqp_hist.hst')    
lastIter = int(db['last'])
CFDlist=[]
for k in xrange(23):
    if 'funcs' in db[str(k)].keys():
        print db[str(k)]['xuser'].keys(),k
        CFDlist.append(k)
        #print db[str(lastIter-k)]['funcs']['fc_cd'],lastIter-k
        '''
        Alpha = db[str(lastIter-k)]['xuser']['alpha_AeroCRM']
        TwistWing = db[str(lastIter-k)]['xuser']['TwistWing']
        TwistTail = db[str(lastIter-k)]['xuser']['TwistTail']
        shapevars = db[str(lastIter-k)]['xuser']['shapevars']
        print Alpha
        print TwistWing
        print TwistTail
        print shapevars
        '''
        #break
        pass
#281

#print CFDlist
icfd=8


sety = db[str(CFDlist[icfd])]['xuser']['set_y']

f = open('lastp.dat','w')
for i in range(sety.shape[0]):
    f.write('%.15f\n'%(sety[i]))
f.close()



        
