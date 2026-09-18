#!/usr/bin/env python3
"""Static brand overlays for the Formwork Builder middle section, drawn straight from the TTFs (Pillow).
Outputs RGBA 1080x1920 PNGs in edit/ovl/."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
W, H = 1080, 1920
F = Path("edit/fonts"); OUT = Path("edit/ovl"); OUT.mkdir(exist_ok=True)
GREEN = (0x19,0x44,0x31,255); LINE = (0x2d,0x8a,0x5b,255); WHITE=(255,255,255,255); INK=(0x0e,0x0e,0x0c,255)
inter = lambda s,w=600: ImageFont.truetype(str(F/f"Inter-{w}.ttf"), s)
def big(s,w=900):
    f = ImageFont.truetype(str(F/"BigShouldersDisplay-VF.ttf"), s); f.set_variation_by_axes([w]); return f
mono  = lambda s,w=700: ImageFont.truetype(str(F/f"JetBrainsMono-{w}.ttf"), s)
def new(): return Image.new("RGBA",(W,H),(0,0,0,0))
def shadowed(img, blur=12, off=(0,6), alpha=140):
    sh = Image.new("RGBA", img.size, (0,0,0,0)); a = img.split()[3].point(lambda v: v*alpha//255)
    sh.paste((0,0,0,255), (off[0],off[1]), a); sh = sh.filter(ImageFilter.GaussianBlur(blur)); return Image.alpha_composite(sh, img)

# 1. banner: solid brand green bar with the logo, 0-150px
BAN_H = 150
ban = new(); d = ImageDraw.Draw(ban); d.rectangle([0,0,W,BAN_H], fill=GREEN)
logo = Image.open("assets/craftons-logo.png").convert("RGBA"); lw = 420; logo = logo.resize((lw, int(logo.height*lw/logo.width)), Image.LANCZOS)
ban.alpha_composite(logo, ((W-lw)//2, (BAN_H-logo.height)//2)); ban.save(OUT/"banner.png")

# 2. hero slide: photo cover-cropped, darkened, headline + sub + pill, banner on top
photo = Image.open("assets/hero-formwork-builder.png").convert("RGB")
s = max(W/photo.width, H/photo.height); photo = photo.resize((int(photo.width*s)+1, int(photo.height*s)+1), Image.LANCZOS)
x0 = (photo.width-W)//2; photo = photo.crop((x0,0,x0+W,H)).convert("RGBA")
dark = Image.new("RGBA",(W,H),(0,0,0,110)); hero = Image.alpha_composite(photo, dark)
d = ImageDraw.Draw(hero)
def center(y, txt, font, fill=WHITE):
    w = d.textlength(txt, font=font); d.text(((W-w)/2, y), txt, font=font, fill=fill)
txt = new(); td = ImageDraw.Draw(txt)
def tcenter(y, s_, font, fill=WHITE):
    w = td.textlength(s_, font=font); td.text(((W-w)/2, y), s_, font=font, fill=fill)
tcenter(700, "Introducing", inter(96,400)); tcenter(820, "Formwork Builder", inter(104,600))
tcenter(1000, "Complete Curved Formwork. Configured Online.", inter(38,400)); tcenter(1056, "Delivered Ready to Assemble.", inter(38,400))
pill = [340,1180,740,1290]; td.rounded_rectangle(pill, radius=55, fill=WHITE); tw = td.textlength("Build Now", font=inter(40,600)); td.text(((W-tw)/2, 1210), "Build Now", font=inter(40,600), fill=INK)
hero = Image.alpha_composite(hero, shadowed(txt, blur=10, off=(0,4), alpha=160)); hero.alpha_composite(ban); hero.save(OUT/"hero.png")

# 3. spec stamp: inner radius, in the empty upper area (model sits low)
def stamp(label, bigtxt, chips, name, y=330):
    im = new(); d = ImageDraw.Draw(im); x = 90
    d.text((x, y), label, font=inter(34,600), fill=LINE, spacing=4)
    d.text((x, y+50), bigtxt, font=big(230,900), fill=INK)
    yy = y+50+250; d.rectangle([x, yy, x+440, yy+6], fill=LINE); yy += 34
    x0 = x
    for c in chips:
        w = d.textlength(c, font=mono(40,700)) + 44
        if x + w > W - 60: x = x0; yy += 68 + 16          # wrap chips that would run off the frame
        d.rounded_rectangle([x, yy, x+w, yy+68], radius=6, fill=GREEN); d.text((x+22, yy+12), c, font=mono(40,700), fill=WHITE); x += w + 18
    shadowed(im, blur=14, off=(0,8), alpha=90).save(OUT/name)
stamp("INNER RADIUS", "R1300", ["600mm high", "600mm thick"], "stamp-radius.png")
stamp("FORMWORK", "SELECTED", ["17mm F17 formply plates", "4mm bendy ply shutters", "end caps"], "stamp-formwork.png")
stamp("INSTANT PRICE  ·  INC GST", "$675", ["dispatched in 5–7 business days"], "stamp-price.png")
print("overlays:", sorted(p.name for p in OUT.glob("*.png")))
