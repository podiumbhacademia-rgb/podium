# gera caminhos SVG orgânicos (mancha com respingos e ondas laterais)
import math, random
def blob(cx, cy, w, h, n=90, amp=10, drips=9, seed=3):
    random.seed(seed)
    pts=[]
    dr=set(random.sample(range(n), drips))
    for i in range(n):
        t=i/n*2*math.pi
        # superelipse (retângulo arredondado)
        c, s = math.cos(t), math.sin(t)
        e=0.35
        x = cx + w/2*math.copysign(abs(c)**e, c)
        y = cy + h/2*math.copysign(abs(s)**e, s)
        r = random.uniform(-amp, amp)
        if i in dr: r += random.uniform(18, 34)
        nx, ny = x-cx, y-cy; L=math.hypot(nx,ny) or 1
        pts.append((x+nx/L*r, y+ny/L*r))
    d=f"M{pts[0][0]:.1f} {pts[0][1]:.1f} "
    for i in range(n):
        p0=pts[i]; p1=pts[(i+1)%n]
        mx,my=(p0[0]+p1[0])/2,(p0[1]+p1[1])/2
        d+=f"Q{p0[0]:.1f} {p0[1]:.1f} {mx:.1f} {my:.1f} "
    return d+"Z"
def wave(x0, width, y0, y1, k=5, amp=26, side=1, seed=1):
    random.seed(seed)
    steps=60; pts=[]
    for i in range(steps+1):
        y=y0+(y1-y0)*i/steps
        x=x0+side*(width+amp*math.sin(i/steps*k*math.pi+seed))
        pts.append((x,y))
    d=f"M{x0} {y0} "+" ".join(f"L{x:.1f} {y:.1f}" for x,y in pts)+f" L{x0} {y1} Z"
    return d
if __name__=="__main__":
    print(blob(397,460,640,400))
