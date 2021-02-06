from csv import writer

def tutul(p):
    return p


def Createcsv(data):
    with open('dataset.csv','w') as file:
        csv_writer=writer(file,lineterminator='\n')
        header=('age','height','weight','city','education','income','gender','body_type','complexin','drinking','smoking','religion','family_status','marital_status','physical_status','id')
        csv_writer.writerow(header)
        for d in data:
           csv_writer.writerow(tuple(d.values()))
        print("done")
