from PIL import Image
from sys import platform
import re
import glob
import os
import ntpath
from datetime import datetime
import sys
import pickle

houseID = sys.argv[1]

# if platform == "linux" or platform == "linux2":
#         outputDirectory='/homes/el216/Workspace/OutputSceneNet'
# elif platform == "darwin":
#         outputDirectory='/Users/lingevan/Workspace/SceneNet'

# house_output_dir = outputDirectory + "/" + houseID
house_temp_dir = '/homes/el216/Workspace/ScriptsSceneNet/' + houseID + '/'
house_output_temp_dir = "/homes/el216/Workspace/OutputSceneNet/" + houseID + '/'

WNID_TO_NYU_CLASS = {
        '04593077':4, '03262932':4, '02933112':6, '03207941':7, '03063968':10, '04398044':7, '04515003':7,
        '00017222':7, '02964075':10, '03246933':10, '03904060':10, '03018349':6, '03786621':4, '04225987':7,
        '04284002':7, '03211117':11, '02920259':1, '03782190':11, '03761084':7, '03710193':7, '03367059':7,
        '02747177':7, '03063599':7, '04599124':7, '20000036':10, '03085219':7, '04255586':7, '03165096':1,
        '03938244':1, '14845743':7, '03609235':7, '03238586':10, '03797390':7, '04152829':11, '04553920':7,
        '04608329':10, '20000016':4, '02883344':7, '04590933':4, '04466871':7, '03168217':4, '03490884':7,
        '04569063':7, '03071021':7, '03221720':12, '03309808':7, '04380533':7, '02839910':7, '03179701':10,
        '02823510':7, '03376595':4, '03891251':4, '03438257':7, '02686379':7, '03488438':7, '04118021':5,
        '03513137':7, '04315948':7, '03092883':10, '15101854':6, '03982430':10, '02920083':1, '02990373':3,
        '03346455':12, '03452594':7, '03612814':7, '06415419':7, '03025755':7, '02777927':12, '04546855':12,
        '20000040':10, '20000041':10, '04533802':7, '04459362':7, '04177755':9, '03206908':7, '20000021':4,
        '03624134':7, '04186051':7, '04152593':11, '03643737':7, '02676566':7, '02789487':6, '03237340':6,
        '04502670':7, '04208936':7, '20000024':4, '04401088':7, '04372370':12, '20000025':4, '03956922':7,
        '04379243':10, '04447028':7, '03147509':7, '03640988':7, '03916031':7, '03906997':7, '04190052':6,
        '02828884':4, '03962852':1, '03665366':7, '02881193':7, '03920867':4, '03773035':12, '03046257':12,
        '04516116':7, '00266645':7, '03665924':7, '03261776':7, '03991062':7, '03908831':7, '03759954':7,
        '04164868':7, '04004475':7, '03642806':7, '04589593':13, '04522168':7, '04446276':7, '08647616':4,
        '02808440':7, '08266235':10, '03467517':7, '04256520':9, '04337974':7, '03990474':7, '03116530':6,
        '03649674':4, '04349401':7, '01091234':7, '15075141':7, '20000028':9, '02960903':7, '04254009':7,
        '20000018':4, '20000020':4, '03676759':11, '20000022':4, '20000023':4, '02946921':7, '03957315':7,
        '20000026':4, '20000027':4, '04381587':10, '04101232':7, '03691459':7, '03273913':7, '02843684':7,
        '04183516':7, '04587648':13, '02815950':3, '03653583':6, '03525454':7, '03405725':6, '03636248':7,
        '03211616':11, '04177820':4, '04099969':4, '03928116':7, '04586225':7, '02738535':4, '20000039':10,
        '20000038':10, '04476259':7, '04009801':11, '03909406':12, '03002711':7, '03085602':11, '03233905':6,
        '20000037':10, '02801938':7, '03899768':7, '04343346':7, '03603722':7, '03593526':7, '02954340':7,
        '02694662':7, '04209613':7, '02951358':7, '03115762':9, '04038727':6, '03005285':7, '04559451':7,
        '03775636':7, '03620967':10, '02773838':7, '20000008':6, '04526964':7, '06508816':7, '20000009':6,
        '03379051':7, '04062428':7, '04074963':7, '04047401':7, '03881893':13, '03959485':7, '03391301':7,
        '03151077':12, '04590263':13, '20000006':1, '03148324':6, '20000004':1, '04453156':7, '02840245':2,
        '04591713':7, '03050864':7, '03727837':5, '06277280':11, '03365592':5, '03876519':8, '03179910':7,
        '06709442':7, '03482252':7, '04223580':7, '02880940':7, '04554684':7, '20000030':9, '03085013':7,
        '03169390':7, '04192858':7, '20000029':9, '04331277':4, '03452741':7, '03485997':7, '20000007':1,
        '02942699':7, '03231368':10, '03337140':7, '03001627':4, '20000011':6, '20000010':6, '20000013':6,
        '04603729':10, '20000015':4, '04548280':12, '06410904':2, '04398951':10, '03693474':9, '04330267':7,
        '03015149':9, '04460038':7, '03128519':7, '04306847':7, '03677231':7, '02871439':6, '04550184':6,
        '14974264':7, '04344873':9, '03636649':7, '20000012':6, '02876657':7, '03325088':7, '04253437':7,
        '02992529':7, '03222722':12, '04373704':4, '02851099':13, '04061681':10, '04529681':7, '02691156':7,
        '04099429':7, '02924116':7, '04146614':7, '02690373':7, '02693413':7, '02781338':7
}


