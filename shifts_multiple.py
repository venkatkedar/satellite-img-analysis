# this function takes in numpy img , rows, cols and shifts based on values passed in rows and cols
# if rows is -ve, it shifts upwards else downwards
# if cols is -ve, it shifts left else right
# it returns numpy array of shifted img , no change in dimensions
def shift(img,rows,cols):
	if(rows==0 and cols==0):
        return img
    
    zr=np.zeros((abs(rows),img.shape[1]))
    zc=np.zeros((img.shape[0],abs(cols)))
    
    if(rows>0):
        #shift down
        img=np.concatenate((zr,img[:-rows,:]),axis=0)      
    else :
        #shift up
        img=np.concatenate((img[-rows:,:],zr),axis=0)
    if(cols>0):
        #shift right
        img=np.concatenate((zc,img[:,:-cols]),axis=1)      
    else :
        #shift left
        img=np.concatenate((img[:,-cols:],zc),axis=1)
        
    return img


# it has been observed that the shift given in paper is true for the entire image as far as 
# African countries are concerned 
# this function shifts the image based on year and satellite type
# it takes img as numpy array , satellite type as string (e.g. 'F14','F16') and year
# it maintains a internal dict from where it searches for the amount of shift for that year and satellite type
# it returns numpy array of shifted img , no change in dimensions of img

def shiftByYear(img,sat_type,year):
    # dict that holds values of how much to shift vertically and horizontally
    # key is a tuple of satellite type and year and value is a tuple of vertical shift, horizontal shift
    # if the vertical shift is -ve , it shifts upwards else downwards
    # if horizontal shift is -ve , it shifts left else right
    shift_dict={('F14',1999):(0,0),('F12',1999):(0,-1),('F14',2000):(0,0),('F14',2001):(0,0),('F14',2002):(0,0),
                ('F14',2003):(0,0),('F15',2000):(-1,-1),('F15',2001):(0,-1),('F15',2006):(0,0),('F15',2007):(0,0),
                ('F16',2004):(-1,0),('F16',2005):(0,0),('F16',2006):(0,0),('F16',2007):(0,0),('F16',2008):(0,-1)
               ,('F16',2009):(-1,0),('F18',2010):(-1,0)}
    rows,cols=shift_dict.get((sat_type,year),(0,0))
    
    shift(img,rows,cols)

#below function finds img which gives minimum value of the sum of squares by shifting img2 in 8 directions around a pixel
# and checking for sum of squares with img1 (img1 is baseline image - F121999)
#shift_list holds the amount of vertical and horizontal shift 

def shiftByImg(img1, img2):
    shift_list=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]

    # this code shifts the img and finds sum of squares for each shift given in shift_list 
    s_diff=[(k,np.sum((shift(img2,k[0],k[1])-img1)**2)) for k in shift_list]

    # this line collects sum of squares in a list
    min_list=[p[1] for p in s_diff]

    # finds arg_min
    arg_min=np.argmin(min_list)

    # gives the shifted image for arg_min
    img3=shift(img2,s_diff[arg_min][0][0],s_diff[arg_min][0][1])
    
    return img3

