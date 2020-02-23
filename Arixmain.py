#罗斯方块，长20，框10，背景文件601*729
#
#
#
#
import pygame
from pygame.locals import *
from sys import exit
from Tools import *
import random
import time
pygame.init()
#初始固定变量
screenx=602#操作框的宽
screeny=730#操作框的长
arixsize=50#每个方块的长宽，最终应该是从图片获取传递过来
totalxmum=0#初始消掉的行数
#初始方块出现的地方，
Init_postion_X=arixsize*4+3
Init_postion_Y=arixsize*1+3
#方块的种类
arixtype=5
#
screen = pygame.display.set_mode((screenx,screeny))
pygame.display.set_caption("Arix-V1")
background = pygame.image.load("res/background.png").convert()
blocklist=Tools().getblocklist()
#绘制初始方块
#Init_arix_type=random.randint(0, arixtype-1)

Init_arix_type=random.randint(4,4) #初始类型是0 T型
arixsubtype=0
currentarixsubtype=0
currentblock_postion_X=Init_postion_X
currentblock_postion_Y=Init_postion_Y
framerate = pygame.time.Clock()
#绘制背景
screen.blit(background, (0, 0))
#绘制初始方块
for blockpostion in Tools().BlitInitArix(Init_postion_X, Init_postion_Y, Init_arix_type):
    currentblock = blocklist[Init_arix_type]
    screen.blit(currentblock, blockpostion)
blocklistpostion=Tools().BlitInitArix(Init_postion_X, Init_postion_Y, Init_arix_type)
tmpbpstion=blocklistpostion
AllblockInfo=[]
#AllblockInfo.append((0,(-1,-1)))
newtools=Tools()

#定义自动下降一格事件,可以控制下降的速度，通过Gameleve控制游戏级别和速度
GameLevel=1
arix_comedown = pygame.USEREVENT +1
pygame.time.set_timer(arix_comedown,2000-GameLevel*2)
currentarixtype=Init_arix_type
checklist=[]
#X从0开始到500，共10列，y从650到0，共13行,每组前面有标志位
for i in range (0,14):
    for j in range (0,10):
        checklist.append((0,(50*j+3,50*i+3)))
