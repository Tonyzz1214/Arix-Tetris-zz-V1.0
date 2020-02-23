#工具函数
import pygame
class Tools (object):
    def __init__(self):
        pygame.init()
        self.blue = pygame.image.load("res/blue01.png").convert_alpha()
        self.green=pygame.image.load("res/green01.png").convert_alpha()
        self.orage=pygame.image.load("res/orage01.png").convert_alpha()
        self.purpel=pygame.image.load("res/purpel01.png").convert_alpha()
        self.red=pygame.image.load("res/red01.png").convert_alpha()
        self.yellow=pygame.image.load("res/yellow01.png").convert_alpha()
        self.blocklist = [self.blue, self.green, self.orage, self.purpel, self.red, self.yellow]

    def getblocklist(self):
        return self.blocklist

    def BlitInitArix(self,x,y,type,picx = 50):
        """
            :param x:int-定位块的X位置
            :param y:int-定位块的Y位置
            :param type:int-块的类型0：T，1：L，2：Z，3:田字,4:I
            :return: int-list
        """
        XYlist=[(0,0),(0,0),(0,0),(0,0)]
        #T型
        if type==0:
            XYlist = [(x-picx, y), (x, y), (x + picx, y), (x ,y + picx)]
        # L型
        elif type==1:
            XYlist = [(x, y), (x , y+ picx), (x , y+ picx * 2), ((x + picx), (y + picx * 2))]
        # Z型
        elif type == 2:
            XYlist = [(x, y), (x+ picx, y), (x+ picx, y + picx), ((x + picx*2), (y + picx))]
        # 田子型
        elif type == 3:
            XYlist = [(x, y), (x + picx, y), (x , y+ picx), (x + picx, y + picx)]
        #I型
        elif type == 4:
            XYlist = [(x, y), (x + picx, y), (x+ picx*2 , y), (x + picx*3, y)]
        return XYlist

    def Arix_status_switch(self,arixtype,arixsubtype,block_postion_xy):
        """
        :param arixtype: 需要转换的块的类型0-4
        :param arixsubtype:需要转换的块的子类型0-4
        :param block_postion_xy:所有块的坐标
        :return: 下一个状态块所有的坐标，是一个4个元素的坐标list，arixsubtype
        """
        picx = 50
        x = block_postion_xy[0][0]
        y = block_postion_xy[0][1]
        # T型
        if arixtype == 0:
            if arixsubtype==0:
                XYlist=[(x+picx,y-picx),(x,y),(x+picx,y),(x+picx,y+picx)]
            elif arixsubtype==1:
                XYlist = [block_postion_xy[0],block_postion_xy[1],block_postion_xy[2],(x+picx,y+picx)]
            elif arixsubtype==2:
                XYlist = [block_postion_xy[0],(x,y+picx), (x,y+2*picx),(x+picx,y+picx)]
            elif arixsubtype==3:
                XYlist = [(x-picx,y+picx),(x,y+picx), (x,y+2*picx),(x+picx,y+picx)]
            arixnextsubtype = (arixsubtype + 1) % 4
            return XYlist, arixnextsubtype
        # L型
        elif arixtype == 1:
            if arixsubtype == 0:
                XYlist = [(x , y + 2*picx), (x, y + picx), (x + picx, y + picx), (x + 2*picx, y + picx)]
            elif arixsubtype == 1:
                XYlist = [(x , y -picx), (x+ picx, y - picx), (x + picx, y ), (x + picx, y + picx)]
            elif arixsubtype == 2:
                XYlist = [(x -picx, y +picx), (x, y + picx), (x + picx, y+ picx ), (x + picx, y)]
            elif arixsubtype == 3:
                XYlist = [(x+ picx, y -2* picx), (x+ picx, y - picx), (x+ picx, y ), (x + 2*picx, y )]
            arixnextsubtype = (arixsubtype + 1) % 4
            return XYlist, arixnextsubtype
        # Z型
        elif arixtype == 2:
            if arixsubtype == 0:
                XYlist = [(x+ 2*picx , y - picx), (x+ 2*picx, y), (x + picx, y), (x + picx, y + picx)]
            elif arixsubtype == 1:
                XYlist = [(x-2*picx , y+ picx ), (x- picx, y + picx), (x - picx, y+2*picx ), (x , y + 2*picx)]
            arixnextsubtype = (arixsubtype + 1) % 2
            #print("arixtype,arixsubtype=", arixtype, arixsubtype)
            return XYlist, arixnextsubtype
        # 田子型
        elif arixtype == 3:
            arixnextsubtype=0
            XYlist = [(x, y), (x + picx, y), (x, y + picx), (x + picx, y + picx)]
            return XYlist, arixnextsubtype
        # I型
        elif arixtype == 4:
            if arixsubtype == 0:
                XYlist = [(x, y), (x+ picx, y ), (x + 2*picx, y ), (x + 3*picx, y)]
            elif arixsubtype == 1:
                XYlist = [(x, y), (x , y - picx), (x, y- 2*picx), (x , y- 3*picx)]
            arixnextsubtype = (arixsubtype + 1) % 2
            # ("arixtype,arixsubtype=",arixtype,arixsubtype)
            return XYlist, arixnextsubtype
        #return XYlist

    def Arix_allblock_move(self,blocklistpostion,xory,addorsub,arixsize):
        """
        :param blocklistpostion: 4个方块的位置list
        :param xory: x或者y轴操作
        :param addorsub: +还是-
        :param arixsize: 移动step
        :return:
        """
        screenx = 502  # 操作框的宽
        screeny = 730  # 操作框的长
        if xory=="x"and addorsub=="add":
            if (blocklistpostion[0][0]+ arixsize<=screenx
                and blocklistpostion[1][0] + arixsize<=screenx
                and blocklistpostion[2][0] + arixsize<=screenx
                and blocklistpostion[3][0] + arixsize<=screenx):
                nextpostion = [(blocklistpostion[0][0]+ arixsize, blocklistpostion[0][1] ),
                              (blocklistpostion[1][0] + arixsize, blocklistpostion[1][1]),
                              (blocklistpostion[2][0] + arixsize, blocklistpostion[2][1]),
                              (blocklistpostion[3][0] + arixsize, blocklistpostion[3][1])]
            else:
                nextpostion=blocklistpostion
            return nextpostion
        elif xory=="x" and addorsub=="sub":
            if (blocklistpostion[0][0] - arixsize >= 0
                    and blocklistpostion[1][0] - arixsize >= 0
                    and blocklistpostion[2][0] - arixsize >= 0
                    and blocklistpostion[3][0] - arixsize >= 0):
                nextpostion = [(blocklistpostion[0][0] - arixsize, blocklistpostion[0][1]),
                               (blocklistpostion[1][0] - arixsize, blocklistpostion[1][1]),
                               (blocklistpostion[2][0] - arixsize, blocklistpostion[2][1]),
                               (blocklistpostion[3][0] - arixsize, blocklistpostion[3][1])]
            else:
                nextpostion=blocklistpostion
            return nextpostion
        if xory == "y" and addorsub == "add":
            if (blocklistpostion[0][1] + arixsize <= screeny
                    and blocklistpostion[1][1] + arixsize <= screeny
                    and blocklistpostion[2][1] + arixsize <= screeny
                    and blocklistpostion[3][1] + arixsize <= screeny):
                nextpostion = [(blocklistpostion[0][0], blocklistpostion[0][1] + arixsize),
                               (blocklistpostion[1][0], blocklistpostion[1][1] + arixsize),
                               (blocklistpostion[2][0], blocklistpostion[2][1] + arixsize),
                               (blocklistpostion[3][0], blocklistpostion[3][1] + arixsize)]
            else:
                nextpostion = blocklistpostion
            return nextpostion
        elif xory == "y" and addorsub == "sub":
            nextpostion = [(blocklistpostion[0][0] , blocklistpostion[0][1]- arixsize),
                           (blocklistpostion[1][0] , blocklistpostion[1][1]- arixsize),
                           (blocklistpostion[2][0] , blocklistpostion[2][1]- arixsize),
                           (blocklistpostion[3][0] , blocklistpostion[3][1]- arixsize)]
            return nextpostion
        if xory == "xy" and addorsub == "add":
            nextpostion = [(blocklistpostion[0][0] + arixsize, blocklistpostion[0][1] + arixsize),
                           (blocklistpostion[1][0] + arixsize, blocklistpostion[1][1] + arixsize),
                           (blocklistpostion[2][0] + arixsize, blocklistpostion[2][1] + arixsize),
                           (blocklistpostion[3][0] + arixsize, blocklistpostion[3][1] + arixsize)]
            return nextpostion
        elif xory == "xy" and addorsub == "sub":
            nextpostion = [(blocklistpostion[0][0]- arixsize , blocklistpostion[0][1]- arixsize),
                           (blocklistpostion[1][0]- arixsize , blocklistpostion[1][1]- arixsize),
                           (blocklistpostion[2][0]- arixsize , blocklistpostion[2][1]- arixsize),
                           (blocklistpostion[3][0]- arixsize , blocklistpostion[3][1]- arixsize)]
            return nextpostion

    def Get_LowestY(self,blocklistpostion):
        thelowestY=0
        for y in blocklistpostion:
            #print("y", y)
            if(y[1]>thelowestY):
                thelowestY=y[1]
        #print ("thelowestY2",thelowestY)
        return thelowestY
if __name__ == '__main__':
    newt=Tools()
    #print(newt.BlitInitArix(0,0,0))