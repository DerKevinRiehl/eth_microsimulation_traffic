import numpy as np
# import matplotlib.pyplot as plt


radius = 27.3
N = 20
for n in range(0,N+1):
    alpha = n/N * 360
    alphas = (n+1)/N * 360
    x = radius * np.cos(alpha/360*2*3.1415)
    y = radius * np.sin(alpha/360*2*3.1415)
    
    xs = radius * np.cos(alphas/360*2*3.1415)
    ys = radius * np.sin(alphas/360*2*3.1415)
    

    
        
    
    
    print('\t<edge id=":J'+str(n)+'_0" function="internal">')
    print('\t\t<lane id=":J'+str(n)+'_0_0" index="0" speed="4.00" length="1.76" shape="0.53,97.53 0.78,97.91 1.11,98.18 1.50,98.35 1.95,98.40"/>')
    print('\t</edge>')
    
    print('\t<edge id="E'+str(n)+'" from="J'+str(n)+'" to="J'+str(n+1)+'" priority="-1">')
    print('\t\t<lane id="E'+str(n)+'_0" index="0" speed="13.89" length="98.05" shape="'+str(x)+','+str(y)+' '+str(xs)+','+str(ys)+'"/>')
    print('\t</edge>')
    
    print('\t<junction id="J'+str(n)+'" type="priority" x="'+str(x)+'" y="'+str(y)+'" incLanes="E'+str(n-1)+'_0" intLanes=":J'+str(n)+'_0_0" shape="1.95,100.00 1.95,96.80 -0.89,98.27 -0.18,99.23 0.26,99.57 0.77,99.81 1.33,99.95">')
    print('\t\t<request index="0" response="0" foes="0" cont="0"/>')
    print('\t</junction>')
    
    
    print('\t<connection from="E'+str(n)+'" to="E'+str(n+1)+'" fromLane="0" toLane="0" via=":J'+str(n+1)+'_0_0" dir="s" state="M"/>')
    print('\t<connection from=":J'+str(n)+'_0" to="E'+str(n)+'" fromLane="0" toLane="0" dir="r" state="M"/>')
    
# plt.plot(xs,ys)