while True:
    key_press = pygame.key.get_pressed()
    framerate.tick(30)
    # 绘制背景
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        #处理定时自动下落，所有方块的4个Y坐标都移动
        if event.type == arix_comedown:
            tmpbpstion=newtools.Arix_allblock_move(blocklistpostion,"y","add",arixsize)
        #    blocklistpostion = tmpbpstion
        #
        # 这个计算比较low，由于tuple类型不能直接修改，则新生成了一个存放坐标的tmplist，计算完成之后，整个更新列表

    if key_press[K_w]:
        tmpbpstion = newtools.Arix_allblock_move(blocklistpostion, "y", "sub", arixsize)
        #blocklistpostion= tmpbpstion
    elif key_press[K_s]:
        tmpbpstion = newtools.Arix_allblock_move(blocklistpostion, "y", "add", arixsize)
        #blocklistpostion = tmpbpstion
    elif key_press[K_a]:
        tmpbpstion = newtools.Arix_allblock_move(blocklistpostion, "x", "sub", arixsize)
        #blocklistpostion = tmpbpstion
    elif key_press[K_d]:
        tmpbpstion = newtools.Arix_allblock_move(blocklistpostion, "x", "add", arixsize)
        #blocklistpostion = tmpbpstion
    elif key_press[K_SPACE]:
        tmpbpstion,currentarixsubtype=Tools().Arix_status_switch(currentarixtype,currentarixsubtype,blocklistpostion)
        #("SPace-pressed,subtype:"+str(currentarixsubtype))
    #更新各个方块的位置信息，后续方块的各种溢出判读就放在这里,当前方块信息和已经存在的方块信息比对，如果一致，则不可以移动
    coverornot = True
    for everyblock in tmpbpstion:
        for everyAllblockInfoblock in AllblockInfo:
            if everyblock==everyAllblockInfoblock[1]:
                coverornot = False
        #blocklistpostion = tmpbpstion
    if Tools().Get_LowestY(tmpbpstion)<660 and coverornot:
        blocklistpostion=tmpbpstion
    else:
        #print ("stop")
        #记录老方块的信息，type和位置信息
        for index in range (0,4):
            if len(AllblockInfo)>=1:
                if AllblockInfo[-1][1][1]<=blocklistpostion[index][1]:
                    AllblockInfo.append((currentarixtype, blocklistpostion[index]))
                else:
                    oldblockindex=0
                    for oldblock in AllblockInfo:
                        if oldblock[1][1]>blocklistpostion[index][1]:
                            inserttmpblock=(currentarixtype,blocklistpostion[index])
                            AllblockInfo.insert(oldblockindex,inserttmpblock)
                            break
                        oldblockindex=oldblockindex+1
            else:
                inserttmpblock = (currentarixtype, blocklistpostion[0])
                AllblockInfo.append(inserttmpblock)
                for index in range(1, 4):
                    oldblockindex = 0
                    for oldblock in AllblockInfo:
                        if oldblock[1][1] > blocklistpostion[index][1]:
                            inserttmpblock = (currentarixtype, blocklistpostion[index])
                            AllblockInfo.insert(oldblockindex, inserttmpblock)
                            break
                        oldblockindex = oldblockindex + 1

            #AllblockInfo.append((currentarixtype, blocklistpostion[0]))
            #AllblockInfo.append((currentarixtype, blocklistpostion[1]))
            #AllblockInfo.append((currentarixtype, blocklistpostion[2]))
            #AllblockInfo.append((currentarixtype, blocklistpostion[3]))
        #在checklist里面打点：
        checklist_i=0
        for blocktmp in blocklistpostion:
            for checkblock in checklist:
                if checkblock[1]==blocktmp:
                    checklist[checklist_i]=(1,checkblock[1])
                checklist_i = checklist_i + 1
            checklist_i = 0
        #检查是否有满足行满的情况
        totalrow=0
        xnum=0
        for x in range (0,14):
            for y in range(0,10):
                if checklist[x*10+y][0]==1:
                     totalrow=totalrow+1
                xnum=x
            if totalrow==10:
                # 1该行上方所有方块的Y都增加一个step
                AllblockInfono=0
                totalxmum=totalxmum+1
                GameLevel=totalxmum//20+1
                print("可以消除第:", xnum, "行了","一共消除了",totalxmum)
                for allblocktmp in AllblockInfo:
                    if allblocktmp[1][1]==xnum*arixsize+3:
                        del AllblockInfo[AllblockInfono:AllblockInfono+10]
                        break
                    AllblockInfono=AllblockInfono+1
                AllblockInfoaddtmp=0
                #for allblocktmp in AllblockInfo[:AllblockInfono]:
                    #tmpblock = (allblocktmp[0], (allblocktmp[1][0], allblocktmp[1][1] + 50))
                    #AllblockInfo[AllblockInfoaddtmp] = tmpblock
                    #AllblockInfoaddtmp = AllblockInfoaddtmp + 1
                for blockdownindex in range (0,AllblockInfono):
                    tmpblock=(AllblockInfo[blockdownindex][0],(AllblockInfo[blockdownindex][1][0],AllblockInfo[blockdownindex][1][1]+50))
                    AllblockInfo[AllblockInfoaddtmp]=tmpblock
                    AllblockInfoaddtmp=AllblockInfoaddtmp+1
                xnum=0
                #初始化checklist状态
                checklisttmp = []
                # X从0开始到500，共10列，y从650到0，共13行,每组前面有标志位
                for i in range(0, 14):
                    for j in range(0, 10):
                        checklisttmp.append((0, (50 * j + 3, 50 * i + 3)))
                checklist=checklisttmp
                #对所有方块刷新checklist状态
                for blocktmp in AllblockInfo:
                    for checkblock in checklist:
                        if checkblock[1] == blocktmp[1]:
                            checklist[checklist_i] = (1, checkblock[1])
                        checklist_i = checklist_i + 1
                    checklist_i = 0
            totalrow = 0
        #刷新一个新的方块
        currentarixtype=random.randint(0,4)
        blocklistpostion = Tools().BlitInitArix(Init_postion_X, Init_postion_Y, currentarixtype)
        tmpbpstion = blocklistpostion
        currentarixsubtype = 0
        for blockpostion in Tools().BlitInitArix(Init_postion_X, Init_postion_Y, currentarixtype):
            currentblock = blocklist[currentarixtype]
            screen.blit(currentblock, blockpostion)


    #刷新移动的方块
    for blockpostiontmp in blocklistpostion:
        currentblock = blocklist[currentarixtype]
        screen.blit(currentblock, blockpostiontmp)
    #检测老方块是否行满了，若满了，需要刷新数据，即所有老方块，Y+Step



    # 刷新老方块
    if len(AllblockInfo)>0:
        for allblocktmp in AllblockInfo:
            #for blocktmp in allblocktmp[1]:
            currentblock = blocklist[allblocktmp[0]]
            screen.blit(currentblock, allblocktmp[1])
    #显示积分和关数
    white = (255, 255, 255)
    myfont = pygame.font.SysFont("SimHei",15)
    textImage1 = myfont.render("消除行数:"+str(totalxmum), True, white)
    textImage2 = myfont.render("当前级别:" + str(GameLevel), True, white)
    screen.blit(textImage2, (510, 40))
    screen.blit(textImage1, (510, 60))
    pygame.display.update()