NYU_13_CLASSES = [(0,'Unknown'),
                                    (1,'Bed'),
                                    (2,'Books'),
                                    (3,'Ceiling'),
                                    (4,'Chair'),
                                    (5,'Floor'),
                                    (6,'Furniture'),
                                    (7,'Objects'),
                                    (8,'Picture'),
                                    (9,'Sofa'),
                                    (10,'Table'),
                                    (11,'TV'),
                                    (12,'Wall'),
                                    (13,'Window')
]


THREE_CLASSES = [(0,'Unknown'),
                                 (1,'Floor'),
                                 (2,'Background'),
                                 (3,'Objects')
]

NYU_CLASS_TO_THREE_CLASSES = {0:0, 1:3, 2:3, 3:2,  4:3,  5:1,  6:3, 
                                7:3, 8:3, 9:3, 10:3, 11:3, 12:2, 13:2}

def readInfoLog():
    INSTANCE_TO_WNID = {}
    f = open(infoLogFile, 'rb')
    f.readline() #ignore first line
    for line in f:
        instance, WNID = re.split(';|:', line)[1:3]
        WNID = WNID.split(',')[0]
        INSTANCE_TO_WNID [instance] = WNID
    return INSTANCE_TO_WNID


if __name__ == '__main__':
    # startTime = datetime.now()
    f = open (house_temp_dir + houseID+'_fromOcMap.pckl','rb')
    [_,_,_,_,_,_,_,_,rooms_with_light,_] = pickle.load(f)
    f.close()

    for room in rooms_with_light:
        prefix = houseID + "_" + str(room)
        room_output_dir = house_output_temp_dir + prefix + "/"
        infoLogFile = room_output_dir + 'infoNew.log' 

        INSTANCE_TO_WNID = readInfoLog()

        if not os.path.exists(room_output_dir + "labels"):
            os.makedirs(room_output_dir + "labels")

        totalNumPng = len(os.listdir(room_output_dir + 'instance'))
        i = 0

        print 'Generating label pngs from instance pngs and infoNew.log for Room',room,'..'

        for pngfile in glob.glob(room_output_dir + "instance/*.png"):
            imageName=ntpath.basename(pngfile)
            # if i%50 == 0:
            # print 'Generating label from instance png: ', round(float(i)/totalNumPng*100,2), '%'
            im = Image.open(pngfile)
            pix = im.load()

            for x in range(im.size[0]):
                for y in range(im.size[1]):
                    instance = pix[x,y]
                    WNID = INSTANCE_TO_WNID.get(str(instance), 0)
                    NYU = WNID_TO_NYU_CLASS.get(WNID, 0)
                    # if NYU == None: print 'no mapping for :', WNID
                    CLASS = NYU_CLASS_TO_THREE_CLASSES.get(NYU)
                    pix[x,y] = CLASS
                    # if NYU == 0: print instance, WNID, NYU, CLASS


            im.save(room_output_dir + 'labels/' + imageName)
            i += 1

        print 'Labels generated for Room',room
            
        # print datetime.now() - startTime

