from mpi4py import MPI
comm = MPI.COMM_WORLD
size=comm.Get_size()
rank = comm.Get_rank()

event_list={'e1':"event 1",'e2':"event 2",'e3':"event 3",'e4':"event 4",'e5':"event 5",'e6':"event 6",'e7':"event 7",'e8':"event 8"}


if rank==0:
    temptag=100
    data='e1'
    req1 = comm.isend(data, dest=1, tag=temptag)
    req1.wait()
    temptag=temptag+1
    data='e2'
    req2 = comm.isend(data, dest=2, tag=temptag)
    req2.wait()
    temptag=temptag+1
    data='e3'
    req3 = comm.isend(data, dest=3, tag=temptag)
    req3.wait()
    temptag=temptag+1
    data='e4'
    req4 = comm.isend(data, dest=4, tag=temptag)
    req4.wait()
    temptag=temptag+1
    data='e5'
    req5 = comm.isend(data, dest=5, tag=temptag)
    req5.wait()
    
    print ('Sends finished')
    
    
    temptag1=1000
    req6 = comm.irecv(source=1,tag=temptag1)
    data = req6.wait()
    print ('Node001 is %s'%(str(data)))
    temptag2=2000
    req7 = comm.irecv(source=2,tag=temptag2)
    data = req7.wait()
    print ('Node002 is %s'%(str(data)))
    temptag3=3000
    req8 = comm.irecv(source=3,tag=temptag3)
    data = req8.wait()
    print ('Node003 is %s'%(str(data)))
    temptag4=4000
    req9 = comm.irecv(source=4,tag=temptag4)
    data = req9.wait()
    print ('Node004 is %s'%(str(data)))
    temptag5=5000
    req10 = comm.irecv(source=5,tag=temptag5)
    data = req10.wait()
    print ('Node005 is %s'%(str(data)))
    
    
    print('Received all ACKs')
    temptag=temptag+1
    data='e6'
    req11 = comm.isend(data, dest=1, tag=temptag) #tag=105
    req11.wait()


    


elif rank==1:
    temptag=100
    req = comm.irecv(source=0,tag=temptag)
    data = req.wait()
    print ('Node001 is executing %s'%(str(event_list[data])))
    temptag1=1000
    data='done1'
    req1 = comm.isend(data, dest=0, tag=temptag1)
    req1.wait()
    
    temptag=temptag+5
    req = comm.irecv(source=0,tag=temptag)
    data = req.wait()
    print ('Node001 is executing %s'%(str(event_list[data])))
    

    
elif rank==2:
    temptag=101
    req = comm.irecv(source=0,tag=temptag)
    data = req.wait()
    print ('Node002 is executing %s'%(str(event_list[data])))
    temptag2=2000
    data='done2'
    req1 = comm.isend(data, dest=0, tag=temptag2)
    req1.wait()
    
elif rank==3:
    temptag=102
    req = comm.irecv(source=0,tag=temptag)
    data = req.wait()
    print ('Node003 is executing %s'%(str(event_list[data])))
    temptag3=3000
    data='done3'
    req1 = comm.isend(data, dest=0, tag=temptag3)
    req1.wait()
    
    
elif rank==4:
    temptag=103
    req = comm.irecv(source=0,tag=temptag)
    data = req.wait()
    print ('Node004 is executing %s'%(str(event_list[data])))
    temptag4=4000
    data='done4'
    req1 = comm.isend(data, dest=0, tag=temptag4)
    req1.wait()
    
    
elif rank==5:
    temptag=104
    req = comm.irecv(source=0,tag=temptag)
    data = req.wait()
    print ('Node005 is executing %s'%(str(event_list[data])))
    temptag5=5000
    data='done5'
    req1 = comm.isend(data, dest=0, tag=temptag5)
    req1.wait()
