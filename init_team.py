import sys ,os ,shutil
team_num = sys.argv[1]
workdir = "/home/awd/gamebox/awd_gamebox"   #need to be upgrade
print "There will be "+team_num+" team in this game!"
print "Init floder..........."

for i in range (int(team_num)) :
    dir_name = workdir+"/team"+str(i)
    print "Create team"+str(i)
    os.mkdir(dir_name)
    #shutil.copytree(workdir+"/project",dir_name)
    f=open(workdir+"/../team"+str(i)+"_score","a+")
    f.write("10000")
    f.close()
